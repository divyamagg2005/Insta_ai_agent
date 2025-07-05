#!/usr/bin/env python3
"""
Test script to verify subtitle timing and processing
"""

import os
import sys
from config import config
from agents.video_agent import VideoAgent

def test_subtitle_timing():
    """Test subtitle timing and processing"""
    
    print("📝 Testing Subtitle Timing and Processing")
    print("=" * 50)
    
    # Test subtitle chunk generation
    print("\n📝 Testing subtitle chunk generation...")
    video_agent = VideoAgent()
    
    test_script = "This is a test of subtitle timing. We want to see if the subtitles appear and disappear correctly with the voiceover. Each chunk should be properly timed."
    test_duration = 10.0  # 10 seconds
    
    subtitle_chunks = video_agent.split_script_for_subtitles(test_script, test_duration)
    
    if not subtitle_chunks:
        print("❌ No subtitle chunks generated")
        return False
    
    print(f"✅ Generated {len(subtitle_chunks)} subtitle chunks:")
    for i, chunk in enumerate(subtitle_chunks):
        print(f"  Chunk {i+1}: '{chunk['text']}' ({chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s)")
    
    # Check timing
    print("\n⏱️ Checking timing...")
    total_duration = 0
    for chunk in subtitle_chunks:
        chunk_duration = chunk['end_time'] - chunk['start_time']
        total_duration += chunk_duration
        print(f"  Chunk duration: {chunk_duration:.2f}s")
    
    print(f"📊 Total subtitle duration: {total_duration:.2f}s")
    print(f"📊 Target duration: {test_duration:.2f}s")
    
    if abs(total_duration - test_duration) > 2.0:
        print("⚠️ Subtitle duration doesn't match target duration")
        return False
    
    # Test subtitle filter generation
    print("\n🎬 Testing subtitle filter generation...")
    if len(subtitle_chunks) > 0:
        first_chunk = subtitle_chunks[0]
        print(f"First chunk text: '{first_chunk['text']}'")
        print(f"First chunk timing: {first_chunk['start_time']:.2f}s - {first_chunk['end_time']:.2f}s")
    
    print("🎉 Subtitle timing test passed!")
    return True

if __name__ == "__main__":
    success = test_subtitle_timing()
    sys.exit(0 if success else 1) 