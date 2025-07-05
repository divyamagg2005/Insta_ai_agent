#!/usr/bin/env python3
"""
Test script to verify subtitle filter creation works correctly
"""

from agents.video_agent import VideoAgent, escape_for_drawtext

def test_subtitle_filter():
    """Test subtitle filter creation"""
    va = VideoAgent()
    
    # Test script
    script = "LLM? Or LLM? Confused? One's AI magic, like ChatGPT. The other? A law degree! Master of Laws - Legum Magister. Two very different meanings. Did you know this? Let me know in the comments!"
    duration = 14.76
    
    print("Testing subtitle filter creation...")
    print(f"Script: {script}")
    print(f"Duration: {duration} seconds")
    print()
    
    # Test text escaping
    test_text = "Hello<<BR>>World! What's up?"
    escaped = escape_for_drawtext(test_text)
    print(f"Test escaping:")
    print(f"  Original: '{test_text}'")
    print(f"  Escaped:  '{escaped}'")
    print()
    
    # Test subtitle chunks
    chunks = va.split_script_for_subtitles(script, duration)
    print(f"Created {len(chunks)} subtitle chunks:")
    for i, chunk in enumerate(chunks):
        print(f"  Chunk {i}: '{chunk['text']}' ({chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s)")
    print()
    
    # Test filter creation
    filter_str = va.create_subtitle_filter(chunks)
    print(f"Filter string length: {len(filter_str)} characters")
    print(f"Filter string preview: {filter_str[:200]}...")
    print()
    
    # Test if filter string is valid (basic check)
    if "drawtext=" in filter_str and "text=" in filter_str:
        print("✅ Filter string appears to be valid")
    else:
        print("❌ Filter string appears to be invalid")
    
    return filter_str

if __name__ == "__main__":
    test_subtitle_filter() 