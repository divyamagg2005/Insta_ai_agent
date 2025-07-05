#!/usr/bin/env python3
"""
Learn2Reel Setup Script
First-time configuration and setup
"""

import os
import sys
import subprocess

def main():
    print("🎬 Learn2Reel Setup")
    print("=" * 30)
    
    # Check if Python dependencies are installed
    print("📦 Checking dependencies...")
    try:
        import streamlit
        import google.generativeai
        import elevenlabs
        print("✅ All dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    
    # Check if FFmpeg is available
    print("\n🎬 Checking FFmpeg...")
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg is available")
        else:
            print("❌ FFmpeg not found")
            print("Please install FFmpeg:")
            print("- Ubuntu/Debian: sudo apt-get install ffmpeg")
            print("- macOS: brew install ffmpeg")
            print("- Windows: Download from https://ffmpeg.org/")
    except FileNotFoundError:
        print("❌ FFmpeg not found")
        print("Please install FFmpeg:")
        print("- Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("- macOS: brew install ffmpeg")
        print("- Windows: Download from https://ffmpeg.org/")
    
    # Create necessary directories
    print("\n📁 Creating directories...")
    os.makedirs("output", exist_ok=True)
    os.makedirs("assets", exist_ok=True)
    print("✅ Directories created")
    
    # Check if configuration exists
    print("\n⚙️ Checking configuration...")
    if os.path.exists("learn2reel_config.json"):
        print("✅ Configuration file exists")
    else:
        print("⚠️ No configuration found")
        print("Run 'python main.py' to set up your configuration")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run 'python main.py' to configure your API keys")
    print("2. Run 'streamlit run ui/streamlit_app.py' for the web interface")
    print("3. Or run 'python main.py' for the command-line interface")

if __name__ == "__main__":
    main() 