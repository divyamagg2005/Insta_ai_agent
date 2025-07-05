#!/usr/bin/env python3
"""
Test script to verify conditional text filter approach for FFmpeg subtitles
"""

import subprocess
import os
from agents.video_agent import VideoAgent

def test_conditional_filter():
    """Test conditional text filter approach for FFmpeg subtitles"""
    va = VideoAgent()
    
    # Check if we have a test video
    test_video = "output/final_reel.mp4"
    if not os.path.exists(test_video):
        print(f"Test video not found: {test_video}")
        print("Please run the main app first to generate a test video")
        return False
    
    # Test script
    script = "LLM? Or LLM? Confused? One's AI magic, like ChatGPT. The other? A law degree! Master of Laws - Legum Magister. Two very different meanings. Did you know this? Let me know in the comments!"
    duration = 14.76
    
    print("Testing conditional text filter approach for FFmpeg subtitles...")
    print(f"Input video: {test_video}")
    print(f"Script: {script}")
    print(f"Duration: {duration} seconds")
    print()
    
    # Create subtitle chunks
    chunks = va.split_script_for_subtitles(script, duration)
    print(f"Created {len(chunks)} subtitle chunks")
    
    # Create filter string
    filter_str = va.create_subtitle_filter(chunks)
    print(f"Filter string length: {len(filter_str)} characters")
    
    # Test FFmpeg command with conditional filter
    output_path = "output/test_subtitles_conditional.mp4"
    cmd = [
        "ffmpeg", "-y",
        "-i", test_video,
        "-vf", filter_str,
        "-map", "0:v:0", "-map", "0:a:0",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    
    print("Running FFmpeg command with conditional filter...")
    print(f"Command: {' '.join(cmd[:4])} [filter] {' '.join(cmd[5:])}")
    print()
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ FFmpeg subtitle command with conditional filter completed successfully!")
        print(f"Output video: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg subtitle command with conditional filter failed!")
        print(f"Error code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        return False

if __name__ == "__main__":
    test_conditional_filter() 