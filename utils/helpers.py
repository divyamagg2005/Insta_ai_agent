import os
import shutil
import logging
from typing import Optional, List
from datetime import datetime
import json

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    logger = logging.getLogger("learn2reel")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def ensure_dir(path: str) -> None:
    """Ensure directory exists"""
    os.makedirs(path, exist_ok=True)

def clean_output_dir(output_dir: str) -> None:
    """Clean output directory"""
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

def get_file_size(file_path: str) -> str:
    """Get human-readable file size"""
    if not os.path.exists(file_path):
        return "0 B"
    
    size = os.path.getsize(file_path)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

def validate_video_file(file_path: str) -> bool:
    """Validate video file exists and is readable"""
    if not os.path.exists(file_path):
        return False
    
    try:
        # Try to get file size
        size = os.path.getsize(file_path)
        return size > 0
    except:
        return False

def generate_filename(prefix: str, extension: str) -> str:
    """Generate unique filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

def save_metadata(metadata: dict, file_path: str) -> None:
    """Save metadata to JSON file"""
    with open(file_path, 'w') as f:
        json.dump(metadata, f, indent=2, default=str)

def load_metadata(file_path: str) -> Optional[dict]:
    """Load metadata from JSON file"""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return None

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to max length with ellipsis"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract keywords from text (simple implementation)"""
    # Remove common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be', 
        'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 
        'would', 'could', 'should', 'may', 'might', 'must', 'can', 'i', 'you', 
        'he', 'she', 'it', 'we', 'they', 'this', 'that', 'these', 'those'
    }
    
    words = text.lower().split()
    keywords = [word.strip('.,!?;:()[]"\'') for word in words 
                if word.strip('.,!?;:()[]"\'').lower() not in stop_words 
                and len(word.strip('.,!?;:()[]"\'')) > 2]
    
    # Count frequency
    word_count = {}
    for word in keywords:
        word_count[word] = word_count.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    return [word for word, count in sorted_words[:max_keywords]] 