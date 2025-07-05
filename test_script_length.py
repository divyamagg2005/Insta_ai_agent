#!/usr/bin/env python3
"""
Test script to verify content generation produces short scripts
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.content_agent import ContentAgent

def test_script_length():
    """Test that generated scripts are appropriately short"""
    
    content_agent = ContentAgent()
    
    # Test learning content
    test_content = "Today I learned about machine learning algorithms and how they can be used to predict user behavior in social media applications."
    
    print("Testing script generation...")
    print(f"Input content: {test_content}")
    print("-" * 50)
    
    # Generate script
    script = content_agent.generate_script(test_content, 30)
    
    if script:
        word_count = len(script.split())
        char_count = len(script)
        
        print(f"Generated script ({word_count} words, {char_count} chars):")
        print(f"'{script}'")
        print("-" * 50)
        print(f"Word count: {word_count}")
        print(f"Character count: {char_count}")
        print(f"Estimated duration: {word_count * 0.5:.1f} seconds (at 120 words/minute)")
        
        if word_count <= 80:
            print("✅ Script length is appropriate for 30-second reel")
        else:
            print("❌ Script is too long for 30-second reel")
    else:
        print("❌ Failed to generate script")

if __name__ == "__main__":
    test_script_length() 