"""
Calculator Agent sử dụng LangGraph
Đây là example cơ bản về cách xây dựng một agent với LangGraph
"""
from typing import Annotated, TypedDict, Literal
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode
from langgraph.graph.message import add_messages

from app.agents.tools import ALL_TOOLS
from app.core.config import settings


class AgentState(TypedDict):
    """
    State của agent - chứa messages và metadata
    LangGraph sẽ tự động merge state giữa các nodes
    """
    # Sử dụng add_messages reducer để tự động append messages
    messages: Annotated[list[BaseMessage], add_messages]


def create_model():
    """
    Tạo LLM model dựa trên API keys có sẵn
    """
    if settings.OPENAI_API_KEY:
        print("🤖 Đang sử dụng OpenAI GPT-4")
        model = ChatOpenAI(
            model="gpt-4o-mini",
            api_key=settings.OPENAI_API_KEY,
            temperature=0
        )
    elif settings.ANTHROPIC_API_KEY:
        print("🤖 Đang sử dụng Anthropic Claude")
        model = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            api_key=settings.ANTHROPIC_API_KEY,
            temperature=0
        )
    else:
        raise ValueError(
            "Cần ít nhất một API key! "
            "Hãy set OPENAI_API_KEY hoặc ANTHROPIC_API_KEY trong .env file"
        )
    
    # Bind tools vào model
    return model.bind_tools(ALL_TOOLS)


def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """
    Quyết định xem có cần gọi tools hay kết thúc
    
    Đây là conditional edge function - routing logic của graph
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # Nếu LLM muốn gọi tool, route đến tools node
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    
    # Ngược lại, kết thúc
    return "end"


def call_model(state: AgentState) -> AgentState:
    """
    Node gọi LLM model
    
    Đây là main reasoning node - nơi LLM suy nghĩ và quyết định
    """
    messages = state["messages"]
    model = create_model()
    
    response = model.invoke(messages)
    
    # Return dict sẽ được merge vào state
    return {"messages": [response]}


def create_calculator_graph():
    """
    Tạo LangGraph workflow cho calculator agent
    
    Graph structure:
    START -> agent -> should_continue? 
                        -> tools -> agent (nếu cần tools)
                        -> END (nếu không cần tools)
    """
    # 1. Khởi tạo graph với AgentState
    workflow = StateGraph(AgentState)
    
    # 2. Add nodes
    workflow.add_node("agent", call_model)  # Node gọi LLM
    workflow.add_node("tools", ToolNode(ALL_TOOLS))  # Node execute tools
    
    # 3. Set entry point
    workflow.add_edge(START, "agent")
    
    # 4. Add conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",  # Nếu cần tools, đi đến tools node
            "end": END,  # Nếu không, kết thúc
        }
    )
    
    # 5. Tools luôn quay lại agent để process kết quả
    workflow.add_edge("tools", "agent")
    
    # 6. Compile graph thành runnable
    return workflow.compile()


# Singleton instance của graph
_graph = None


def get_calculator_agent():
    """
    Lấy calculator agent instance (singleton pattern)
    """
    global _graph
    if _graph is None:
        _graph = create_calculator_graph()
    return _graph


async def run_agent(message: str) -> dict:
    """
    Chạy agent với một message
    
    Args:
        message: Câu hỏi/yêu cầu từ user
        
    Returns:
        Dict chứa response và metadata
    """
    graph = get_calculator_agent()
    
    # Tạo initial state
    initial_state = {
        "messages": [HumanMessage(content=message)]
    }
    
    # Run graph
    result = await graph.ainvoke(initial_state)
    
    # Extract response
    last_message = result["messages"][-1]
    
    return {
        "response": last_message.content,
        "messages": result["messages"],
        "steps": len(result["messages"]),
    }
