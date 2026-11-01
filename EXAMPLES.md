# 💡 LangGraph Examples - Từ Cơ Bản Đến Nâng Cao

## Example 1: Simple Graph (Không cần LLM)

**File**: `app/agents/simple_example.py`

**Mục đích**: Hiểu cách graph hoạt động mà không cần API key

**Run**:
```bash
python test_simple.py
```

**Học được gì**:
- State được truyền qua các nodes
- Mỗi node xử lý và return state mới
- Graph tự động merge states

---

## Example 2: Calculator Agent (Basic ReAct)

**File**: `app/agents/calculator_agent.py`

**Mục đích**: Agent tự động quyết định gọi tools

**Flow**:
```
User: "Tính 25 * 4 + 10"
  ↓
Agent: "Tôi cần gọi multiply(25, 4)"
  ↓
Tool: multiply(25, 4) = 100
  ↓
Agent: "Giờ tôi cần cộng 100 + 10"
  ↓
Tool: add(100, 10) = 110
  ↓
Agent: "Kết quả là 110"
```

**Run**:
```bash
# Start server
python run.py

# Test
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tính 25 * 4 + 10"}'
```

---

## Example 3: Conversation với Memory

**Tạo file mới**: `app/agents/memory_agent.py`

```python
from typing import Annotated
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import HumanMessage, SystemMessage

class ConversationState(MessagesState):
    """State có memory"""
    user_name: str = ""
    conversation_count: int = 0

def greeting_node(state: ConversationState):
    """Node chào hỏi"""
    messages = state["messages"]
    last_msg = messages[-1].content
    
    # Extract name nếu có
    if "tôi là" in last_msg.lower():
        name = last_msg.lower().split("tôi là")[1].strip()
        return {
            "messages": [HumanMessage(
                content=f"Xin chào {name}! Rất vui được gặp bạn."
            )],
            "user_name": name,
            "conversation_count": state.get("conversation_count", 0) + 1
        }
    
    return {
        "messages": [HumanMessage(
            content="Xin chào! Tôi có thể giúp gì cho bạn?"
        )],
        "conversation_count": state.get("conversation_count", 0) + 1
    }

def memory_node(state: ConversationState):
    """Node nhớ context"""
    user_name = state.get("user_name", "")
    count = state.get("conversation_count", 0)
    
    if user_name:
        msg = f"Này {user_name}, chúng ta đã nói chuyện {count} lần rồi đấy!"
    else:
        msg = f"Chúng ta đã trao đổi {count} messages."
    
    return {"messages": [HumanMessage(content=msg)]}

# Build graph
workflow = StateGraph(ConversationState)
workflow.add_node("greeting", greeting_node)
workflow.add_node("memory", memory_node)
workflow.add_edge(START, "greeting")
workflow.add_edge("greeting", "memory")
workflow.add_edge("memory", END)

memory_graph = workflow.compile()
```

**Test**:
```python
# Message 1
result1 = memory_graph.invoke({
    "messages": [HumanMessage(content="Xin chào, tôi là Nam")]
})

# Message 2 - agent sẽ nhớ tên
result2 = memory_graph.invoke({
    "messages": result1["messages"] + [
        HumanMessage(content="Bạn còn nhớ tên tôi không?")
    ],
    "user_name": result1["user_name"],
    "conversation_count": result1["conversation_count"]
})
```

---

## Example 4: Human-in-the-Loop

**Concept**: Agent pause để hỏi user trước khi thực hiện action nguy hiểm

```python
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

class ApprovalState(MessagesState):
    pending_action: str = ""
    approved: bool = False

def action_node(state: ApprovalState):
    """Node đề xuất action"""
    return {
        "messages": [HumanMessage(
            content="Tôi sẽ xóa tất cả files. Bạn có chắc không?"
        )],
        "pending_action": "delete_all_files"
    }

def should_execute(state: ApprovalState) -> str:
    """Check approval"""
    if state["approved"]:
        return "execute"
    return "wait_approval"

def execute_node(state: ApprovalState):
    """Execute action sau khi được approve"""
    action = state["pending_action"]
    return {
        "messages": [HumanMessage(
            content=f"Đã thực hiện: {action}"
        )]
    }

# Build graph với checkpointer
memory = MemorySaver()
workflow = StateGraph(ApprovalState)
workflow.add_node("action", action_node)
workflow.add_node("execute", execute_node)
workflow.add_edge(START, "action")
workflow.add_conditional_edges(
    "action",
    should_execute,
    {
        "execute": "execute",
        "wait_approval": END  # Pause ở đây
    }
)
workflow.add_edge("execute", END)

approval_graph = workflow.compile(checkpointer=memory)
```

**Usage**:
```python
# Step 1: Agent đề xuất
thread = {"configurable": {"thread_id": "1"}}
result = approval_graph.invoke(
    {"messages": [HumanMessage(content="Xóa files đi")]},
    thread
)
# Output: "Tôi sẽ xóa tất cả files. Bạn có chắc không?"

# Step 2: User approve
result = approval_graph.invoke(
    {"approved": True},
    thread
)
# Output: "Đã thực hiện: delete_all_files"
```

---

## Example 5: Parallel Tool Execution

**Concept**: Gọi nhiều tools cùng lúc để tăng tốc

```python
import asyncio
from langchain_core.tools import tool

@tool
async def fetch_weather(city: str) -> str:
    """Lấy thời tiết"""
    await asyncio.sleep(1)  # Simulate API call
    return f"Thời tiết ở {city}: Nắng đẹp"

@tool
async def fetch_news(topic: str) -> str:
    """Lấy tin tức"""
    await asyncio.sleep(1)  # Simulate API call
    return f"Tin tức về {topic}: ..."

# Agent có thể gọi cả 2 tools song song
# LangGraph tự động parallelize nếu tools độc lập
```

---

## Example 6: Conditional Routing (Router Agent)

**Concept**: Route đến node khác nhau dựa trên user intent

```python
def classify_intent(state: MessagesState) -> str:
    """Phân loại intent của user"""
    last_msg = state["messages"][-1].content.lower()
    
    if "thời tiết" in last_msg:
        return "weather"
    elif "tin tức" in last_msg:
        return "news"
    elif "tính toán" in last_msg:
        return "calculator"
    else:
        return "general"

# Build router graph
workflow = StateGraph(MessagesState)
workflow.add_node("weather_handler", handle_weather)
workflow.add_node("news_handler", handle_news)
workflow.add_node("calculator_handler", handle_calculator)
workflow.add_node("general_handler", handle_general)

workflow.add_conditional_edges(
    START,
    classify_intent,
    {
        "weather": "weather_handler",
        "news": "news_handler",
        "calculator": "calculator_handler",
        "general": "general_handler"
    }
)
```

---

## Example 7: Retry với Exponential Backoff

**Concept**: Tự động retry khi tool fail

```python
import time

class RetryState(MessagesState):
    retry_count: int = 0
    max_retries: int = 3

def tool_with_retry(state: RetryState):
    """Tool có thể fail"""
    try:
        result = unreliable_api_call()
        return {"messages": [HumanMessage(content=result)]}
    except Exception as e:
        retry_count = state["retry_count"]
        if retry_count < state["max_retries"]:
            wait_time = 2 ** retry_count  # Exponential backoff
            time.sleep(wait_time)
            return {"retry_count": retry_count + 1}
        else:
            return {
                "messages": [HumanMessage(
                    content=f"Failed sau {retry_count} lần retry: {e}"
                )]
            }

def should_retry(state: RetryState) -> str:
    if state["retry_count"] < state["max_retries"]:
        return "retry"
    return "end"
```

---

## Example 8: Multi-Agent Collaboration

**Concept**: Nhiều agents làm việc cùng nhau

```python
class MultiAgentState(MessagesState):
    current_agent: str = "researcher"
    research_done: bool = False
    draft_done: bool = False

def researcher_agent(state: MultiAgentState):
    """Agent research thông tin"""
    # Do research
    return {
        "messages": [HumanMessage(content="Đã research xong")],
        "research_done": True,
        "current_agent": "writer"
    }

def writer_agent(state: MultiAgentState):
    """Agent viết bài"""
    # Write article
    return {
        "messages": [HumanMessage(content="Đã viết xong")],
        "draft_done": True,
        "current_agent": "reviewer"
    }

def reviewer_agent(state: MultiAgentState):
    """Agent review"""
    # Review and approve
    return {
        "messages": [HumanMessage(content="Đã review, OK!")]
    }

# Connect agents
workflow.add_edge("researcher", "writer")
workflow.add_edge("writer", "reviewer")
```

---

## Example 9: RAG Pipeline

**Concept**: Retrieve → Generate với LangGraph

```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class RAGState(MessagesState):
    retrieved_docs: list = []
    context: str = ""

def retrieve_node(state: RAGState):
    """Retrieve relevant docs"""
    query = state["messages"][-1].content
    
    # Search vector store
    docs = vectorstore.similarity_search(query, k=3)
    
    return {
        "retrieved_docs": docs,
        "context": "\n".join([doc.page_content for doc in docs])
    }

def generate_node(state: RAGState):
    """Generate answer với context"""
    context = state["context"]
    question = state["messages"][-1].content
    
    prompt = f"""
    Context: {context}
    
    Question: {question}
    
    Answer:
    """
    
    response = llm.invoke(prompt)
    return {"messages": [response]}

# RAG graph
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "generate")
```

---

## Example 10: Streaming Responses

**Concept**: Stream responses real-time

```python
from fastapi.responses import StreamingResponse

@router.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Stream agent responses"""
    
    async def generate():
        graph = get_calculator_agent()
        
        async for event in graph.astream_events(
            {"messages": [HumanMessage(content=request.message)]},
            version="v1"
        ):
            if event["event"] == "on_chat_model_stream":
                chunk = event["data"]["chunk"]
                yield f"data: {chunk.content}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

**Test**:
```bash
curl -N http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{"message": "Tính 10 + 20"}'
```

---

## 🎯 Kết Luận

Các examples này cover:
- ✅ Basic graphs
- ✅ ReAct agents
- ✅ Memory management
- ✅ Human-in-the-loop
- ✅ Parallel execution
- ✅ Conditional routing
- ✅ Error handling & retry
- ✅ Multi-agent systems
- ✅ RAG pipelines
- ✅ Streaming

**Next**: Implement các patterns này vào use case của bạn!
