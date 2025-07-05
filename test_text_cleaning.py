#!/usr/bin/env python3
"""
Test script to verify text cleaning removes formatting characters
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.voice_agent import VoiceAgent

def test_text_cleaning():
    """Test that text cleaning removes formatting characters"""
    
    voice_agent = VoiceAgent()
    
    # Test scripts with various formatting characters
    test_scripts = [
        "This is a *bold* statement with #hashtags and _underscores_",
        "Here's some ~strikethrough~ text with `code` formatting",
        "Normal text with #learning #education #tech hashtags",
        "Text with *emphasis* and **double emphasis**",
        "Clean text without any formatting characters"
    ]
    
    print("Testing text cleaning...")
    print("=" * 60)
    
    for i, script in enumerate(test_scripts, 1):
        print(f"\nTest {i}:")
        print(f"Original: '{script}'")
        
        cleaned = voice_agent.clean_script_text(script)
        print(f"Cleaned:  '{cleaned}'")
        
        # Check if cleaning worked
        has_formatting = any(char in script for char in ['*', '#', '_', '~', '`'])
        if has_formatting and len(cleaned) < len(script):
            print("✅ Formatting characters removed successfully")
        elif not has_formatting:
            print("✅ No formatting characters to remove")
        else:
            print("❌ Formatting characters not properly removed")

if __name__ == "__main__":
    test_text_cleaning() 