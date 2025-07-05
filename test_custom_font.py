#!/usr/bin/env python3
"""
Test script to verify custom Montserrat font for subtitles
"""

import subprocess
import os
from agents.video_agent import VideoAgent, clean_script_for_subtitles

def test_custom_font():
    """Test custom Montserrat font for subtitles"""
    va = VideoAgent()
    
    # Use an existing video file from assets
    test_video = "assets/1.mp4"
    if not os.path.exists(test_video):
        print(f"Test video not found: {test_video}")
        return False
    
    # Check if font file exists
    font_path = "assets/Montserrat-SemiBold.ttf"
    if not os.path.exists(font_path):
        print(f"Font file not found: {font_path}")
        return False
    
    print(f"✅ Font file found: {font_path}")
    
    # Test script with special characters (shorter for testing)
    script = "LLM? Or LLM? Confused? One's AI magic, like ChatGPT. The other? A law degree!"
    duration = 8.0  # Shorter duration for testing
    
    print("Testing custom Montserrat font for subtitles...")
    print(f"Input video: {test_video}")
    print(f"Original script: {script}")
    
    # Test script cleaning
    cleaned_script = clean_script_for_subtitles(script)
    print(f"Cleaned script: {cleaned_script}")
    print(f"Duration: {duration} seconds")
    print()
    
    # Test the subtitle chunking with timing
    chunks = va.split_script_for_subtitles(script, duration)
    print(f"Created {len(chunks)} subtitle chunks:")
    for i, chunk in enumerate(chunks):
        word_count = len(chunk['text'].split())
        print(f"  Chunk {i+1}: '{chunk['text']}' ({word_count} words, {chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s)")
    print()
    
    # Test the add_subtitles method directly
    output_path = "output/test_subtitles_custom_font.mp4"
    
    try:
        va.add_subtitles(test_video, script, output_path, duration)
        print("✅ Custom font subtitle approach completed successfully!")
        print(f"Output video: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Custom font subtitle approach failed: {e}")
        return False

if __name__ == "__main__":
    test_custom_font() 