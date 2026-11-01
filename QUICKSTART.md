# Quick Start Guide

## Step 1: Setup Virtual Environment

```bash
# Create and activate venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

## Step 2: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Or use the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

## Step 3: Configure API Keys

```bash
# Copy example
cp .env.example .env

# Edit .env and add at least ONE API key:
# OPENAI_API_KEY=sk-...
# or
# ANTHROPIC_API_KEY=sk-ant-...
# or
# GOOGLE_API_KEY=...
```

## Step 4: Test Integrations

```bash
python test_integrations.py
```

Expected output:
```
===========================================================
TESTING LLM INTEGRATIONS
===========================================================

Step 1: Initializing LLM Registry...

Step 2: Registered Providers
  * ✓ openai       - openai       (gpt-4o-mini)
    ✗ anthropic   - anthropic     (claude-3-5-sonnet-20241022)

Step 3: Health Check
   Overall Status: HEALTHY
   Healthy: 1/3
   ✓ openai       - OK (523ms)
   ⚠ anthropic   - No API key
```

## Step 5: Run Server

```bash
python run.py
```

Expected output:
```
Starting LangGraph FastAPI Demo Server (Refactored)

Server: http://0.0.0.0:8000
Docs: http://0.0.0.0:8000/docs
Health: http://0.0.0.0:8000/health

Press CTRL+C to stop
```

## Step 6: Test Endpoints

### Basic Health
```bash
curl http://localhost:8000/health
```

### Integration Health (with LLM tests)
```bash
curl http://localhost:8000/health/integrations
```

### Chat
```bash
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### Swagger UI
Open browser: http://localhost:8000/docs

## Troubleshooting

### "No module named 'uvicorn'"
```bash
pip install -r requirements.txt
```

### "No API key found"
Check `.env` file has at least one API key set.

### Syntax errors
Make sure all files are properly saved and no trailing characters.

## Next Steps

1. Explore API docs at `/docs`
2. Test all health endpoints
3. Check integration health
4. Read `REFACTORED_GUIDE.md` for details
5. Review code structure in `src/`
