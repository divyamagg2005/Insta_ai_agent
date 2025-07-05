"""
Learn2Reel - Command Line Interface
Automate Instagram Reels creation from learning content
"""

import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.instagram_agent import InstagramAgent

def main():
    print("🎬 Learn2Reel - AI Agent for Instagram Reels")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ['GEMINI_API_KEY', 'ELEVENLABS_API_KEY', 'IG_USERNAME', 'IG_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
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