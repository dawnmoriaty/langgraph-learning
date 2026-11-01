# 🎯 Refactored Project Guide

## ✅ Hoàn Thành

Đã refactor project theo P-041 architecture với:

1. ✅ **Integrations** - Provider registry với fallback
2. ✅ **Core Config** - Tách theo domain  
3. ✅ **Common Utilities** - Responses, errors, handlers
4. ✅ **Modules** - Router → Service pattern

---

## 🚀 Quick Start - TEST NGAY!

### Bước 1: Setup (nếu chưa)

```bash
# Activate venv (nếu chưa có, tạo mới)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Bước 2: Config API Keys

```bash
# Copy .env
cp .env.example .env

# Edit .env và thêm ÍT NHẤT 1 API key:
# OPENAI_API_KEY=sk-...
# hoặc ANTHROPIC_API_KEY=sk-ant-...
# hoặc GOOGLE_API_KEY=...
```

### Bước 3: TEST INTEGRATIONS (QUAN TRỌNG!)

```bash
python test_integrations.py
```

**Bạn sẽ thấy**:
```
🔍 TESTING LLM INTEGRATIONS
===========================================================

📦 Step 1: Initializing LLM Registry...
   ✅ openai       - openai       (gpt-4o-mini)
   ⭐ Registered providers...

🏥 Step 2: Health Check (với LLM calls thật)
   Đang test từng provider...
   
   Overall Status: HEALTHY
   Healthy: 1/3
   ✅ openai       - OK (523ms)
   ⚠️  anthropic   - No API key
   ⚠️  google      - No API key

🔄 Step 3: Testing Fallback Mechanism
   Testing order: openai → anthropic → google
   ✅ Success with: gpt-4o-mini (645ms)
```

### Bước 4: Chạy Server

```bash
python run.py
```

**Output**:
```
╔══════════════════════════════════════════════════════════╗
║     🚀 LangGraph FastAPI Demo Server (Refactored)       ║
╚══════════════════════════════════════════════════════════╝

🚀 Starting application...
App: LangGraph FastAPI Demo v0.2.0
Environment: development

📦 Initializing LLM Registry...
✅ 1 providers available: openai

✅ Application started successfully!
📚 Docs: http://0.0.0.0:8000/docs
🏥 Health: http://0.0.0.0:8000/health
```

### Bước 5: Test Endpoints

#### A. Basic Health Check

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "version": "0.2.0",
    "environment": "development",
    "timestamp": 1234567890
  },
  "error": null,
  "meta": null
}
```

#### B. Detailed Health với Config

```bash
curl http://localhost:8000/health/detailed
```

Response:
```json
{
  "success": true,
  "data": {
    "status": "healthy",
    "config": {
      "app": {
        "name": "LangGraph FastAPI Demo",
        "version": "0.2.0",
        "env": "development"
      },
      "llm": {
        "available_providers": ["openai"],
        "temperature": 0.0
      }
    },
    "warnings": []
  }
}
```

#### C. Integration Health (Test API Keys!)

```bash
curl http://localhost:8000/health/integrations
```

Response:
```json
{
  "success": true,
  "data": {
    "overall_status": "healthy",
    "total": 3,
    "healthy": 1,
    "providers": [
      {
        "provider": "openai",
        "status": "healthy",
        "available": true,
        "response_time": 0.523
      },
      {
        "provider": "anthropic",
        "status": "no_api_key",
        "available": false
      }
    ]
  }
}
```

#### D. Chat với Agent (Placeholder)

```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tính 10 + 20"
  }'
```

Response:
```json
{
  "success": true,
  "data": {
    "response": "[Agent response cho: Tính 10 + 20]",
    "conversation_id": "conv_abc123",
    "metadata": {
      "steps": 1,
      "provider": "placeholder"
    }
  }
}
```

---

## 📂 Cấu Trúc Mới

```
project/
├── src/                    # NEW! Monorepo structure
│   ├── integrations/      # ✅ LLM provider registry
│   │   ├── llm_registry.py   # Provider registry với fallback
│   │   └── health.py          # Health checker
│   │
│   ├── core/              # ✅ Core system
│   │   ├── config/           # Config tách theo domain
│   │   │   ├── app.py           # App settings
│   │   │   ├── llm.py           # LLM settings
│   │   │   ├── agent.py         # Agent settings
│   │   │   ├── security.py      # Security settings
│   │   │   └── settings.py      # Unified settings
│   │   └── common/           # Common utilities
│   │       ├── responses.py     # Envelope pattern
│   │       ├── errors.py        # Structured errors
│   │       └── exception_handlers.py
│   │
│   ├── modules/           # ✅ Business modules
│   │   ├── health/           # Health check module
│   │   │   ├── router.py        # HTTP layer
│   │   │   ├── service.py       # Business logic
│   │   │   └── schemas.py       # Pydantic models
│   │   └── chat/             # Chat module
│   │       ├── router.py
│   │       ├── service.py
│   │       └── schemas.py
│   │
│   └── main.py            # FastAPI app
│
├── app/                    # OLD structure (giữ lại reference)
├── test_integrations.py   # ✅ Test script
├── run.py                  # ✅ Run server
└── .env.example           # ✅ Updated config
```

---

## 🎯 Key Features

### 1. Provider Registry với Fallback

```python
from src.integrations import get_llm_registry

registry = get_llm_registry()

# Get LLM với automatic fallback
llm = registry.get_llm_with_fallback(["openai", "anthropic", "google"])

# Provider tự động fallback nếu primary fail
```

### 2. Config Theo Domain

```python
from src.core.config import get_settings

settings = get_settings()

# Access configs
print(settings.app.APP_NAME)
print(settings.llm.OPENAI_API_KEY)
print(settings.agent.AGENT_MAX_STEPS)
print(settings.security.JWT_SECRET)
```

### 3. Envelope Response Pattern

```json
{
  "success": true,
  "data": {...},
  "error": null,
  "meta": {...}
}
```

### 4. Structured Errors

```python
from src.core.common import NotFoundError, ValidationError

# Tự động convert sang API response
raise NotFoundError("User not found")
# → {"success": false, "error": {"code": "NOT_FOUND", ...}}
```

### 5. Router → Service Separation

```python
# Router: chỉ handle HTTP
@router.get("/users")
async def list_users(service: UserService = Depends()):
    result = await service.list_users()
    return success_response(data=result)

# Service: chứa business logic
class UserService:
    async def list_users(self):
        # Business logic here
        return users
```

---

## 📊 So Sánh: Trước vs Sau

### Trước (Old Structure)

```python
# app/main.py
from app.core.config import settings

if settings.OPENAI_API_KEY:
    llm = ChatOpenAI(...)
elif settings.ANTHROPIC_API_KEY:
    llm = ChatAnthropic(...)
# Manual fallback, no health check
```

### Sau (New Structure)

```python
# src/integrations/llm_registry.py
registry = LLMRegistry()
registry.register("openai", ...)
registry.register("anthropic", ...)

# Automatic fallback
llm = registry.get_llm_with_fallback()

# Health check
health = await checker.check_all()
```

---

## 🧪 Testing

### Test Integrations

```bash
python test_integrations.py
```

### Test API

```bash
# Health
curl http://localhost:8000/health

# Integrations (với LLM calls thật)
curl http://localhost:8000/health/integrations

# Chat
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

---

## ⚙️ Configuration

### .env File

```bash
# Application
APP_NAME="LangGraph FastAPI Demo"
APP_ENV=development
DEBUG=True

# LLM Providers (chọn ít nhất 1)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...

# LLM Settings
LLM_TEMPERATURE=0.0
LLM_MAX_TOKENS=4096
LLM_FALLBACK_ORDER=openai,anthropic,google

# Agent
AGENT_MAX_STEPS=10
INPUT_GUARD_ENABLED=True
OUTPUT_GUARD_ENABLED=True
```

---

## 🎓 Học Từ P-041

### Patterns Đã Áp Dụng

✅ **Provider Registry Pattern**
- Multiple LLM providers
- Automatic fallback
- Health checks

✅ **Config by Domain**
- app.py, llm.py, agent.py, security.py
- Unified settings object
- Validation

✅ **Envelope Response**
- Consistent API responses
- Success/error envelope
- Pagination support

✅ **Structured Errors**
- Error hierarchy
- Auto HTTP status codes
- FastAPI exception handlers

✅ **Separation of Concerns**
- Router → Service
- Config → Business logic
- HTTP → Domain logic

### Patterns Chưa Làm (Future)

⏳ **Repository Pattern**
- Cần database
- Data access layer

⏳ **Agent Components**
- Guard, LLM, Tools tách riêng
- Multi-flow pattern

⏳ **Observability**
- Langfuse tracing
- Metrics, logging

---

## 🐛 Troubleshooting

### "LLM Registry chưa được khởi tạo"

**Nguyên nhân**: Server chưa chạy startup  
**Fix**: Chạy qua `python run.py`, không import trực tiếp

### "Không có provider nào available"

**Nguyên nhân**: Chưa set API key  
**Fix**: Check `.env` file có ít nhất 1 key

### Test integrations báo "No API key"

**OK!** Đây là expected nếu không có key  
Thêm key vào `.env` để test thật

---

## 📚 Next Steps

### Immediate (Làm Ngay)

1. ✅ Test `python test_integrations.py`
2. ✅ Thêm API key vào `.env`
3. ✅ Chạy server `python run.py`
4. ✅ Test health endpoints
5. ✅ Xem Swagger UI: http://localhost:8000/docs

### Short Term (1-2 tuần)

6. ⏳ Refactor `app/agents/` → `src/agent/`
7. ⏳ Tích hợp agent vào chat service
8. ⏳ Thêm guardrails
9. ⏳ Add tests

### Long Term (1-2 tháng)

10. ⏳ Add database + Repository pattern
11. ⏳ Observability (Langfuse)
12. ⏳ Multi-agent flows
13. ⏳ Production deployment

---

## 💡 Key Takeaways

### Anh Cần Nhớ

1. **Test integrations trước**: `python test_integrations.py`
2. **Check health**: http://localhost:8000/health/integrations
3. **Fallback tự động**: Không cần lo nếu 1 provider fail
4. **Envelope everywhere**: Tất cả responses có `{success, data, error, meta}`
5. **Config tách biệt**: `settings.app`, `settings.llm`, `settings.agent`, `settings.security`

### Best Practices Áp Dụng

- ✅ Separation of concerns (Router/Service/Repository)
- ✅ Config by domain
- ✅ Structured error handling
- ✅ Provider abstraction
- ✅ Health checks
- ✅ Consistent responses
- ✅ Dependency injection

---

**Chúc anh test thành công! 🚀**

Có vấn đề gì cứ hỏi em!
