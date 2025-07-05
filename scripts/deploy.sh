#!/bin/bash

# Learn2Reel Deployment Script
echo "🚀 Deploying Learn2Reel..."

# Check if required files exist
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create it with your API keys."
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install/update requirements
echo "📥 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p output
mkdir -p assets

# Run tests
echo "🧪 Running tests..."
python -m pytest tests/ -v

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✅ Tests passed!"
else
    echo "❌ Tests failed. Please fix issues before deploying."
    exit 1
fi

# Start application
echo "🎬 Starting Learn2Reel..."
echo "Choose how to run:"
echo "1. CLI version (python main.py)"
echo "2. Web interface (streamlit run ui/streamlit_app.py)"
echo "3. Both (recommended for development)"

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        python main.py
        ;;
    2)
        streamlit run ui/streamlit_app.py
        ;;
    3)
        echo "🌐 Starting web interface..."
        streamlit run ui/streamlit_app.py &
        echo "⚡ Web interface started. CLI is also available."
        echo "🔗 Open http://localhost:8501 in your browser"
        ;;
    *)
        echo "❌ Invalid choice. Starting web interface by default..."
        streamlit run ui/streamlit_app.py
        ;;
esac

echo "🎉 Learn2Reel deployment complete!" 