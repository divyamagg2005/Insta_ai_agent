"""
Learn2Reel - Command Line Interface
Automate Instagram Reels creation from learning content
"""

import os
import sys
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.instagram_agent import InstagramAgent
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('learn2reel.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def main():
    print("🧠 BrainRot Learning - AI Agent for Instagram Reels")
    print("=" * 50)
    
    try:
        # Check if configuration exists
        if not os.path.exists(config.config_file):
            print("❌ No configuration found.")
            print("Please use the web interface to configure your API keys:")
            print("   streamlit run ui/streamlit_app.py")
            return
        
        # Validate configuration
        errors = config.validate()
        
        if errors:
            print("❌ Configuration errors found:")
            for error in errors:
                print(f"  - {error}")
            print("\nPlease use the web interface to update your configuration:")
            print("   streamlit run ui/streamlit_app.py")
            return
        
        logger.info("Configuration validated successfully")
        
        # Check optional Instagram credentials
        if not (config.ig_username and config.ig_password):
            print("⚠️ Instagram credentials not configured - auto-upload will be disabled")
            logger.warning("Instagram credentials not configured")
    except Exception as e:
        print(f"❌ Error during initialization: {e}")
        logger.error(f"Initialization error: {e}")
        return
    
    # Initialize agents
    content_agent = ContentAgent()
    voice_agent = VoiceAgent()
    video_agent = VideoAgent()
    instagram_agent = InstagramAgent()
    
    # Get user input
    print("\n📝 What did you learn today?")
    learning_content = input("Enter your learning content: ")
    
    if not learning_content.strip():
        print("❌ Please provide some learning content")
        return
    
    print("\n🧠 Generating script...")
    script = content_agent.generate_script(learning_content)
    
    if not script:
        print("❌ Failed to generate script")
        return
    
    print(f"✅ Script generated:\n{script[:100]}...")
    
    # Generate hashtags
    print("\n🏷️ Generating hashtags...")
    hashtags = content_agent.generate_hashtags(learning_content)
    print(f"✅ Hashtags: {hashtags}")
    
    # Generate voiceover
    print("\n🎙️ Generating voiceover...")
    voiceover_path = voice_agent.generate_voiceover(script)
    
    if not voiceover_path:
        print("❌ Failed to generate voiceover")
        return
    
    print(f"✅ Voiceover generated: {voiceover_path}")
    
    # Create video
    print("\n🎬 Creating video...")
    video_path = video_agent.create_reel(script, voiceover_path)
    
    if not video_path:
        print("❌ Failed to create video")
        return
    
    print(f"✅ Video created: {video_path}")
    
    # Ask if user wants to upload to Instagram
    upload_choice = input("\n📲 Upload to Instagram? (y/n): ").lower().strip()
    
    if upload_choice == 'y':
        print("\n📤 Uploading to Instagram...")
        
        # Create caption
        caption = f"Today I learned: {learning_content[:100]}..."
        
        success = instagram_agent.upload_reel(video_path, caption, hashtags)
        
        if success:
            print("✅ Successfully uploaded to Instagram!")
        else:
            print("❌ Failed to upload to Instagram")
    
    print("\n🎉 Learn2Reel process completed!")
    print(f"📁 Files created:")
    print(f"   - Script: Generated")
    print(f"   - Voiceover: {voiceover_path}")
    print(f"   - Video: {video_path}")

if __name__ == "__main__":
    main()