"""
Example đơn giản nhất về LangGraph
Để hiểu cách LangGraph hoạt động từ cơ bản
"""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage


class SimpleState(TypedDict):
    """State đơn giản chỉ có messages"""
    messages: Annotated[list[BaseMessage], add_messages]


def simple_node_1(state: SimpleState) -> SimpleState:
    """Node 1 - Chào hỏi"""
    print("📍 Đang ở Node 1: Chào hỏi")
    return {
        "messages": [HumanMessage(content="Xin chào từ Node 1!")]
    }


def simple_node_2(state: SimpleState) -> SimpleState:
    """Node 2 - Xử lý"""
    print("📍 Đang ở Node 2: Xử lý")
    messages = state["messages"]
    
    # Lấy message cuối cùng và process
    last_msg = messages[-1].content
    processed = f"Đã xử lý: '{last_msg}' ở Node 2"
    
    return {
        "messages": [HumanMessage(content=processed)]
    }


def simple_node_3(state: SimpleState) -> SimpleState:
    """Node 3 - Kết thúc"""
    print("📍 Đang ở Node 3: Kết thúc")
    return {
        "messages": [HumanMessage(content="Hoàn thành!")]
    }


def create_simple_graph():
    """
    Tạo một graph đơn giản để demo
    
    Flow: START -> node1 -> node2 -> node3 -> END
    """
    workflow = StateGraph(SimpleState)
    
    # Thêm các nodes
    workflow.add_node("node1", simple_node_1)
    workflow.add_node("node2", simple_node_2)
    workflow.add_node("node3", simple_node_3)
    
    # Kết nối các nodes
    workflow.add_edge(START, "node1")
    workflow.add_edge("node1", "node2")
    workflow.add_edge("node2", "node3")
    workflow.add_edge("node3", END)
    
    return workflow.compile()


def run_simple_example():
    """Chạy example đơn giản"""
    print("\n" + "="*50)
    print("🚀 LANGGRAPH SIMPLE EXAMPLE")
    print("="*50 + "\n")
    
    graph = create_simple_graph()
    
    # Chạy graph với empty state
    result = graph.invoke({"messages": []})
    
    print("\n" + "="*50)
    print("📋 KẾT QUẢ")
    print("="*50)
    print(f"Tổng số messages: {len(result['messages'])}")
    print("\nCác messages:")
    for i, msg in enumerate(result["messages"], 1):
        print(f"  {i}. {msg.content}")
    print("\n" + "="*50)
    
    return result


if __name__ == "__main__":
    # Chạy trực tiếp file này để test
    run_simple_example()
