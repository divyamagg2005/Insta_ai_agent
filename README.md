# 🧠 BrainRot Learning - AI Agent for Instagram Reels

Transform your daily learning into viral Instagram Reels automatically using AI agents.

[![Docker](https://img.shields.io/badge/Docker-Ready-blue?logo=docker)](https://docs.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-green?logo=python)](https://python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20UI-red?logo=streamlit)](https://streamlit.io/)

## ✨ Features

- **AI Script Generation**: Gemini 2.5 Flash creates viral-style reel scripts
- **Voice Synthesis**: ElevenLabs generates natural-sounding voiceovers
- **Video Creation**: MoviePy combines audio with visuals
- **🎬 Synchronized Subtitles**: Smart subtitle system with customizable timing and appearance
- **Auto-Upload**: Instagrapi handles Instagram posting
- **Web Interface**: Streamlit UI for easy interaction
- **🔐 Privacy First**: Your credentials are never stored on our servers

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd learn2reel
   ```

2. **Deploy with one command:**
   ```bash
   chmod +x scripts/deploy.sh
   ./scripts/deploy.sh
   ```

3. **Access the application:**
   - Web UI: http://localhost:8501
   - Configure your API keys in the web interface

### Manual Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install FFmpeg:**
   - **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
   - **macOS:** `brew install ffmpeg`
   - **Windows:** Download from https://ffmpeg.org/

3. **Run the application:**
   ```bash
   # Web interface (recommended)
   streamlit run ui/streamlit_app.py
   
   # Configure your API keys in the web interface
   
   # Command line (after configuration)
   python main.py
   ```

## 🎬 Subtitle Features

Learn2Reel now includes a sophisticated subtitle system that:

- **Synchronizes with Audio**: Subtitles appear and disappear in sync with the voiceover
- **Smart Timing**: Automatically calculates optimal duration for each subtitle chunk
- **Customizable Appearance**: 
  - Font size (30-80px)
  - Font color (white, yellow, cyan, green)
  - Background opacity (0-100%)
  - Position (top, center, bottom)
- **Timing Control**:
  - Minimum duration per subtitle (0.5-3.0 seconds)
  - Maximum duration per subtitle (2.0-6.0 seconds)
  - Gap between subtitle chunks (0.0-1.0 seconds)

### Subtitle Configuration

**Via Web Interface:**
- Use the sidebar settings in the Streamlit app
- Real-time preview of subtitle settings
- Easy toggle to enable/disable subtitles

**Via Environment Variables:**
```bash
# Enable/disable subtitles
SUBTITLE_ENABLED=true

# Appearance settings
SUBTITLE_FONT_SIZE=50
SUBTITLE_FONT_COLOR=white
SUBTITLE_BACKGROUND_COLOR=black@0.7
SUBTITLE_POSITION_Y=h-text_h-50

# Timing settings
SUBTITLE_MIN_DURATION=1.0
SUBTITLE_MAX_DURATION=4.0
SUBTITLE_GAP=0.2
```

## 🔧 Setup Instructions

### 1. Get API Keys

**Gemini API:**
- Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Copy to your `.env` file

**ElevenLabs API:**
- Sign up at [ElevenLabs](https://elevenlabs.io/)
- Go to Profile → API Keys
- Create a new key and copy to `.env`

**Instagram:**
- Use your regular Instagram credentials
- Enable 2FA for better security

### 2. Voice Configuration

Get your ElevenLabs voice ID:
```python
from agents.voice_agent import VoiceAgent
voice_agent = VoiceAgent()
voices = voice_agent.get_available_voices()
print(voices)
```

## 📁 Project Structure

```
learn2reel/
├── agents/
│   ├── content_agent.py      # Script generation
│   ├── voice_agent.py        # Voice synthesis
│   ├── video_agent.py        # Video creation with subtitles
│   └── instagram_agent.py    # Instagram upload
├── ui/
│   └── streamlit_app.py      # Web interface with subtitle controls
├── output/                   # Generated files
├── assets/                   # Stock videos/images
├── main.py                   # CLI interface
├── test_subtitles.py         # Subtitle testing script
├── requirements.txt          # Dependencies
└── .env                      # API keys and subtitle config
```

## 🎯 Usage Examples

### CLI Usage
```bash
python main.py
# Enter your learning content when prompted
```

### Web Interface
```bash
streamlit run ui/streamlit_app.py
# Open browser and use the web interface
# Configure subtitle settings in the sidebar
```

### Programmatic Usage
```python
from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from config import config

# Configure subtitle settings
config.subtitle_enabled = True
config.subtitle_font_size = 60
config.subtitle_font_color = "yellow"
config.subtitle_position_y = "(h-text_h)/2"

# Generate script
content_agent = ContentAgent()
script = content_agent.generate_script("Today I learned about RAG in AI...")

# Generate voiceover
voice_agent = VoiceAgent()
voiceover_path = voice_agent.generate_voiceover(script)

# Create video with subtitles
video_agent = VideoAgent()
video_path = video_agent.create_reel(script, voiceover_path)
```

### Testing Subtitles
```bash
python test_subtitles.py
# Tests different subtitle configurations
```

## 🔐 Security Notes

- Never commit `.env` file to version control
- Use strong, unique passwords for Instagram
- Enable 2FA on all accounts
- Regularly rotate API keys

## 📦 Deployment

### Streamlit Cloud
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Add secrets in dashboard
4. Deploy

### Local Docker
```bash
docker build -t learn2reel .
docker run -p 8501:8501 learn2reel
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🐛 Troubleshooting

**Common Issues:**

1. **API Key Errors**
   - Check `.env` file exists and has correct keys
   - Verify API key validity

2. **Instagram Login Issues**
   - Try clearing session.json
   - Check username/password
   - Verify 2FA settings

3. **Video Generation Errors**
   - Ensure ffmpeg is installed
   - Check output directory permissions

4. **Subtitle Issues**
   - Verify FFmpeg supports drawtext filter
   - Check subtitle configuration values
   - Try different font sizes if text is too large/small

## 🆘 Support

- Create an issue on GitHub
- Check existing issues for solutions
- Join our Discord community

---

**Happy Learning and Creating! 🎬📚**
```