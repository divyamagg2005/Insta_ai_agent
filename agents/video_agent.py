import os
import subprocess
import random
from PIL import Image
import numpy as np
import re
from config import config

# Helper to escape FFmpeg drawtext special characters and remove emojis
FFMPEG_SPECIAL_CHARS = [':', '%', '\\', "'", '"', '[', ']', '(', ')', ',', ';', '=', '#', '$', '&', '<', '>', '|', '{', '}', '^', '~', '`']
def escape_for_drawtext(text):
    # Remove emojis and non-BMP unicode symbols
    text = re.sub(r'[\U00010000-\U0010FFFF]', '', text)
    # Replace <<BR>> with literal \n for FFmpeg (do this FIRST)
    text = text.replace('<<BR>>', '\\n')
    # Escape backslashes first
    text = text.replace('\\', '\\\\')
    # Escape single quotes for FFmpeg
    text = text.replace("'", "\\'")
    # Escape colons and other special characters that might be interpreted as filter options
    text = text.replace(':', '\\:')
    text = text.replace('=', '\\=')
    text = text.replace(',', '\\,')
    return text

def clean_script_for_subtitles(script):
    """Clean script by removing all special characters and punctuation, leaving only words and spaces"""
    # Remove all punctuation and special characters except spaces
    cleaned = re.sub(r'[^\w\s]', '', script)
    # Remove extra whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # Remove leading/trailing whitespace
    cleaned = cleaned.strip()
    return cleaned

class VideoAgent:
    def __init__(self):
        self.output_dir = "output"
        self.assets_dir = "assets"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def create_reel(self, script, voiceover_path, output_path="output/final_reel.mp4"):
        """Create Instagram reel from voiceover and random background video using FFmpeg"""
        
        try:
            # Check if voiceover exists
            if not os.path.exists(voiceover_path):
                print(f"Voiceover file not found: {voiceover_path}")
                return None
            
            # Validate script length (should be under 100 words for 30 seconds)
            word_count = len(script.split())
            if word_count > 100:
                print(f"Script too long ({word_count} words). Truncating to first 80 words...")
                words = script.split()[:80]
                script = " ".join(words) + "..."
            
            # Get audio duration
            audio_duration = self.get_audio_duration(voiceover_path)
            if audio_duration is None:
                print("Could not determine audio duration")
                return None
            
            # Use audio duration as the target duration (don't trim audio)
            duration = audio_duration
            print(f"Using audio duration: {duration} seconds")
            
            # Select random background video (1-20)
            bg_video_path = self.select_random_background()
            if not bg_video_path:
                print("No background video found")
                return None
            
            # Combine video and audio
            self.combine_video_audio(bg_video_path, voiceover_path, output_path, duration)
            
            # Add subtitles if enabled
            if config.subtitle_enabled:
                final_output = output_path.replace('.mp4', '_with_subtitles.mp4')
                cleaned_script = self.clean_text_for_overlay(script)
                self.add_subtitles(output_path, cleaned_script, final_output, duration)
                output_path = final_output
            else:
                # Fallback to simple text overlay
                final_output = output_path.replace('.mp4', '_with_text.mp4')
                cleaned_script = self.clean_text_for_overlay(script)
                self.add_text_overlay(output_path, cleaned_script, final_output)
                output_path = final_output
            
            print(f"Reel created successfully: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error creating reel: {e}")
            return None
    
    def select_random_background(self):
        """Select a random background video from assets (1-20.mp4)"""
        video_number = random.randint(1, 20)
        video_path = os.path.join(self.assets_dir, f"{video_number}.mp4")
        
        if os.path.exists(video_path):
            print(f"Selected background video: {video_number}.mp4")
            return video_path
        else:
            print(f"Background video {video_number}.mp4 not found")
            return None
    

    
    def get_audio_duration(self, audio_path):
        """Get audio duration using FFmpeg"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-show_entries", 
                "format=duration", "-of", "csv=p=0", audio_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except:
            return None
    
    def combine_video_audio(self, video_path, audio_path, output_path, duration):
        """Combine video and audio using FFmpeg, ensuring video matches audio duration"""
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",  # This ensures the output duration matches the shorter of video/audio
            "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
            "-r", "24",
            output_path
        ]
        subprocess.run(cmd, check=True)
        print(f"Video combined with audio. Final duration: {duration} seconds")
    
    def add_subtitles(self, input_path, script, output_path, duration):
        """Add synchronized subtitles to video using FFmpeg"""
        # Split script into subtitle chunks (3 words per chunk)
        subtitle_chunks = self.split_script_for_subtitles(script, duration)
        
        if not subtitle_chunks:
            # Fallback to simple text overlay if subtitle splitting fails
            self.add_text_overlay(input_path, script, output_path)
            return
        
        # Create subtitle filter (multi-chunk, timed) with custom font
        filter_parts = []
        font_path = "assets/Montserrat-SemiBold.ttf"
        
        for chunk in subtitle_chunks:
            text = chunk['text']
            if not text or not text.strip():
                continue
            # Since we're only dealing with clean words and spaces, minimal escaping needed
            escaped_text = text.replace("'", "\\'")
            subtitle_filter = (
                f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
                f"fontcolor=white:"
                f"fontsize={config.subtitle_font_size}:"
                f"x=(w-text_w)/2:"
                f"y=h/4:"
                f"borderw=2:bordercolor=black:"
                f"enable='between(t,{chunk['start_time']},{chunk['end_time']})'"
            )
            filter_parts.append(subtitle_filter)
        filter_str = ",".join(filter_parts)
        print("[DEBUG] FFmpeg subtitle filter:", filter_str)
        
        # Apply subtitles using FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", filter_str,
            "-map", "0:v:0", "-map", "0:a:0",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-shortest",
            output_path
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"Subtitles added successfully with custom font")
        except subprocess.CalledProcessError as e:
            print(f"Error adding subtitles: {e}")
            # Fallback to simple text overlay
            self.add_text_overlay(input_path, script, output_path)
    
    def split_script_for_subtitles(self, script, duration, words_per_chunk=3):
        """Split script into timed subtitle chunks of N words each (default 3), synced with voiceover timing."""
        # Clean the script first to remove all special characters
        cleaned_script = clean_script_for_subtitles(script)
        cleaned_script = cleaned_script.strip()
        if not cleaned_script:
            return []
        
        words = cleaned_script.split()
        total_words = len(words)
        if total_words == 0:
            return []
        
        # Calculate timing based on voiceover duration
        # Assume words are spoken at roughly equal pace
        words_per_second = total_words / duration
        seconds_per_word = duration / total_words
        
        # Split into 3-word chunks
        chunks = []
        i = 0
        while i < total_words:
            chunk_words = words[i:i+words_per_chunk]
            if not chunk_words:
                i += words_per_chunk
                continue
            chunk_text = ' '.join(chunk_words)
            if chunk_text.strip():
                chunks.append(chunk_text)
            i += words_per_chunk
        
        # Calculate timing for each chunk based on word count
        subtitle_chunks = []
        current_time = 0
        for chunk_text in chunks:
            if not chunk_text.strip():
                continue
            chunk_word_count = len(chunk_text.split())
            chunk_duration = chunk_word_count * seconds_per_word
            start_time = current_time
            end_time = start_time + chunk_duration
            subtitle_chunks.append({
                'text': chunk_text,
                'start_time': start_time,
                'end_time': end_time
            })
            current_time = end_time
        
        return subtitle_chunks
    
    def create_subtitle_filter(self, subtitle_chunks):
        """Create FFmpeg filter for multiple subtitle overlays using a single drawtext with conditional text."""
        if not subtitle_chunks:
            return ""
        
        # Build a conditional text expression for a single drawtext filter
        text_conditions = []
        
        for i, chunk in enumerate(subtitle_chunks):
            text = chunk['text']
            if not text or not text.strip():
                print(f"[DEBUG] Skipping empty subtitle chunk at index {i}")
                continue
            escaped_text = escape_for_drawtext(text)
            print(f"[DEBUG] Subtitle chunk {i}: '{escaped_text}' (start={chunk['start_time']}, end={chunk['end_time']})")
            
            # Create condition for this time range
            condition = f"if(between(t,{chunk['start_time']},{chunk['end_time']}),'{escaped_text}',"
            text_conditions.append(condition)
        
        # Build nested conditional expression
        if not text_conditions:
            return ""
        
        # Start with the first condition
        filter_text = text_conditions[0]
        
        # Add nested conditions for each subsequent chunk
        for i in range(1, len(text_conditions)):
            filter_text += text_conditions[i]
        
        # Close all the nested conditions with empty string as default
        filter_text += "''" + ")" * len(text_conditions)
        
        # Create the complete filter
        filter_str = (
            f"drawtext=text='{filter_text}':"
            f"fontcolor=white:"
            f"fontsize={config.subtitle_font_size}:"
            f"x=(w-text_w)/2:"
            f"y=h/4:"
            f"borderw=2:bordercolor=black"
        )
        
        print("[DEBUG] FFmpeg subtitle filter:", filter_str)
        return filter_str
    
    def add_text_overlay(self, input_path, text, output_path):
        """Add text overlay to video using FFmpeg (fallback method)"""
        # Escape text for FFmpeg
        escaped_text = escape_for_drawtext(text)
        
        # Create filter string with custom font
        font_path = "assets/Montserrat-SemiBold.ttf"
        filter_str = f"drawtext=fontfile='{font_path}':text='{escaped_text}':fontcolor=white:fontsize=60:x=(w-text_w)/2:y=h/4:borderw=2:bordercolor=black:shadowcolor=black:shadowx=2:shadowy=2"
        
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", filter_str,  # Pass as single argument
            "-c:a", "copy",
            output_path
        ]
        subprocess.run(cmd, check=True)
    
    def clean_text_for_overlay(self, text):
        """Clean text for video overlay by removing formatting characters and emojis"""
        # Remove hashtags, asterisks, and other formatting characters
        cleaned = text
        
        # Remove hashtags
        cleaned = re.sub(r'#\w+', '', cleaned)
        
        # Remove asterisks, underscores, tildes, backticks
        cleaned = cleaned.replace('*', '').replace('_', '').replace('~', '').replace('`', '')
        
        # Remove emojis and non-BMP unicode symbols
        cleaned = re.sub(r'[\U00010000-\U0010FFFF]', '', cleaned)
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        return cleaned
    
    def download_stock_video(self, query="technology", output_path="assets/stock_clip.mp4"):
        """Download stock video (placeholder - would need actual stock video API)"""
        # This is a placeholder - in a real implementation, you'd use:
        # - Pexels API
        # - Unsplash API
        # - Your own stock video collection
        print(f"Stock video download not implemented. Using default background.")
        return None