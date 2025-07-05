import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    # API Keys
    gemini_api_key: str = os.getenv('GEMINI_API_KEY', '')
    elevenlabs_api_key: str = os.getenv('ELEVENLABS_API_KEY', '')
    elevenlabs_voice_id: str = os.getenv('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')
    
    # Instagram
    ig_username: str = os.getenv('IG_USERNAME', '')
    ig_password: str = os.getenv('IG_PASSWORD', '')
    
    # Paths
    output_dir: str = os.getenv('OUTPUT_DIR', 'output')
    assets_dir: str = os.getenv('ASSETS_DIR', 'assets')
    
    # Video settings
    video_width: int = int(os.getenv('VIDEO_WIDTH', '1080'))
    video_height: int = int(os.getenv('VIDEO_HEIGHT', '1920'))
    video_fps: int = int(os.getenv('VIDEO_FPS', '24'))
    
    # Voice settings
    voice_stability: float = float(os.getenv('VOICE_STABILITY', '0.5'))
    voice_similarity_boost: float = float(os.getenv('VOICE_SIMILARITY_BOOST', '0.75'))
    
    # Content settings
    default_reel_duration: int = int(os.getenv('DEFAULT_REEL_DURATION', '30'))
    max_hashtags: int = int(os.getenv('MAX_HASHTAGS', '20'))
    
    # Subtitle settings
    subtitle_enabled: bool = os.getenv('SUBTITLE_ENABLED', 'true').lower() == 'true'
    subtitle_font_size: int = int(os.getenv('SUBTITLE_FONT_SIZE', '50'))
    subtitle_font_color: str = os.getenv('SUBTITLE_FONT_COLOR', 'white')
    subtitle_background_color: str = os.getenv('SUBTITLE_BACKGROUND_COLOR', 'black@0.7')
    subtitle_position_y: str = os.getenv('SUBTITLE_POSITION_Y', 'h-text_h-50')
    subtitle_min_duration: float = float(os.getenv('SUBTITLE_MIN_DURATION', '1.0'))
    subtitle_max_duration: float = float(os.getenv('SUBTITLE_MAX_DURATION', '4.0'))
    subtitle_gap: float = float(os.getenv('SUBTITLE_GAP', '0.2'))
    
    def validate(self) -> list:
        """Validate configuration and return list of missing/invalid values"""
        errors = []
        
        if not self.gemini_api_key:
            errors.append("GEMINI_API_KEY is required")
        
        if not self.elevenlabs_api_key:
            errors.append("ELEVENLABS_API_KEY is required")
        
        if not self.ig_username:
            errors.append("IG_USERNAME is required for Instagram upload")
        
        if not self.ig_password:
            errors.append("IG_PASSWORD is required for Instagram upload")
        
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
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        return cls()

# Global config instance
config = Config.from_env() 