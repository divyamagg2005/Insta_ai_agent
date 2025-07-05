#!/usr/bin/env python3
"""
Simple test to verify voiceover generation
"""

import os
import sys
from config import config
from agents.voice_agent import VoiceAgent

def test_voiceover():
    """Test voiceover generation"""
    
    print("🎙️ Testing Voiceover Generation")
    print("=" * 40)
    
    # Check configuration
    print("📋 Checking ElevenLabs API key...")
    if not config.elevenlabs_api_key:
        print("❌ ElevenLabs API key not configured")
        return False
    
    print("✅ API key found")
    
    # Test voiceover generation
    print("\n🎙️ Generating voiceover...")
    voice_agent = VoiceAgent()
    
    test_script = "Hello, this is a test of the voiceover generation. I hope this works properly."
    
    voiceover_path = voice_agent.generate_voiceover(test_script)
    
    if not voiceover_path:
        print("❌ Failed to generate voiceover")
        return False
    
    if not os.path.exists(voiceover_path):
        print("❌ Voiceover file not found")
        return False
    
    print(f"✅ Voiceover generated successfully: {voiceover_path}")
    
    # Check file size
    file_size = os.path.getsize(voiceover_path)
    print(f"📊 File size: {file_size} bytes")
    
    if file_size < 1000:
        print("⚠️ File seems too small, might be empty")
        return False
    
    print("🎉 Voiceover test passed!")
    return True

if __name__ == "__main__":
    success = test_voiceover()
    sys.exit(0 if success else 1) 