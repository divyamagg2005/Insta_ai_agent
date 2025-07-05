#!/usr/bin/env python3
"""
Test script to verify filter file approach for FFmpeg subtitles
"""

import subprocess
import os
from agents.video_agent import VideoAgent

def test_filter_file_approach():
    """Test filter file approach for FFmpeg subtitles"""
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
    
    print("Testing filter file approach for FFmpeg subtitles...")
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
    
    # Create filter file
    filter_file_path = "output/test_subtitle_filter.txt"
    try:
        with open(filter_file_path, 'w', encoding='utf-8') as f:
            f.write(filter_str)
        print(f"Created filter file: {filter_file_path}")
        
        # Test FFmpeg command with filter file
        output_path = "output/test_subtitles_filter_file.mp4"
        cmd = [
            "ffmpeg", "-y",
            "-i", test_video,
            "-vf", f"filter_script={filter_file_path}",
            "-map", "0:v:0", "-map", "0:a:0",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        print("Running FFmpeg command with filter file...")
        print(f"Command: {' '.join(cmd[:4])} filter_script={filter_file_path} {' '.join(cmd[6:])}")
        print()
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ FFmpeg subtitle command with filter file completed successfully!")
        print(f"Output video: {output_path}")
        
        # Clean up filter file
        if os.path.exists(filter_file_path):
            os.remove(filter_file_path)
            print(f"Cleaned up filter file: {filter_file_path}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print("❌ FFmpeg subtitle command with filter file failed!")
        print(f"Error code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        
        # Clean up filter file
        if os.path.exists(filter_file_path):
            os.remove(filter_file_path)
        
        return False
    except Exception as e:
        print(f"❌ Error creating or using filter file: {e}")
        
        # Clean up filter file
        if os.path.exists(filter_file_path):
            os.remove(filter_file_path)
        
        return False

if __name__ == "__main__":
    test_filter_file_approach() 