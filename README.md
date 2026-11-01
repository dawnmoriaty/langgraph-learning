# 🤖 LangGraph với FastAPI - Hướng Dẫn Từ Đầu

Đây là project demo về cách xây dựng AI Agent với **LangGraph** và tích hợp với **FastAPI**.

## 📚 Mục Lục

- [LangGraph là gì?](#langgraph-là-gì)
- [Cấu trúc project](#cấu-trúc-project)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Chạy ứng dụng](#chạy-ứng-dụng)
- [Sử dụng API](#sử-dụng-api)
- [Hiểu về LangGraph](#hiểu-về-langgraph)
- [Roadmap học tiếp](#roadmap-học-tiếp)

---

## 🎯 LangGraph là gì?

**LangGraph** là thư viện Python để xây dựng **stateful AI agents** và **workflows phức tạp** với LLM.

### Tại sao dùng LangGraph?

- ✅ **Stateful**: Giữ lại state giữa các bước xử lý
- ✅ **Cyclic**: Hỗ trợ loops - agent có thể gọi tools nhiều lần
- ✅ **Multi-actor**: Nhiều agents phối hợp làm việc
- ✅ **Visual**: Có thể visualize workflow dạng graph
- ✅ **Control**: Kiểm soát chính xác flow của agent

### So sánh với LangChain thường

| Feature | LangChain | LangGraph |
|---------|-----------|-----------|
| Simple chains | ✅ Tốt | ⚠️ Overkill |
| Complex workflows | ⚠️ Khó | ✅ Tốt |
| Loops/Cycles | ❌ Không | ✅ Có |
| State management | ⚠️ Giới hạn | ✅ Linh hoạt |
| Visual debugging | ❌ | ✅ |

---

## 📁 Cấu Trúc Project

```
langgraph-fastapi-demo/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── agents/              # LangGraph agents
│   │   ├── __init__.py
│   │   ├── tools.py         # Tools cho agent (add, subtract, etc.)
│   │   ├── calculator_agent.py  # Main calculator agent
│   │   └── simple_example.py    # Example cơ bản nhất
│   ├── api/                 # API routes
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/                # Core configs
│   │   ├── __init__.py
│   │   └── config.py
│   └── models/              # Pydantic models
│       ├── __init__.py
│       └── schemas.py
├── .env                     # Environment variables (bạn tạo)
├── .env.example             # Template cho .env
├── .gitignore
├── requirements.txt         # Dependencies
├── pyproject.toml          # Poetry config
├── run.py                  # Script chạy server
├── test_simple.py          # Test simple example
└── README.md               # File này
```

---

## 🚀 Cài Đặt

### Bước 1: Clone hoặc tạo project

```bash
# Nếu chưa có, tạo thư mục
mkdir langgraph-demo
cd langgraph-demo
```

### Bước 2: Tạo virtual environment

```bash
# Tạo venv
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Bước 3: Cài đặt dependencies

```bash
# Cách 1: Dùng pip
pip install -r requirements.txt

# Cách 2: Dùng poetry (nếu bạn dùng poetry)
poetry install
```

### Bước 4: Verify cài đặt

```bash
python -c "import langgraph; print(f'LangGraph version: {langgraph.__version__}')"
```

---

## ⚙️ Cấu Hình

### 1. Tạo file `.env`

```bash
cp .env.example .env
```

### 2. Thêm API key vào `.env`

Bạn cần **ít nhất một** trong các API keys sau:

#### Option A: Dùng OpenAI (GPT-4)

```bash
OPENAI_API_KEY=sk-your-openai-key-here
```

👉 Lấy key tại: https://platform.openai.com/api-keys

#### Option B: Dùng Anthropic (Claude)

```bash
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
```

👉 Lấy key tại: https://console.anthropic.com/

#### Option C: Dùng Google (Gemini)

```bash
GOOGLE_API_KEY=your-google-key-here
```

👉 Lấy key tại: https://makersuite.google.com/app/apikey

### 3. File `.env` hoàn chỉnh

```bash
# Chọn một trong các API keys này
OPENAI_API_KEY=sk-your-key-here
# ANTHROPIC_API_KEY=sk-ant-your-key-here
# GOOGLE_API_KEY=your-key-here

# App settings (optional)
APP_NAME="LangGraph FastAPI Demo"
DEBUG=True
HOST=0.0.0.0
PORT=8000

# LangSmith tracing (optional - để debug)
LANGCHAIN_TRACING_V2=false
# LANGCHAIN_API_KEY=your-langsmith-key
# LANGCHAIN_PROJECT=langgraph-demo
```

---

## 🎮 Chạy Ứng Dụng

### Option 1: Test Simple Example (Không cần API key)

Đây là cách tốt nhất để hiểu LangGraph trước:

```bash
python test_simple.py
```

Bạn sẽ thấy:
```
🚀 LANGGRAPH SIMPLE EXAMPLE
==================================================

📍 Đang ở Node 1: Chào hỏi
📍 Đang ở Node 2: Xử lý
📍 Đang ở Node 3: Kết thúc

==================================================
📋 KẾT QUẢ
==================================================
Tổng số messages: 3

Các messages:
  1. Xin chào từ Node 1!
  2. Đã xử lý: 'Xin chào từ Node 1!' ở Node 2
  3. Hoàn thành!
```

### Option 2: Chạy FastAPI Server

```bash
# Cách 1: Dùng script run.py
python run.py

# Cách 2: Dùng uvicorn trực tiếp
uvicorn app.main:app --reload

# Cách 3: Từ app/main.py
python -m app.main
```

Server sẽ chạy tại: **http://localhost:8000**

### Option 3: Chạy với Docker (Bonus)

```bash
# TODO: Thêm Dockerfile nếu cần
```

---

## 📡 Sử Dụng API

### 1. Xem API Documentation

Mở browser và vào:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 2. Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "langgraph-fastapi",
  "version": "0.1.0"
}
```

### 3. Xem danh sách Tools

```bash
curl http://localhost:8000/tools
```

Response:
```json
{
  "total": 4,
  "tools": [
    {
      "name": "add",
      "description": "Cộng hai số lại với nhau.",
      "args": {"a": "float", "b": "float"}
    },
    ...
  ]
}
```

### 4. Chat với Agent

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tính 25 * 4 + 10"
  }'
```

Response:
```json
{
  "response": "Kết quả là 110",
  "conversation_id": "conv_abc123",
  "metadata": {
    "steps": 5,
    "message_count": 5
  }
}
```

### 5. Test với Python

```python
import requests

response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "15 chia cho 3 bằng mấy?"}
)

print(response.json())
```

### 6. Test với JavaScript/TypeScript

```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    message: 'Tính 100 - 25'
  })
});

const data = await response.json();
console.log(data);
```

---

## 🧠 Hiểu Về LangGraph

### 1. Khái niệm cơ bản

#### State
- **State** là dữ liệu được truyền qua các nodes
- Mỗi node nhận state, xử lý, và return state mới
- LangGraph tự động merge states

```python
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
```

#### Nodes
- **Nodes** là các hàm xử lý logic
- Mỗi node nhận state và return state mới

```python
def call_model(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = model.invoke(messages)
    return {"messages": [response]}
```

#### Edges
- **Edges** kết nối các nodes
- Có 2 loại:
  - **Normal edge**: Luôn đi theo path cố định
  - **Conditional edge**: Quyết định path dựa trên logic

```python
# Normal edge
workflow.add_edge("node_a", "node_b")

# Conditional edge
workflow.add_conditional_edges(
    "agent",
    should_continue,  # Function quyết định
    {
        "tools": "tools",
        "end": END
    }
)
```

### 2. Flow của Calculator Agent

```
START
  ↓
[Agent Node] → Gọi LLM để suy nghĩ
  ↓
[Should Continue?] → Kiểm tra có cần tools không?
  ↓              ↓
  YES            NO
  ↓              ↓
[Tools Node]   [END]
  ↓
[Agent Node] → Xử lý kết quả từ tools
  ↓
[Should Continue?] → ...
```

### 3. Tại sao cần LangGraph cho Calculator?

**Câu hỏi**: Tại sao không dùng simple chain?

**Trả lời**: Vì agent cần **tự quyết định**:
1. Phép tính nào cần thực hiện trước
2. Gọi bao nhiêu tools
3. Tools nào cần gọi
4. Khi nào dừng lại

Ví dụ với câu: **"Tính (10 + 5) * 2 - 3"**

Agent sẽ:
1. 🤔 Suy nghĩ: Cần tính 10 + 5 trước
2. 🔧 Gọi `add(10, 5)` → 15
3. 🤔 Suy nghĩ: Giờ nhân với 2
4. 🔧 Gọi `multiply(15, 2)` → 30
5. 🤔 Suy nghĩ: Cuối cùng trừ 3
6. 🔧 Gọi `subtract(30, 3)` → 27
7. ✅ Trả lời: "Kết quả là 27"

### 4. Code walkthrough

#### 4.1. Định nghĩa tools

```python
@tool
def add(a: float, b: float) -> float:
    """Cộng hai số lại với nhau"""
    return a + b
```

#### 4.2. Tạo graph

```python
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", ToolNode(ALL_TOOLS))
```

#### 4.3. Routing logic

```python
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    last_message = state["messages"][-1]
    
    if last_message.tool_calls:
        return "tools"  # Gọi tools
    return "end"  # Kết thúc
```

#### 4.4. Compile và run

```python
graph = workflow.compile()
result = await graph.ainvoke(initial_state)
```

---

## 📖 Roadmap Học Tiếp

### Bước 1: Hiểu cơ bản ✅ (Bạn đang ở đây)
- [x] Cài đặt LangGraph
- [x] Chạy simple example
- [x] Hiểu State, Nodes, Edges
- [x] Tạo basic agent với tools

### Bước 2: Nâng cao Agent
- [ ] Thêm **memory** để agent nhớ conversation
- [ ] Implement **human-in-the-loop** (agent hỏi user)
- [ ] Thêm **streaming** responses
- [ ] Handle **errors** và **retries**

### Bước 3: Multi-Agent System
- [ ] Tạo nhiều agents phối hợp
- [ ] Agent routing (chọn agent phù hợp)
- [ ] Agent collaboration patterns

### Bước 4: Production-Ready
- [ ] Add authentication
- [ ] Rate limiting
- [ ] Caching responses
- [ ] Monitoring và logging
- [ ] Deploy lên cloud

### Tài liệu học thêm

1. **LangGraph Official Docs**: https://langchain-ai.github.io/langgraph/
2. **LangChain Docs**: https://python.langchain.com/
3. **FastAPI Docs**: https://fastapi.tiangolo.com/
4. **Examples Gallery**: https://github.com/langchain-ai/langgraph/tree/main/examples

---

## 🎯 Use Cases Thực Tế

### 1. Customer Support Bot
- Trả lời câu hỏi
- Tìm kiếm knowledge base
- Escalate đến human nếu cần

### 2. Data Analysis Agent
- Đọc data từ database
- Phân tích và tạo charts
- Trả lời insight

### 3. Code Review Agent
- Đọc code
- Tìm bugs và security issues
- Suggest improvements

### 4. Research Assistant
- Search web
- Summarize papers
- Generate reports

---

## 🐛 Troubleshooting

### Lỗi: "No API key found"

**Giải pháp**: Kiểm tra file `.env` và đảm bảo có ít nhất một API key.

### Lỗi: "Module not found"

**Giải pháp**:
```bash
# Activate venv
source venv/bin/activate

# Install lại
pip install -r requirements.txt
```

### Lỗi: "Port 8000 already in use"

**Giải pháp**: Đổi port trong `.env`:
```bash
PORT=8001
```

### Agent không gọi tools

**Nguyên nhân**: LLM có thể cần prompt rõ ràng hơn.

**Giải pháp**: Thử câu hỏi rõ ràng hơn:
- ❌ "Tính toán gì đó"
- ✅ "Tính 25 * 4"

---

## 🤝 Contributing

Đây là project demo cho mục đích học tập. Feel free to fork và customize!

---

## 📝 License

MIT License - Tự do sử dụng và chỉnh sửa.

---

## 💬 Liên Hệ & Hỗ Trợ

Nếu có câu hỏi:
1. Đọc kỹ README này
2. Check issues trên GitHub
3. Tham gia LangChain Discord: https://discord.gg/langchain

---

**Happy Learning! 🚀**

Chúc bạn học tốt LangGraph và xây dựng được những AI agents tuyệt vời!
