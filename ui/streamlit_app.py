import streamlit as st
import os
import sys
from dotenv import load_dotenv
import time
import sys
import sys
print("Python executable:", sys.executable)



# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.instagram_agent import InstagramAgent
from config import config

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Learn2Reel",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .step-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .success-message {
        background: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎬 Learn2Reel</h1>
        <p>Transform your learning into engaging Instagram Reels automatically</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys status
        st.subheader("API Keys Status")
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        elevenlabs_key = os.getenv('ELEVENLABS_API_KEY')
        ig_username = os.getenv('IG_USERNAME')
        
        st.write(f"🤖 Gemini API: {'✅' if gemini_key else '❌'}")
        st.write(f"🎙️ ElevenLabs API: {'✅' if elevenlabs_key else '❌'}")
        st.write(f"📱 Instagram: {'✅' if ig_username else '❌'}")
        
        if not all([gemini_key, elevenlabs_key, ig_username]):
            st.error("Please configure your API keys in the .env file")
            st.stop()
        
        # Settings
        st.subheader("Settings")
        reel_duration = st.slider("Target Reel Duration (seconds)", 15, 30, 25)  # Target duration for script generation
        
        # Subtitle Settings
        st.subheader("🎬 Subtitle Settings")
        
        subtitle_enabled = st.checkbox("Enable Subtitles", value=config.subtitle_enabled, help="Add synchronized subtitles to the video")
        
        if subtitle_enabled:
            col1, col2 = st.columns(2)
            
            with col1:
                subtitle_font_size = st.slider("Font Size", 30, 80, config.subtitle_font_size, help="Size of subtitle text")
                subtitle_font_color = st.selectbox("Font Color", ["white", "yellow", "cyan", "green"], index=0, help="Color of subtitle text")
            
            with col2:
                subtitle_bg_opacity = st.slider("Background Opacity", 0.0, 1.0, 0.7, step=0.1, help="Opacity of subtitle background")
                subtitle_position = st.selectbox("Position", ["Bottom", "Center", "Top"], index=0, help="Position of subtitles on screen")
            
            # Timing settings
            st.subheader("⏱️ Timing Settings")
            col1, col2 = st.columns(2)
            
            with col1:
                subtitle_min_duration = st.slider("Min Duration (s)", 0.5, 3.0, config.subtitle_min_duration, step=0.1, help="Minimum duration for each subtitle")
                subtitle_gap = st.slider("Gap Between (s)", 0.0, 1.0, config.subtitle_gap, step=0.1, help="Gap between subtitle chunks")
            
            with col2:
                subtitle_max_duration = st.slider("Max Duration (s)", 2.0, 6.0, config.subtitle_max_duration, step=0.1, help="Maximum duration for each subtitle")
            
            # Update config with user settings
            config.subtitle_enabled = subtitle_enabled
            config.subtitle_font_size = subtitle_font_size
            config.subtitle_font_color = subtitle_font_color
            config.subtitle_background_color = f"black@{subtitle_bg_opacity}"
            config.subtitle_min_duration = subtitle_min_duration
            config.subtitle_max_duration = subtitle_max_duration
            config.subtitle_gap = subtitle_gap
            
            # Set position based on selection
            if subtitle_position == "Bottom":
                config.subtitle_position_y = "h-text_h-50"
            elif subtitle_position == "Center":
                config.subtitle_position_y = "(h-text_h)/2"
            else:  # Top
                config.subtitle_position_y = "50"
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📚 What did you learn today?")
        
        # Learning content input
        learning_content = st.text_area(
            "Enter your learning content:",
            placeholder="e.g., Today I learned about Retrieval-Augmented Generation (RAG) in AI. RAG combines the power of large language models with external knowledge bases to provide more accurate and up-to-date information...",
            height=150
        )
        
        # Generate button
        if st.button("🚀 Generate Reel", type="primary", use_container_width=True):
            if not learning_content.strip():
                st.error("Please enter some learning content")
                return
            
            # Initialize agents
            content_agent = ContentAgent()
            voice_agent = VoiceAgent()
            video_agent = VideoAgent()
            instagram_agent = InstagramAgent()
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Step 1: Generate script
                status_text.text("🧠 Generating script...")
                progress_bar.progress(20)
                
                script = content_agent.generate_script(learning_content, reel_duration)
                
                if not script:
                    st.error("Failed to generate script")
                    return
                
                # Step 2: Generate hashtags
                status_text.text("🏷️ Generating hashtags...")
                progress_bar.progress(40)
                
                hashtags = content_agent.generate_hashtags(learning_content)
                
                # Step 3: Generate voiceover
                status_text.text("🎙️ Generating voiceover...")
                progress_bar.progress(60)
                
                voiceover_path = voice_agent.generate_voiceover(script)
                
                if not voiceover_path:
                    st.error("Failed to generate voiceover")
                    return
                
                # Step 4: Create video
                status_text.text("🎬 Creating video...")
                progress_bar.progress(80)
                
                video_path = video_agent.create_reel(script, voiceover_path)
                
                if not video_path:
                    st.error("Failed to create video")
                    return
                
                # Complete - Video is ready for preview
                progress_bar.progress(100)
                status_text.text("✅ Reel generated successfully! Preview below.")
                
                # Store results in session state
                st.session_state.script = script
                st.session_state.hashtags = hashtags
                st.session_state.voiceover_path = voiceover_path
                st.session_state.video_path = video_path
                st.session_state.learning_content = learning_content
                st.session_state.reel_duration = reel_duration
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    with col2:
        st.header("📊 Preview & Actions")
        
        # Show results if available
        if hasattr(st.session_state, 'script'):
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.subheader("📝 Generated Script")
            st.write(st.session_state.script)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="step-card">', unsafe_allow_html=True)
            st.subheader("🏷️ Hashtags")
            st.write(st.session_state.hashtags)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Audio player
            if hasattr(st.session_state, 'voiceover_path') and os.path.exists(st.session_state.voiceover_path):
                st.subheader("🎙️ Voiceover")
                st.audio(st.session_state.voiceover_path)
            
            # Video player - This is the main preview
            if hasattr(st.session_state, 'video_path') and os.path.exists(st.session_state.video_path):
                st.subheader("🎬 Final Video Preview")
                st.video(st.session_state.video_path)
                
                # Action buttons
                st.subheader("🚀 Actions")
                
                # Upload to Instagram button
                if st.button("📤 Upload to Instagram", type="primary", use_container_width=True):
                    with st.spinner("Uploading to Instagram..."):
                        instagram_agent = InstagramAgent()
                        caption = f"Today I learned: {st.session_state.learning_content[:100]}..."
                        success = instagram_agent.upload_reel(
                            st.session_state.video_path, 
                            caption, 
                            st.session_state.hashtags
                        )
                        
                        if success:
                            st.success("✅ Successfully uploaded to Instagram!")
                        else:
                            st.error("❌ Failed to upload to Instagram")
                
                # Regenerate button
                if st.button("🔄 Regenerate Reel", use_container_width=True):
                    # Clear session state to allow regeneration
                    for key in ['script', 'hashtags', 'voiceover_path', 'video_path']:
                        if hasattr(st.session_state, key):
                            delattr(st.session_state, key)
                    st.rerun()
    
    # Instructions
    with st.expander("📖 How to use Learn2Reel"):
        st.markdown("""
        1. **Setup**: Configure your API keys in the `.env` file
        2. **Input**: Enter what you learned today in the text area
        3. **Configure**: Adjust subtitle settings in the sidebar (optional)
        4. **Generate**: Click the "Generate Reel" button
        5. **Preview**: Review the generated script, hashtags, and video
        6. **Upload**: Click "Upload to Instagram" when satisfied, or "Regenerate" to try again
        
        **Required API Keys:**
        - Gemini 2.5 Flash API key
        - ElevenLabs API key
        - Instagram username and password
        
        **Subtitle Features:**
        - Synchronized subtitles that appear and disappear with the audio
        - Customizable font size, color, and position
        - Adjustable timing for better readability
        """)

if __name__ == "__main__":
    main()