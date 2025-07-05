#!/bin/bash

# Learn2Reel Setup Script
echo "🎬 Setting up Learn2Reel..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )(\d+\.\d+)')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.8 or higher is required. Current version: $python_version"
    exit 1
fi

echo "✅ Python version: $python_version"

# Install system dependencies
echo "🔧 Installing system dependencies..."
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    sudo apt-get update
    sudo apt-get install -y ffmpeg
elif [[ "$OSTYPE" == "darwin"* ]]; then
    brew install ffmpeg
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Please install ffmpeg manually on Windows"
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python requirements..."
pip install -r requirements.txt

# Create directories
echo "📁 Creating directories..."
mkdir -p output
mkdir -p assets
mkdir -p logs

# Create .env template if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << EOL
# Learn2Reel Configuration
# Copy this file and fill in your actual API keys

# Gemini API (Get from: https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=your_gemini_key_here

# ElevenLabs API (Get from: https://elevenlabs.io/app/speech-synthesis)
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=your_voice_id_here

# Instagram Credentials
IG_USERNAME=your_instagram_username
IG_PASSWORD=your_instagram_password

# Optional: Video Settings
VIDEO_WIDTH=1080
VIDEO_HEIGHT=1920
VIDEO_FPS=24
DEFAULT_REEL_DURATION=30

# Optional: Voice Settings
VOICE_STABILITY=0.5
VOICE_SIMILARITY_BOOST=0.75

# Optional: Paths
OUTPUT_DIR=output
ASSETS_DIR=assets
EOL
    echo "✅ .env template created. Please fill in your API keys."
else
    echo "✅ .env file already exists."
fi

# Create sample asset
echo "🎨 Creating sample asset..."
# Here you could download a sample video or create a placeholder

# Make scripts executable
chmod +x scripts/*.sh

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Fill in your API keys in the .env file"
echo "2. Run: ./scripts/deploy.sh"
echo "3. Or run directly: python main.py"
echo ""
echo "For web interface: streamlit run ui/streamlit_app.py" 