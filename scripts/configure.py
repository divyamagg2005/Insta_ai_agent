#!/usr/bin/env python3
"""
Learn2Reel Configuration Manager
Standalone script for managing configuration
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config

def show_current_config():
    """Display current configuration"""
    config = Config()
    config.load_config()
    
    print("🎬 Current Configuration")
    print("=" * 30)
    
    # API Keys (masked)
    print(f"🤖 Gemini API: {'✅' if config.gemini_api_key else '❌'}")
    print(f"🎙️ ElevenLabs API: {'✅' if config.elevenlabs_api_key else '❌'}")
    print(f"📱 Instagram: {'✅' if config.ig_username else '❌'}")
    
    # Settings
    print(f"\n🎬 Subtitle Settings:")
    print(f"  Enabled: {config.subtitle_enabled}")
    print(f"  Font Size: {config.subtitle_font_size}")
    print(f"  Font Color: {config.subtitle_font_color}")
    
    print(f"\n📹 Video Settings:")
    print(f"  Resolution: {config.video_width}x{config.video_height}")
    print(f"  FPS: {config.video_fps}")
    
    print(f"\n🎙️ Voice Settings:")
    print(f"  Stability: {config.voice_stability}")
    print(f"  Similarity Boost: {config.voice_similarity_boost}")

def reset_config():
    """Reset configuration to defaults"""
    print("⚠️ This will reset all configuration to defaults.")
    confirm = input("Are you sure? (y/n): ").strip().lower()
    
    if confirm in ['y', 'yes']:
        config = Config()
        config.save_config()
        print("✅ Configuration reset to defaults")
    else:
        print("❌ Configuration reset cancelled")

def update_api_keys():
    """Update API keys"""
    config = Config()
    config.load_config()
    
    print("🔑 Update API Keys")
    print("=" * 20)
    
    print("Get your API keys from:")
    print("- Gemini: https://makersuite.google.com/app/apikey")
    print("- ElevenLabs: https://elevenlabs.io/")
    
    gemini_key = input("Enter Gemini API Key (leave blank to keep current): ").strip()
    if gemini_key:
        config.gemini_api_key = gemini_key
    
    elevenlabs_key = input("Enter ElevenLabs API Key (leave blank to keep current): ").strip()
    if elevenlabs_key:
        config.elevenlabs_api_key = elevenlabs_key
    
    ig_username = input("Enter Instagram Username (leave blank to keep current): ").strip()
    if ig_username:
        config.ig_username = ig_username
    
    ig_password = input("Enter Instagram Password (leave blank to keep current): ").strip()
    if ig_password:
        config.ig_password = ig_password
    
    if config.save_config():
        print("✅ Configuration updated successfully!")
    else:
        print("❌ Failed to save configuration")

def main():
    print("🎬 Learn2Reel Configuration Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Show current configuration")
        print("2. Update API keys")
        print("3. Reset to defaults")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            show_current_config()
        elif choice == '2':
            update_api_keys()
        elif choice == '3':
            reset_config()
        elif choice == '4':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 