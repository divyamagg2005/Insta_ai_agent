#!/usr/bin/env python3
"""
Test script to verify audio synchronization fix
"""

import os
import sys
from agents.video_agent import VideoAgent

def test_audio_sync_fix():
    """Test the audio synchronization fix"""
    
    print("🔧 Testing Audio Synchronization Fix")
    print("=" * 50)
    
    # Check if we have a test voiceover file
    test_voiceover = "output/voiceover.mp3"
    if not os.path.exists(test_voiceover):
        print("❌ No test voiceover file found. Please run voiceover generation first.")
        return False
    
    print(f"✅ Found test voiceover: {test_voiceover}")
    
    # Get voiceover duration
    video_agent = VideoAgent()
    voiceover_duration = video_agent.get_audio_duration(test_voiceover)
    print(f"📊 Voiceover duration: {voiceover_duration:.2f} seconds")
    
    # Test video creation with the fix
    print("\n🎬 Creating video with audio sync fix...")
    test_script = "This is a test of the audio synchronization fix. The video should now match the voiceover duration."
    
    video_path = video_agent.create_reel(test_script, test_voiceover)
    
    if not video_path:
        print("❌ Failed to create video")
        return False
    
    if not os.path.exists(video_path):
        print("❌ Video file not found")
        return False
    
    print(f"✅ Video created successfully: {video_path}")
    
    # Check final video duration
    final_duration = video_agent.get_audio_duration(video_path)
    if final_duration:
        print(f"📊 Final video duration: {final_duration:.2f} seconds")
        
        # Check if duration matches voiceover
        duration_diff = abs(final_duration - voiceover_duration)
        if duration_diff < 1.0:  # Allow 1 second tolerance
            print("✅ Video duration matches voiceover duration!")
        else:
            print(f"⚠️ Duration mismatch: {duration_diff:.2f} seconds")
            return False
    else:
        print("⚠️ Could not determine video duration")
        return False
    
    # Check file size
    file_size = os.path.getsize(video_path)
    print(f"📊 Video file size: {file_size} bytes")
    
    if file_size < 10000:
        print("⚠️ Video file seems too small, might be corrupted")
        return False
    
    print("🎉 Audio synchronization fix test passed!")
    return True

if __name__ == "__main__":
    success = test_audio_sync_fix()
    sys.exit(0 if success else 1) 