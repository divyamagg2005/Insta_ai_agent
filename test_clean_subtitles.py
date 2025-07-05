#!/usr/bin/env python3
"""
Test script to verify clean subtitle approach with 3-word chunks
"""

import subprocess
import os
from agents.video_agent import VideoAgent, clean_script_for_subtitles

def test_clean_subtitles():
    """Test clean subtitle approach with 3-word chunks"""
    va = VideoAgent()
    
    # Check if we have a test video
    test_video = "output/final_reel.mp4"
    if not os.path.exists(test_video):
        print(f"Test video not found: {test_video}")
        print("Please run the main app first to generate a test video")
        return False
    
    # Test script with special characters
    script = "LLM? Or LLM? Confused? One's AI magic, like ChatGPT. The other? A law degree! Master of Laws - Legum Magister. Two very different meanings. Did you know this? Let me know in the comments!"
    duration = 14.76
    
    print("Testing clean subtitle approach with 3-word chunks...")
    print(f"Input video: {test_video}")
    print(f"Original script: {script}")
    
    # Test script cleaning
    cleaned_script = clean_script_for_subtitles(script)
    print(f"Cleaned script: {cleaned_script}")
    print(f"Duration: {duration} seconds")
    print()
    
    # Test the add_subtitles method directly
    output_path = "output/test_subtitles_clean.mp4"
    
    try:
        va.add_subtitles(test_video, script, output_path, duration)
        print("✅ Clean subtitle approach completed successfully!")
        print(f"Output video: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Clean subtitle approach failed: {e}")
        return False

if __name__ == "__main__":
    test_clean_subtitles() 