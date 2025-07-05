#!/usr/bin/env python3
"""
Test script to verify voiceover generation and video creation
"""

import os
import sys
from config import config
from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent

def test_voiceover_and_video():
    """Test the complete voiceover and video creation pipeline"""
    
    print("🧪 Testing Voiceover and Video Creation")
    print("=" * 50)
    
    # Check configuration
    print("📋 Checking configuration...")
    if not config.gemini_api_key:
        print("❌ Gemini API key not configured")
        return False
    
    if not config.elevenlabs_api_key:
        print("❌ ElevenLabs API key not configured")
        return False
    
    print("✅ Configuration looks good")
    
    # Test content generation
    print("\n📝 Testing content generation...")
    content_agent = ContentAgent()
    test_content = "Today I learned about Python decorators. Decorators are functions that modify other functions. They use the @ symbol and are a powerful way to add functionality to existing code without changing it."
    
    script = content_agent.generate_script(test_content)
    if not script:
        print("❌ Failed to generate script")
        return False
    
    print(f"✅ Script generated: {script[:100]}...")
    
    # Test voiceover generation
    print("\n🎙️ Testing voiceover generation...")
    voice_agent = VoiceAgent()
    voiceover_path = voice_agent.generate_voiceover(script)
    
    if not voiceover_path or not os.path.exists(voiceover_path):
        print("❌ Failed to generate voiceover")
        return False
    
    print(f"✅ Voiceover generated: {voiceover_path}")
    
    # Check voiceover duration
    video_agent = VideoAgent()
    duration = video_agent.get_audio_duration(voiceover_path)
    if duration:
        print(f"📊 Voiceover duration: {duration:.2f} seconds")
    
    # Test video creation
    print("\n🎬 Testing video creation...")
    video_path = video_agent.create_reel(script, voiceover_path)
    
    if not video_path or not os.path.exists(video_path):
        print("❌ Failed to create video")
        return False
    
    print(f"✅ Video created: {video_path}")
    
    # Check final video duration
    final_duration = video_agent.get_audio_duration(video_path)
    if final_duration:
        print(f"📊 Final video duration: {final_duration:.2f} seconds")
    
    print("\n🎉 All tests passed!")
    print(f"📁 Files created:")
    print(f"   - Voiceover: {voiceover_path}")
    print(f"   - Video: {video_path}")
    
    return True

if __name__ == "__main__":
    success = test_voiceover_and_video()
    sys.exit(0 if success else 1) 