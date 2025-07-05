#!/usr/bin/env python3
"""
Test script to verify video creation
"""

import os
import sys
from config import config
from agents.video_agent import VideoAgent

def test_video_creation():
    """Test video creation with a simple voiceover"""
    
    print("🎬 Testing Video Creation")
    print("=" * 40)
    
    # Check if we have a test voiceover file
    test_voiceover = "output/voiceover.mp3"
    if not os.path.exists(test_voiceover):
        print("❌ No test voiceover file found. Please run voiceover generation first.")
        return False
    
    print(f"✅ Found test voiceover: {test_voiceover}")
    
    # Test video creation
    print("\n🎬 Creating video...")
    video_agent = VideoAgent()
    
    test_script = "This is a test of video creation with voiceover synchronization."
    
    video_path = video_agent.create_reel(test_script, test_voiceover)
    
    if not video_path:
        print("❌ Failed to create video")
        return False
    
    if not os.path.exists(video_path):
        print("❌ Video file not found")
        return False
    
    print(f"✅ Video created successfully: {video_path}")
    
    # Check file size
    file_size = os.path.getsize(video_path)
    print(f"📊 Video file size: {file_size} bytes")
    
    if file_size < 10000:
        print("⚠️ Video file seems too small, might be corrupted")
        return False
    
    # Check if video has audio
    print("\n🔊 Checking video audio...")
    duration = video_agent.get_audio_duration(video_path)
    if duration:
        print(f"📊 Video duration: {duration:.2f} seconds")
        if duration < 1.0:
            print("⚠️ Video duration seems too short")
            return False
    else:
        print("⚠️ Could not determine video duration")
    
    print("🎉 Video creation test passed!")
    return True

if __name__ == "__main__":
    success = test_video_creation()
    sys.exit(0 if success else 1) 