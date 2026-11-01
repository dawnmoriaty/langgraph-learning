#!/bin/bash
# Setup script

echo "Setting up LangGraph FastAPI Demo..."

# Activate venv if exists
if [ -d "venv" ]; then
    echo "Activating venv..."
    source venv/bin/activate
else
    echo "Creating venv..."
    python -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env"
echo "2. Add your API keys to .env"
echo "3. Run: python test_integrations.py"
echo "4. Run: python run.py"
