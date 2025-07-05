import os
import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from pathlib import Path

@dataclass
class Config:
    # API Keys
    gemini_api_key: str = ''
    elevenlabs_api_key: str = ''
    elevenlabs_voice_id: str = 'FGY2WhTYpPnrIDTdsKH5'
    
    # Instagram
    ig_username: str = ''
    ig_password: str = ''
    
    # Paths
    output_dir: str = 'output'
    assets_dir: str = 'assets'
    
    # Video settings
    video_width: int = 1080
    video_height: int = 1920
    video_fps: int = 24
    
    # Voice settings
    voice_stability: float = 0.5
    voice_similarity_boost: float = 0.75
    
    # Content settings
    default_reel_duration: int = 30
    max_hashtags: int = 20
    
    # Subtitle settings
    subtitle_enabled: bool = True
    subtitle_font_size: int = 50
    subtitle_font_color: str = 'white'
    subtitle_background_color: str = 'black@0.7'
    subtitle_position_y: str = 'h-text_h-50'
    subtitle_min_duration: float = 1.0
    subtitle_max_duration: float = 4.0
    subtitle_gap: float = 0.2
    
    # Configuration file path
    config_file: str = 'learn2reel_config.json'
    
    def validate(self) -> list:
        """Validate configuration and return list of missing/invalid values"""
        errors = []
        
        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")
        
        if not self.elevenlabs_api_key:
            errors.append("ELEVENLABS_API_KEY is required")
        
        # Instagram credentials are optional
        # if not self.ig_username:
        #     errors.append("IG_USERNAME is required for Instagram upload")
        # 
        # if not self.ig_password:
        #     errors.append("IG_PASSWORD is required for Instagram upload")
        
        if self.video_width <= 0 or self.video_height <= 0:
            errors.append("Video dimensions must be positive")
        
        if self.video_fps <= 0:
            errors.append("Video FPS must be positive")
        
        if self.subtitle_font_size <= 0:
            errors.append("Subtitle font size must be positive")
        
        if self.subtitle_min_duration <= 0 or self.subtitle_max_duration <= 0:
            errors.append("Subtitle duration settings must be positive")
        
        if self.subtitle_min_duration > self.subtitle_max_duration:
            errors.append("Subtitle min duration cannot be greater than max duration")
        
        return errors
    
    def save_config(self) -> bool:
        """Save configuration to JSON file"""
        try:
            config_dict = asdict(self)
            # Don't save sensitive data
            config_dict.pop('gemini_api_key', None)
            config_dict.pop('elevenlabs_api_key', None)
            config_dict.pop('ig_username', None)
            config_dict.pop('ig_password', None)
            
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving config: {e}")
            return False
    
    def load_config(self) -> bool:
        """Load configuration from JSON file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config_dict = json.load(f)
                
                # Update non-sensitive settings
                for key, value in config_dict.items():
                    if hasattr(self, key) and not key.endswith('_key') and not key in ['ig_username', 'ig_password']:
                        setattr(self, key, value)
                return True
        except Exception as e:
            print(f"Error loading config: {e}")
        return False
    
    def get_sensitive_data(self) -> Dict[str, str]:
        """Get sensitive data (API keys, credentials)"""
        return {
            'gemini_api_key': self.gemini_api_key,
            'elevenlabs_api_key': self.elevenlabs_api_key,
            'ig_username': self.ig_username,
            'ig_password': self.ig_password
        }
    
    def set_sensitive_data(self, data: Dict[str, str]):
        """Set sensitive data (API keys, credentials)"""
        if 'gemini_api_key' in data:
            self.gemini_api_key = data['gemini_api_key']
        if 'elevenlabs_api_key' in data:
            self.elevenlabs_api_key = data['elevenlabs_api_key']
        if 'ig_username' in data:
            self.ig_username = data['ig_username']
        if 'ig_password' in data:
            self.ig_password = data['ig_password']
    
    @classmethod
    def create_interactive(cls) -> 'Config':
        """Create configuration interactively"""
        config = cls()
        
        print("🎬 Learn2Reel Configuration Setup")
        print("=" * 40)
        
        # Load existing config if available
        config.load_config()
        
        # API Keys (Required)
        print("\n🔑 API Keys (Required):")
        print("Get your API keys from:")
        print("- Gemini: https://makersuite.google.com/app/apikey")
        print("- ElevenLabs: https://elevenlabs.io/")
        
        if not config.gemini_api_key:
            config.gemini_api_key = input("Enter your Gemini API Key: ").strip()
        
        if not config.elevenlabs_api_key:
            config.elevenlabs_api_key = input("Enter your ElevenLabs API Key: ").strip()
        
        # Instagram (Optional)
        print("\n📱 Instagram Credentials (Optional):")
        print("Leave blank if you don't want auto-upload")
        
        if not config.ig_username:
            config.ig_username = input("Enter Instagram Username (optional): ").strip()
        
        if not config.ig_password:
            config.ig_password = input("Enter Instagram Password (optional): ").strip()
        
        # Subtitle Settings
        print("\n🎬 Subtitle Settings:")
        subtitle_enabled = input("Enable subtitles? (y/n, default: y): ").strip().lower()
        if subtitle_enabled in ['n', 'no']:
            config.subtitle_enabled = False
        
        if config.subtitle_enabled:
            try:
                font_size = input(f"Subtitle font size (default: {config.subtitle_font_size}): ").strip()
                if font_size:
                    config.subtitle_font_size = int(font_size)
            except ValueError:
                pass
        
        # Save configuration
        if config.save_config():
            print("\n✅ Configuration saved successfully!")
        else:
            print("\n⚠️ Could not save configuration")
        
        return config

# Global config instance
config = Config()
config.load_config() 