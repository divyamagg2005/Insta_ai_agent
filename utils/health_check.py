#!/usr/bin/env python3
"""
Health check utilities for Learn2Reel
"""

import os
import sys
import logging
from typing import Dict, Any

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import config

logger = logging.getLogger(__name__)

def check_api_keys() -> Dict[str, bool]:
    """Check if required API keys are configured"""
    return {
        'gemini_api': bool(config.gemini_api_key),
        'elevenlabs_api': bool(config.elevenlabs_api_key),
        'instagram_credentials': bool(config.ig_username and config.ig_password)
    }

def check_directories() -> Dict[str, bool]:
    """Check if required directories exist and are writable"""
    directories = ['output', 'assets']
    results = {}
    
    for directory in directories:
        path = os.path.join(os.getcwd(), directory)
        exists = os.path.exists(path)
        writable = os.access(path, os.W_OK) if exists else False
        results[directory] = exists and writable
    
    return results

def check_ffmpeg() -> bool:
    """Check if FFmpeg is available"""
    try:
        import subprocess
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return False

def check_font_file() -> bool:
    """Check if the custom font file exists"""
    font_path = os.path.join('assets', 'Montserrat-SemiBold.ttf')
    return os.path.exists(font_path)

def get_system_info() -> Dict[str, Any]:
    """Get system information for health check"""
    import platform
    
    return {
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'architecture': platform.architecture()[0],
        'processor': platform.processor()
    }

def comprehensive_health_check() -> Dict[str, Any]:
    """Perform a comprehensive health check of the system"""
    health_status = {
        'status': 'healthy',
        'checks': {},
        'system_info': get_system_info(),
        'config': {
            'subtitle_enabled': config.subtitle_enabled,
            'subtitle_font_size': config.subtitle_font_size,
            'video_dimensions': f"{config.video_width}x{config.video_height}",
            'video_fps': config.video_fps
        }
    }
    
    # Check API keys
    api_status = check_api_keys()
    health_status['checks']['api_keys'] = api_status
    
    # Check directories
    dir_status = check_directories()
    health_status['checks']['directories'] = dir_status
    
    # Check FFmpeg
    ffmpeg_available = check_ffmpeg()
    health_status['checks']['ffmpeg'] = ffmpeg_available
    
    # Check font file
    font_available = check_font_file()
    health_status['checks']['font_file'] = font_available
    
    # Determine overall health
    all_checks = []
    all_checks.extend(api_status.values())
    all_checks.extend(dir_status.values())
    all_checks.append(ffmpeg_available)
    all_checks.append(font_available)
    
    # API keys are critical, others are warnings
    critical_checks = [api_status['gemini_api'], api_status['elevenlabs_api']]
    
    if not all(critical_checks):
        health_status['status'] = 'critical'
    elif not all(all_checks):
        health_status['status'] = 'warning'
    else:
        health_status['status'] = 'healthy'
    
    return health_status

def print_health_report():
    """Print a formatted health report"""
    health = comprehensive_health_check()
    
    print("🏥 Learn2Reel Health Check Report")
    print("=" * 40)
    
    # Overall status
    status_emoji = {
        'healthy': '✅',
        'warning': '⚠️',
        'critical': '❌'
    }
    print(f"Overall Status: {status_emoji[health['status']]} {health['status'].upper()}")
    
    # API Keys
    print("\n🔑 API Keys:")
    for key, available in health['checks']['api_keys'].items():
        status = "✅ Available" if available else "❌ Missing"
        print(f"  {key}: {status}")
    
    # Directories
    print("\n📁 Directories:")
    for directory, available in health['checks']['directories'].items():
        status = "✅ Available" if available else "❌ Missing/Not Writable"
        print(f"  {directory}: {status}")
    
    # System tools
    print("\n🛠️ System Tools:")
    ffmpeg_status = "✅ Available" if health['checks']['ffmpeg'] else "❌ Missing"
    font_status = "✅ Available" if health['checks']['font_file'] else "❌ Missing"
    print(f"  FFmpeg: {ffmpeg_status}")
    print(f"  Custom Font: {font_status}")
    
    # System info
    print("\n💻 System Information:")
    for key, value in health['system_info'].items():
        print(f"  {key}: {value}")
    
    # Configuration
    print("\n⚙️ Configuration:")
    for key, value in health['config'].items():
        print(f"  {key}: {value}")
    
    return health['status'] == 'healthy'

if __name__ == "__main__":
    success = print_health_report()
    sys.exit(0 if success else 1) 