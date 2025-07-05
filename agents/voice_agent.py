import os
import requests
from dotenv import load_dotenv

load_dotenv()

class VoiceAgent:
    def __init__(self):
        self.api_key = os.getenv('ELEVENLABS_API_KEY')
        self.voice_id = os.getenv('ELEVENLABS_VOICE_ID', 'EXAVITQu4vr4xnSDxMaL')  # Default voice
        self.base_url = "https://api.elevenlabs.io/v1"
    
    def generate_voiceover(self, script, output_path="output/voiceover.mp3"):
        """Generate voiceover from script using ElevenLabs API"""
        
        # Clean the script text - remove formatting characters
        cleaned_script = self.clean_script_text(script)
        
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        url = f"{self.base_url}/text-to-speech/{self.voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        
        data = {
            "text": cleaned_script,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.0,
                "use_speaker_boost": True
            },
            "optimization_level": 0  # Faster generation, shorter output
        }
        
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"Voiceover saved to: {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            print(f"Error generating voiceover: {e}")
            return None
    
    def clean_script_text(self, script):
        """Clean script text by removing formatting characters and special symbols"""
        import re
        
        # Remove hashtags, asterisks, and other formatting characters
        cleaned = script
        
        # Remove hashtags
        cleaned = re.sub(r'#\w+', '', cleaned)
        
        # Remove asterisks (used for emphasis)
        cleaned = cleaned.replace('*', '')
        
        # Remove other common formatting characters
        cleaned = cleaned.replace('_', '')  # Underscores
        cleaned = cleaned.replace('~', '')  # Tildes
        cleaned = cleaned.replace('`', '')  # Backticks
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove leading/trailing whitespace
        cleaned = cleaned.strip()
        
        # Remove any remaining special characters that might be read aloud
        cleaned = re.sub(r'[^\w\s.,!?;:()\-\'"]', '', cleaned)
        
        print(f"Original script length: {len(script)} chars")
        print(f"Cleaned script length: {len(cleaned)} chars")
        
        return cleaned
    
    def get_available_voices(self):
        """Get list of available voices from ElevenLabs"""
        url = f"{self.base_url}/voices"
        headers = {"xi-api-key": self.api_key}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return None
