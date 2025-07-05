#!/usr/bin/env python3
"""
Test script to verify voiceover-synced subtitle timing
"""

import subprocess
import os
from agents.video_agent import VideoAgent, clean_script_for_subtitles

def test_voiceover_sync():
    """Test voiceover-synced subtitle timing"""
    va = VideoAgent()
    
    # Use an existing video file from assets
    test_video = "assets/1.mp4"
    if not os.path.exists(test_video):
        print(f"Test video not found: {test_video}")
        return False
    
    # Test script with special characters (shorter for testing)
    script = "LLM? Or LLM? Confused? One's AI magic, like ChatGPT. The other? A law degree!"
    duration = 8.0  # Shorter duration for testing
    
    print("Testing voiceover-synced subtitle timing...")
    print(f"Input video: {test_video}")
    print(f"Original script: {script}")
    
    # Test script cleaning
    cleaned_script = clean_script_for_subtitles(script)
    print(f"Cleaned script: {cleaned_script}")
    print(f"Duration: {duration} seconds")
    
    # Calculate timing details
    words = cleaned_script.split()
    total_words = len(words)
    words_per_second = total_words / duration
    seconds_per_word = duration / total_words
    
    print(f"Total words: {total_words}")
    print(f"Words per second: {words_per_second:.2f}")
    print(f"Seconds per word: {seconds_per_word:.3f}")
    print()
    
    # Test the subtitle chunking with timing
    chunks = va.split_script_for_subtitles(script, duration)
    print(f"Created {len(chunks)} subtitle chunks:")
    for i, chunk in enumerate(chunks):
        word_count = len(chunk['text'].split())
        print(f"  Chunk {i+1}: '{chunk['text']}' ({word_count} words, {chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s)")
    print()
    
    # Test the add_subtitles method directly
    output_path = "output/test_subtitles_voiceover_sync.mp4"
    
    try:
        va.add_subtitles(test_video, script, output_path, duration)
        print("✅ Voiceover-synced subtitle approach completed successfully!")
        print(f"Output video: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Voiceover-synced subtitle approach failed: {e}")
        return False

if __name__ == "__main__":
    test_voiceover_sync() 