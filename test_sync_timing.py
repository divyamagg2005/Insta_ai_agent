#!/usr/bin/env python3
"""
Test script to demonstrate subtitle synchronization with voiceover timing
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.video_agent import VideoAgent, clean_script_for_subtitles

def test_synchronization():
    """Test subtitle synchronization with voiceover timing"""
    agent = VideoAgent()
    
    # Test with different script lengths and durations
    test_cases = [
        {
            'script': "This is a test script for synchronization",
            'duration': 10.0,
            'description': "Short script, 10 seconds"
        },
        {
            'script': "This is a longer test script that contains many more words to test how the synchronization works with different timing patterns and ensures that the subtitles appear at the right moments during the voiceover",
            'duration': 30.0,
            'description': "Long script, 30 seconds"
        },
        {
            'script': "Quick test",
            'duration': 5.0,
            'description': "Very short script, 5 seconds"
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\n=== Test Case {i+1}: {test_case['description']} ===")
        print(f"Script: {test_case['script']}")
        print(f"Duration: {test_case['duration']} seconds")
        
        # Clean the script
        cleaned = clean_script_for_subtitles(test_case['script'])
        print(f"Cleaned: {cleaned}")
        
        # Get subtitle chunks
        chunks = agent.split_script_for_subtitles(cleaned, test_case['duration'], words_per_chunk=5)
        
        print(f"\nSubtitle chunks ({len(chunks)} total):")
        total_time = 0
        for j, chunk in enumerate(chunks):
            duration = chunk['end_time'] - chunk['start_time']
            total_time += duration
            print(f"  Chunk {j+1}: '{chunk['text']}'")
            print(f"    Time: {chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s (duration: {duration:.2f}s)")
            print(f"    Words: {chunk['word_count']}")
        
        print(f"\nTiming Analysis:")
        print(f"  Total subtitle time: {total_time:.2f}s")
        print(f"  Voiceover duration: {test_case['duration']:.2f}s")
        print(f"  Coverage: {(total_time/test_case['duration'])*100:.1f}%")
        
        # Check for gaps or overlaps
        gaps = []
        overlaps = []
        for j in range(len(chunks)-1):
            current_end = chunks[j]['end_time']
            next_start = chunks[j+1]['start_time']
            
            if next_start > current_end:
                gap = next_start - current_end
                gaps.append(gap)
            elif next_start < current_end:
                overlap = current_end - next_start
                overlaps.append(overlap)
        
        if gaps:
            print(f"  Gaps found: {len(gaps)} (total gap time: {sum(gaps):.2f}s)")
        if overlaps:
            print(f"  Overlaps found: {len(overlaps)} (total overlap time: {sum(overlaps):.2f}s)")
        if not gaps and not overlaps:
            print(f"  Perfect timing: no gaps or overlaps")

def test_overflow_prevention():
    """Test overflow prevention with long text"""
    agent = VideoAgent()
    
    # Test with very long words that might overflow
    long_script = "This script contains supercalifragilisticexpialidocious words that are very long and might cause overflow issues in the subtitle system"
    duration = 20.0
    
    print(f"\n=== Overflow Prevention Test ===")
    print(f"Script: {long_script}")
    
    cleaned = clean_script_for_subtitles(long_script)
    chunks = agent.split_script_for_subtitles(cleaned, duration, words_per_chunk=5)
    
    print(f"\nChunks after overflow prevention:")
    for i, chunk in enumerate(chunks):
        from agents.video_agent import estimate_text_width
        estimated_width = estimate_text_width(chunk['text'], 50)
        print(f"  Chunk {i+1}: '{chunk['text']}' (estimated width: {estimated_width:.1f}px)")
        if estimated_width > 900:
            print(f"    WARNING: This chunk might still overflow!")

if __name__ == "__main__":
    test_synchronization()
    test_overflow_prevention() 