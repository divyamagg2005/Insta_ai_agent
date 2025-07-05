# 🧠 BrainRot Learning - AI-Powered Content Creation Platform

Transform your daily learning into viral Instagram Reels automatically using AI agents. Create engaging educational content with AI-generated scripts, natural voiceovers, and synchronized subtitles.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://docs.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-red?logo=streamlit)](https://streamlit.io/)
[![Deploy on HF Spaces](https://img.shields.io/badge/Deploy%20on-HF%20Spaces-orange)](https://huggingface.co/spaces)

## ✨ Features

- **🤖 AI Script Generation**: Gemini 2.5 Flash creates viral-style reel scripts from your learning content
- **🎙️ Voice Synthesis**: ElevenLabs generates natural-sounding voiceovers
- **🎬 Video Creation**: MoviePy combines audio with visuals and synchronized subtitles
- **📱 Auto-Upload**: Instagrapi handles Instagram posting (optional)
- **🌐 Web Interface**: Beautiful Streamlit UI for easy interaction
- **🔐 Privacy First**: Your credentials are never stored on our servers
- **⚙️ Customizable Subtitles**: Smart subtitle system with timing and appearance controls

## 🚀 Quick Start

### Option 1: Deploy on Hugging Face Spaces (Recommended)

1. **Fork this repository** to your GitHub account
2. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
3. **Choose "Docker"** as the SDK
4. **Connect your forked repository**
5. **Configure API keys** in the web interface once deployed

Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/learn2reel`

### Option 2: Local Development

#### Using Docker (Recommended)

```bash
# Clone the repository
git clone <your-repo-url>
cd learn2reel

# Build and run with Docker
docker build -t learn2reel .
docker run -p 8501:8501 learn2reel

# Or use docker-compose
docker-compose up --build
```

#### Manual Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd learn2reel

# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg
# Ubuntu/Debian: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
# Windows: Download from https://ffmpeg.org/

# Run the application
streamlit run ui/streamlit_app.py
```

## 🔧 Configuration

### Required API Keys

1. **Gemini API Key** (for AI script generation)
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it in the web interface

2. **ElevenLabs API Key** (for voice synthesis)
   - Sign up at [ElevenLabs](https://elevenlabs.io/)
   - Go to Profile → API Keys
   - Create a new key and add it in the web interface

3. **Instagram Credentials** (optional, for auto-upload)
   - Use your regular Instagram credentials
   - Enable 2FA for better security

### Configuration via Web Interface

Once you access the application:
1. Open the sidebar configuration panel
2. Enter your API keys
3. Configure subtitle settings
4. Save configuration

## 🎬 Subtitle Features

The platform includes a sophisticated subtitle system:

- **⏱️ Synchronized Timing**: Subtitles appear and disappear in sync with voiceover
- **🎨 Customizable Appearance**: 
  - Font size (30-80px)
  - Font color (white, yellow, cyan, green)
  - Background opacity (0-100%)
  - Position (top, center, bottom)
- **⚙️ Timing Control**:
  - Minimum duration per subtitle (0.5-3.0 seconds)
  - Maximum duration per subtitle (2.0-6.0 seconds)
  - Gap between subtitle chunks (0.0-1.0 seconds)

## 📁 Project Structure

```
learn2reel/
├── agents/
│   ├── content_agent.py      # AI script generation
│   ├── voice_agent.py        # Voice synthesis
│   ├── video_agent.py        # Video creation with subtitles
│   └── instagram_agent.py    # Instagram upload
├── ui/
│   └── streamlit_app.py      # Web interface
├── output/                   # Generated videos and audio
├── assets/                   # Stock videos and images
├── config.py                 # Configuration management
├── main.py                   # CLI interface
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
└── learn2reel_config.json  # Default configuration
```

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the application**:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

2. **Configure API keys** in the sidebar

3. **Enter your learning content** in the text area

4. **Customize subtitle settings** in the sidebar

5. **Generate and download** your Instagram reel

### Command Line Interface

```bash
python main.py
# Follow the prompts to enter content and generate reels
```

### Programmatic Usage

```python
from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from config import config

# Generate AI script
content_agent = ContentAgent()
script = content_agent.generate_script("Today I learned about machine learning...")

# Generate voiceover
voice_agent = VoiceAgent()
voiceover_path = voice_agent.generate_voiceover(script)

# Create video with subtitles
video_agent = VideoAgent()
video_path = video_agent.create_reel(script, voiceover_path)
```

## 🚀 Deployment Options

### 1. Hugging Face Spaces (Recommended for AI/ML projects)
- Perfect for showcasing AI projects
- Free tier available
- Automatic Docker builds
- Great for portfolio

### 2. Railway
- One-click deployment
- Auto-detects Dockerfile
- Good free tier

### 3. Render
- Free tier available
- Auto-scaling
- Custom domains

### 4. Google Cloud Run
- Production-ready
- Auto-scaling
- Pay-per-use

### 5. AWS ECS/Fargate
- Enterprise-grade
- Full control
- Scalable

## 🔐 Security & Privacy

- **API Keys**: Never stored on our servers, only in your local configuration
- **Instagram Credentials**: Optional, only used for auto-upload if configured
- **Data Privacy**: All processing happens locally or in your deployed container
- **No Data Collection**: We don't collect or store your content

## 🐛 Troubleshooting

### Common Issues

1. **API Key Errors**
   - Verify API keys are correct and active
   - Check API quotas and limits

2. **FFmpeg Issues**
   - Ensure FFmpeg is installed: `ffmpeg -version`
   - Check system dependencies

3. **Video Generation Errors**
   - Verify output directory permissions
   - Check available disk space

4. **Subtitle Issues**
   - Try different font sizes
   - Check subtitle timing settings
   - Verify FFmpeg drawtext filter support

### Debug Commands

```bash
# Test Docker build
docker build -t learn2reel .

# Test local installation
python -c "import streamlit; print('Streamlit OK')"

# Check FFmpeg
ffmpeg -version
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check this README and code comments
- **Community**: Join discussions in GitHub Discussions

---

**Transform your learning into viral content! 🎬📚✨**