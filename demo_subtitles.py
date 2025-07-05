#!/usr/bin/env python3
"""
Demo script for Learn2Reel subtitle functionality
"""

import os
import sys
from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from config import config

def demo_subtitle_features():
    """Demonstrate subtitle features with different configurations"""
    print("🎬 Learn2Reel Subtitle Demo")
    print("=" * 50)
    
    # Sample learning content
    learning_content = """
    Today I learned about artificial intelligence and machine learning. 
    AI is transforming how we work and live. 
    Machine learning algorithms can predict patterns in data. 
    Deep learning uses neural networks to solve complex problems.
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
        
        # Step 3: Create videos with different subtitle configurations
        print("\n🎬 Creating videos with different subtitle styles...")
        
        subtitle_demos = [
            {
                "name": "Classic White Subtitles",
                "description": "Traditional white text with black background",
                "config": {
                    "enabled": True,
                    "font_size": 50,
                    "font_color": "white",
                    "background_color": "black@0.7",
                    "position": "Bottom"
                }
            },
            {
                "name": "Bold Yellow Subtitles",
                "description": "High contrast yellow text for better visibility",
                "config": {
                    "enabled": True,
                    "font_size": 60,
                    "font_color": "yellow",
                    "background_color": "black@0.8",
                    "position": "Center"
                }
            },
            {
                "name": "Cyan Subtitles",
                "description": "Modern cyan text with semi-transparent background",
                "config": {
                    "enabled": True,
                    "font_size": 45,
                    "font_color": "cyan",
                    "background_color": "black@0.6",
                    "position": "Bottom"
                }
            },
            {
                "name": "No Subtitles",
                "description": "Video without any text overlays",
                "config": {
                    "enabled": False
                }
            }
        ]
        
        for i, demo in enumerate(subtitle_demos):
            print(f"\n📹 Demo {i+1}: {demo['name']}")
            print(f"   Description: {demo['description']}")
            
            # Update config
            config.subtitle_enabled = demo["config"]["enabled"]
            if demo["config"]["enabled"]:
                config.subtitle_font_size = demo["config"]["font_size"]
                config.subtitle_font_color = demo["config"]["font_color"]
                config.subtitle_background_color = demo["config"]["background_color"]
                
                # Set position
                if demo["config"]["position"] == "Bottom":
                    config.subtitle_position_y = "h-text_h-50"
                elif demo["config"]["position"] == "Center":
                    config.subtitle_position_y = "(h-text_h)/2"
                else:
                    config.subtitle_position_y = "50"
            
            # Create video
            output_path = f"output/demo_subtitles_{i+1}.mp4"
            video_path = video_agent.create_reel(script, voiceover_path, output_path)
            
            if video_path:
                print(f"   ✅ Video created: {video_path}")
                if demo["config"]["enabled"]:
                    print(f"   📝 Font: {demo['config']['font_color']}, Size: {demo['config']['font_size']}")
                    print(f"   📍 Position: {demo['config']['position']}")
                else:
                    print(f"   📝 Subtitles: Disabled")
            else:
                print(f"   ❌ Failed to create video")
        
        print("\n🎉 Demo completed!")
        print("📁 Check the 'output' folder for generated videos")
        print("\n💡 Tips:")
        print("   - White subtitles work best for most backgrounds")
        print("   - Yellow provides high contrast for better readability")
        print("   - Cyan gives a modern, tech-focused look")
        print("   - Center position works well for short text")
        print("   - Bottom position is traditional and widely readable")
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")

def show_subtitle_timing_info():
    """Show information about subtitle timing"""
    print("\n⏱️ Subtitle Timing Information:")
    print("=" * 40)
    print("• Subtitles are automatically timed based on word count")
    print("• Each sentence becomes a separate subtitle chunk")
    print("• Minimum duration: 1.0 seconds (configurable)")
    print("• Maximum duration: 4.0 seconds (configurable)")
    print("• Gap between subtitles: 0.2 seconds (configurable)")
    print("• Timing is calculated based on audio duration")
    print("• Longer sentences get more screen time")
    print("• Short sentences are grouped for better readability")

if __name__ == "__main__":
    demo_subtitle_features()
    show_subtitle_timing_info() 