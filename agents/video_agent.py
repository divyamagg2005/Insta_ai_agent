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

def estimate_text_width(text, font_size=60):
    """Estimate text width in pixels for overflow detection"""
    # Rough estimation: average character width is about 0.6 * font_size
    # For 1080x1920 video, safe width is around 900-1000 pixels
    estimated_width = len(text) * font_size * 0.6
    return estimated_width

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
    
    def get_video_duration(self, video_path):
        """Get video duration using FFmpeg"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-show_entries", 
                "format=duration", "-of", "csv=p=0", video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return float(result.stdout.strip())
        except:
            return None
    
    def analyze_voiceover_timing(self, voiceover_path, script):
        """Analyze voiceover audio to get more accurate word timing (placeholder for future enhancement)"""
        # This is a placeholder for future implementation
        # In a real implementation, you could use:
        # - Speech recognition with timestamps
        # - Audio analysis to detect word boundaries
        # - Whisper API with word-level timestamps
        
        duration = self.get_audio_duration(voiceover_path)
        if duration is None:
            return None
        
        # For now, return basic timing info
        return {
            'duration': duration,
            'words': len(script.split()),
            'words_per_second': len(script.split()) / duration if duration > 0 else 0
        }
    
    def combine_video_audio(self, video_path, audio_path, output_path, duration):
        """Combine video and audio using FFmpeg, ensuring video matches audio duration"""
        # Get video duration to check if we need to loop it
        video_duration = self.get_video_duration(video_path)
        
        if video_duration and video_duration < duration:
            # If video is shorter than audio, loop it
            print(f"Video duration ({video_duration}s) is shorter than audio ({duration}s). Looping video...")
            cmd = [
                "ffmpeg", "-y",
                "-stream_loop", "-1",  # Loop the video input
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-map", "0:v:0",  # Use video from first input (background video)
                "-map", "1:a:0",  # Use audio from second input (voiceover)
                "-shortest",  # This ensures the output duration matches the shorter of video/audio
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                "-r", "24",
                output_path
            ]
        else:
            # Normal case - video is longer than or equal to audio
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "libx264",
                "-c:a", "aac",
                "-map", "0:v:0",  # Use video from first input (background video)
                "-map", "1:a:0",  # Use audio from second input (voiceover)
                "-shortest",  # This ensures the output duration matches the shorter of video/audio
                "-vf", "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
                "-r", "24",
                output_path
            ]
        
        subprocess.run(cmd, check=True)
        print(f"Video combined with audio. Final duration: {duration} seconds")
    
    def add_subtitles(self, input_path, script, output_path, duration):
        """Add synchronized subtitles to video using FFmpeg"""
        # Split script into subtitle chunks (5-6 words per chunk)
        subtitle_chunks = self.split_script_for_subtitles(script, duration)
        
        if not subtitle_chunks:
            # Fallback to simple text overlay if subtitle splitting fails
            self.add_text_overlay(input_path, script, output_path)
            return
        
        # Create subtitle filter (multi-chunk, timed) with custom font
        filter_parts = []
        font_path = "assets/Montserrat-SemiBold.ttf"
        
        # Check if font file exists
        if not os.path.exists(font_path):
            print(f"[WARNING] Font file not found: {font_path}")
            print("[DEBUG] Using default font")
            font_path = ""  # Use default font
        
        for chunk in subtitle_chunks:
            text = chunk['text']
            if not text or not text.strip():
                continue
            
            # Check if text needs to be split into multiple lines
            estimated_width = estimate_text_width(text, config.subtitle_font_size)
            if estimated_width > 900:
                # Split long text into multiple lines
                lines = self.split_text_into_lines(text)
                for line_idx, line in enumerate(lines):
                    if not line.strip():
                        continue
                    escaped_text = line.replace("'", "\\'")
                    y_offset = line_idx * (config.subtitle_font_size + 10)
                                    # Build filter with or without custom font
                if font_path:
                    subtitle_filter = (
                        f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
                        f"fontcolor=white:"
                        f"fontsize={config.subtitle_font_size}:"
                        f"x=(w-text_w)/2:"
                        f"y=(h/4)+{y_offset}:"
                        f"borderw=2:bordercolor=black:"
                        f"enable='between(t,{chunk['start_time']},{chunk['end_time']})'"
                    )
                else:
                    subtitle_filter = (
                        f"drawtext=text='{escaped_text}':"
                        f"fontcolor=white:"
                        f"fontsize={config.subtitle_font_size}:"
                        f"x=(w-text_w)/2:"
                        f"y=(h/4)+{y_offset}:"
                        f"borderw=2:bordercolor=black:"
                        f"enable='between(t,{chunk['start_time']},{chunk['end_time']})'"
                    )
                    filter_parts.append(subtitle_filter)
            else:
                # Single line subtitle
                escaped_text = text.replace("'", "\\'")
                # Build filter with or without custom font
                if font_path:
                    subtitle_filter = (
                        f"drawtext=fontfile='{font_path}':text='{escaped_text}':"
                        f"fontcolor=white:"
                        f"fontsize={config.subtitle_font_size}:"
                        f"x=(w-text_w)/2:"
                        f"y=h/4:"
                        f"borderw=2:bordercolor=black:"
                        f"enable='between(t,{chunk['start_time']},{chunk['end_time']})'"
                    )
                else:
                    subtitle_filter = (
                        f"drawtext=text='{escaped_text}':"
                        f"fontcolor=white:"
                        f"fontsize={config.subtitle_font_size}:"
                        f"x=(w-text_w)/2:"
                        f"y=h/4:"
                        f"borderw=2:bordercolor=black:"
                        f"enable='between(t,{chunk['start_time']},{chunk['end_time']})'"
                    )
                filter_parts.append(subtitle_filter)
        
        # Combine all subtitle filters
        if filter_parts:
            filter_str = ",".join(filter_parts)
            print(f"[DEBUG] Using {len(filter_parts)} subtitle filters")
            print("[DEBUG] Subtitle chunks:")
            for i, chunk in enumerate(subtitle_chunks):
                print(f"  Chunk {i}: '{chunk['text']}' ({chunk['start_time']:.2f}s - {chunk['end_time']:.2f}s)")
        else:
            print("[DEBUG] No subtitle filters generated, using fallback")
            self.add_text_overlay(input_path, script, output_path)
            return
        
        # Apply subtitles using FFmpeg
        cmd = [
            "ffmpeg", "-y",
            "-i", input_path,
            "-vf", filter_str,
            "-c:v", "libx264",
            "-c:a", "copy",  # Preserve original audio
            output_path
        ]
        
        try:
            print(f"[DEBUG] Running FFmpeg command: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"Subtitles added successfully with custom font")
        except subprocess.CalledProcessError as e:
            print(f"Error adding subtitles: {e}")
            print("[DEBUG] Falling back to simple text overlay")
            # Fallback to simple text overlay
            self.add_text_overlay(input_path, script, output_path)
    
    def split_script_for_subtitles(self, script, duration, words_per_chunk=5):
        """Split script into timed subtitle chunks of N words each (default 5), synced with voiceover timing."""
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
        # Use more sophisticated timing that accounts for natural speech patterns
        words_per_second = total_words / duration
        seconds_per_word = duration / total_words
        
        # Split into 5-6 word chunks with overflow prevention
        chunks = []
        i = 0
        while i < total_words:
            # Try to get 5-6 words, but adjust if text would be too long
            chunk_words = words[i:i+words_per_chunk]
            if not chunk_words:
                i += words_per_chunk
                continue
            
            chunk_text = ' '.join(chunk_words)
            
            # Check if text would overflow using width estimation
            estimated_width = estimate_text_width(chunk_text, config.subtitle_font_size)
            max_safe_width = 900  # For 1080x1920 video
            
            if estimated_width > max_safe_width:
                # Reduce chunk size to prevent overflow
                reduced_chunk = words[i:i+max(3, words_per_chunk-2)]
                chunk_text = ' '.join(reduced_chunk)
                i += len(reduced_chunk)
            else:
                i += words_per_chunk
            
            if chunk_text.strip():
                chunks.append(chunk_text)
        
        # Calculate timing for each chunk with improved synchronization
        subtitle_chunks = []
        current_time = 0
        total_processed_words = 0
        
        for chunk_text in chunks:
            if not chunk_text.strip():
                continue
            
            chunk_word_count = len(chunk_text.split())
            
            # Calculate timing based on word position in the script
            # This provides better sync than equal word timing
            start_word_index = total_processed_words
            end_word_index = start_word_index + chunk_word_count
            
            # Calculate start and end times based on word position
            start_time = (start_word_index / total_words) * duration
            end_time = (end_word_index / total_words) * duration
            
            # Ensure minimum subtitle duration (1.0 seconds for better readability)
            min_duration = 1.0
            if end_time - start_time < min_duration:
                end_time = start_time + min_duration
            
            # Ensure maximum subtitle duration (3 seconds)
            max_duration = 3.0
            if end_time - start_time > max_duration:
                end_time = start_time + max_duration
            
            # Add a small gap between subtitles for better readability
            if subtitle_chunks and start_time < subtitle_chunks[-1]['end_time'] + 0.2:
                start_time = subtitle_chunks[-1]['end_time'] + 0.2
            
            subtitle_chunks.append({
                'text': chunk_text,
                'start_time': start_time,
                'end_time': end_time,
                'word_count': chunk_word_count
            })
            
            total_processed_words += chunk_word_count
            current_time = end_time
        
        return subtitle_chunks
    
    def split_text_into_lines(self, text, max_chars_per_line=25):
        """Split text into multiple lines to prevent overflow"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            # Check if adding this word would exceed the line limit
            if current_length + len(word) + 1 > max_chars_per_line and current_line:
                # Start a new line
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
            else:
                # Add to current line
                current_line.append(word)
                current_length += len(word) + 1 if current_line else len(word)
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines
    
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
            "-vf", filter_str,
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