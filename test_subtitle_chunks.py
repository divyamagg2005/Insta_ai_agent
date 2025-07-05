#!/usr/bin/env python3
"""
Test script to verify subtitle chunking with 5-6 words and overflow prevention
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.video_agent import VideoAgent, estimate_text_width, clean_script_for_subtitles

def test_subtitle_chunking():
    """Test the new subtitle chunking functionality"""
    agent = VideoAgent()
    
    # Test script with various lengths
    test_scripts = [
        "This is a short test script for testing subtitle functionality",
        "This is a much longer test script that contains many more words to test how the system handles longer text chunks and ensures that text does not overflow the video boundaries",
        "Short script",
        "This script has exactly five words for testing purposes",
        "This script has exactly six words for testing purposes now",
        "This is a very long script that should be split into multiple lines when the text becomes too long to fit on a single line of subtitles"
    ]
    
    for i, script in enumerate(test_scripts):
        print(f"\n=== Test {i+1} ===")
        print(f"Original script: {script}")
        
        # Clean the script
        cleaned = clean_script_for_subtitles(script)
        print(f"Cleaned script: {cleaned}")
        
        # Test subtitle chunking
        duration = 30.0  # 30 seconds
        chunks = agent.split_script_for_subtitles(cleaned, duration, words_per_chunk=5)
        
        print(f"Number of chunks: {len(chunks)}")
        for j, chunk in enumerate(chunks):
            estimated_width = estimate_text_width(chunk['text'], 50)  # font size 50
            print(f"  Chunk {j+1}: '{chunk['text']}' (width: {estimated_width:.1f}px, time: {chunk['start_time']:.1f}s-{chunk['end_time']:.1f}s)")
            
            # Test line splitting for long text
            if estimated_width > 900:
                lines = agent.split_text_into_lines(chunk['text'])
                print(f"    Split into {len(lines)} lines:")
                for k, line in enumerate(lines):
                    print(f"      Line {k+1}: '{line}'")

if __name__ == "__main__":
    test_subtitle_chunking() 