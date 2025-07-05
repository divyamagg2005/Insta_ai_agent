import streamlit as st
import os
import sys
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.instagram_agent import InstagramAgent
from config import config

# Page configuration
st.set_page_config(
    page_title="BrainRot Learning",
    page_icon="🧠",
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
        color: #333;
    }
    .welcome-card {
        background: #e3f2fd;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2196f3;
        margin: 1rem 0;
        color: #1565c0;
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
        <h1>🧠 BrainRot Learning</h1>
        <p>Transform your daily learning into viral Instagram Reels in seconds</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome message for new users
    if not config.gemini_api_key and not config.elevenlabs_api_key:
        st.markdown("""
        <div class="welcome-card">
            <h3>🚀 Welcome to BrainRot Learning!</h3>
            <p><strong>The Problem:</strong> People want to teach and share knowledge on social media, but they don't have time to create, edit, and post videos.</p>
            <p><strong>The Solution:</strong> Just type what you learned today, and we'll create a viral Instagram reel with subtitles and post it automatically!</p>
            <hr>
            <p><strong>🔐 Privacy First:</strong> Your credentials are never stored on our servers. All your secrets stay with you.</p>
            <p>To get started, configure your API keys in the sidebar:</p>
            <ul>
                <li><strong>Gemini API Key</strong> - For AI script generation</li>
                <li><strong>ElevenLabs API Key</strong> - For voice synthesis</li>
                <li><strong>Instagram Credentials</strong> - Optional, for auto-upload</li>
            </ul>
            <p>Get your API keys from:</p>
            <ul>
                <li><a href="https://makersuite.google.com/app/apikey" target="_blank" style="color: #1976d2;">Google AI Studio (Gemini)</a></li>
                <li><a href="https://elevenlabs.io/" target="_blank" style="color: #1976d2;">ElevenLabs</a></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Mission Statement
    st.markdown("""
    <div class="step-card">
        <h3>🎯 Our Mission</h3>
        <p><strong>How it works:</strong></p>
        <ol>
            <li>📚 Learn something new today</li>
            <li>✍️ Type what you learned in the box below</li>
            <li>🤖 AI creates a viral-style script with subtitles</li>
            <li>🎬 Automatically generates and posts to Instagram</li>
        </ol>
        <p><strong>No more excuses!</strong> Share your knowledge with the world in seconds.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys status
        st.subheader("API Keys Status")
        
        gemini_key = config.gemini_api_key
        elevenlabs_key = config.elevenlabs_api_key
        ig_username = config.ig_username
        
        st.write(f"🤖 Gemini API: {'✅' if gemini_key else '❌'}")
        st.write(f"🎙️ ElevenLabs API: {'✅' if elevenlabs_key else '❌'}")
        st.write(f"📱 Instagram: {'✅' if ig_username else '❌'}")
        
        # Credential input forms
        # Configuration management
        if not all([gemini_key, elevenlabs_key]):
            st.error("Please configure your API keys below")
            
            with st.expander("🔑 Configure API Keys", expanded=True):
                st.markdown("**Get your API keys from:**")
                st.markdown("- [Gemini](https://makersuite.google.com/app/apikey)")
                st.markdown("- [ElevenLabs](https://elevenlabs.io/)")
                
                # API Keys input
                new_gemini_key = st.text_input(
                    "Gemini API Key",
                    value=gemini_key,
                    type="password",
                    help="Enter your Gemini API key"
                )
                
                new_elevenlabs_key = st.text_input(
                    "ElevenLabs API Key", 
                    value=elevenlabs_key,
                    type="password",
                    help="Enter your ElevenLabs API key"
                )
                
                # Instagram credentials (optional)
                st.markdown("**Instagram (Optional - for auto-upload):**")
                new_ig_username = st.text_input(
                    "Instagram Username",
                    value=ig_username,
                    help="Leave blank if you don't want auto-upload"
                )
                
                new_ig_password = st.text_input(
                    "Instagram Password",
                    value=config.ig_password,
                    type="password",
                    help="Leave blank if you don't want auto-upload"
                )
                
                # Save button
                if st.button("💾 Save Configuration", type="primary"):
                    if new_gemini_key and new_elevenlabs_key:
                        config.gemini_api_key = new_gemini_key
                        config.elevenlabs_api_key = new_elevenlabs_key
                        config.ig_username = new_ig_username
                        config.ig_password = new_ig_password
                        
                        if config.save_config():
                            st.success("✅ Configuration saved successfully!")
                            st.rerun()
                        else:
                            st.error("❌ Failed to save configuration")
                    else:
                        st.error("❌ Gemini and ElevenLabs API keys are required")
        else:
            # Show configuration management for users who already have credentials
            with st.expander("⚙️ Manage Configuration"):
                st.markdown("**Current API Keys:**")
                st.markdown(f"🤖 Gemini API: ✅ Configured")
                st.markdown(f"🎙️ ElevenLabs API: ✅ Configured")
                st.markdown(f"📱 Instagram: {'✅ Configured' if ig_username else '❌ Not configured'}")
                
                # Update credentials
                st.markdown("**Update Credentials:**")
                new_gemini_key = st.text_input(
                    "Update Gemini API Key",
                    value="",
                    type="password",
                    help="Leave blank to keep current"
                )
                
                new_elevenlabs_key = st.text_input(
                    "Update ElevenLabs API Key", 
                    value="",
                    type="password",
                    help="Leave blank to keep current"
                )
                
                new_ig_username = st.text_input(
                    "Update Instagram Username",
                    value="",
                    help="Leave blank to keep current"
                )
                
                new_ig_password = st.text_input(
                    "Update Instagram Password",
                    value="",
                    type="password",
                    help="Leave blank to keep current"
                )
                
                # Update button
                if st.button("🔄 Update Configuration"):
                    updated = False
                    if new_gemini_key:
                        config.gemini_api_key = new_gemini_key
                        updated = True
                    if new_elevenlabs_key:
                        config.elevenlabs_api_key = new_elevenlabs_key
                        updated = True
                    if new_ig_username:
                        config.ig_username = new_ig_username
                        updated = True
                    if new_ig_password:
                        config.ig_password = new_ig_password
                        updated = True
                    
                    if updated and config.save_config():
                        st.success("✅ Configuration updated successfully!")
                        st.rerun()
                    elif updated:
                        st.error("❌ Failed to save configuration")
                    else:
                        st.info("ℹ️ No changes to save")
        
        if not all([gemini_key, elevenlabs_key]):
            st.stop()
        
        # Settings
        st.subheader("Settings")
        reel_duration = st.slider("Target Reel Duration (seconds)", 15, 30, 25)  # Target duration for script generation
    
    # Main content area
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
    
    # Preview & Actions section
    if hasattr(st.session_state, 'script'):
        st.header("📊 Preview & Actions")
        
        # Show results if available
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