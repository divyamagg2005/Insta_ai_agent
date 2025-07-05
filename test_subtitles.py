#!/usr/bin/env python3
"""
Test script for subtitle functionality
"""

import os
import sys
from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from config import config

def test_subtitles():
    """Test the subtitle functionality"""
    print("🎬 Testing Subtitle Functionality")
    print("=" * 50)
    
    # Sample learning content
    learning_content = """
    Today I learned about machine learning algorithms. 
    Supervised learning uses labeled data to train models. 
    Unsupervised learning finds patterns in unlabeled data. 
    Reinforcement learning learns through trial and error.
    """
    
    print(f"📝 Learning Content: {learning_content.strip()}")
    
    # Initialize agents
    content_agent = ContentAgent()
    voice_agent = VoiceAgent()
    video_agent = VideoAgent()
    
    try:
        # Step 1: Generate script
        print("\n🧠 Generating script...")
        script = content_agent.generate_script(learning_content, 25)
        
        if not script:
            print("❌ Failed to generate script")
            return
        
        print(f"✅ Script generated: {script}")
        
        # Step 2: Generate voiceover
        print("\n🎙️ Generating voiceover...")
        voiceover_path = voice_agent.generate_voiceover(script)
        
        if not voiceover_path:
            print("❌ Failed to generate voiceover")
            return
        
        print(f"✅ Voiceover generated: {voiceover_path}")
        
        # Step 3: Create video with subtitles
        print("\n🎬 Creating video with subtitles...")
        
        # Test with different subtitle settings
        subtitle_configs = [
            {
                "name": "Default Subtitles",
                "enabled": True,
                "font_size": 50,
                "font_color": "white",
                "position": "Bottom"
            },
            {
                "name": "Large Yellow Subtitles",
                "enabled": True,
                "font_size": 70,
                "font_color": "yellow",
                "position": "Center"
            },
            {
                "name": "No Subtitles",
                "enabled": False
            }
        ]
        
        for i, subtitle_config in enumerate(subtitle_configs):
            print(f"\n📹 Testing: {subtitle_config['name']}")
            
            # Update config
            config.subtitle_enabled = subtitle_config["enabled"]
            if subtitle_config["enabled"]:
                config.subtitle_font_size = subtitle_config["font_size"]
                config.subtitle_font_color = subtitle_config["font_color"]
                if subtitle_config["position"] == "Bottom":
                    config.subtitle_position_y = "h-text_h-50"
                elif subtitle_config["position"] == "Center":
                    config.subtitle_position_y = "(h-text_h)/2"
                else:
                    config.subtitle_position_y = "50"
            
            # Create video
            output_path = f"output/test_subtitles_{i+1}.mp4"
            video_path = video_agent.create_reel(script, voiceover_path, output_path)
            
            if video_path:
                print(f"✅ Video created: {video_path}")
                print(f"   - Subtitles: {'Enabled' if subtitle_config['enabled'] else 'Disabled'}")
                if subtitle_config["enabled"]:
                    print(f"   - Font Size: {subtitle_config['font_size']}")
                    print(f"   - Font Color: {subtitle_config['font_color']}")
                    print(f"   - Position: {subtitle_config['position']}")
            else:
                print(f"❌ Failed to create video")
        
        print("\n🎉 Subtitle test completed!")
        print("📁 Check the 'output' folder for generated videos")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_subtitles() 