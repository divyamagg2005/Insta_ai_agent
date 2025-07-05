import google.generativeai as genai
from config import config

class ContentAgent:
    def __init__(self):
        if not config.gemini_api_key:
            print("Error: Gemini API key not configured")
            return
        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    def generate_script(self, learning_content, duration=30):
        """Generate a reel-friendly script from learning content"""
        prompt = f"""
        You are a content creator who specializes in making engaging Instagram Reels about learning and education.
        
        Transform the following learning content into a compelling Instagram Reel script:
        
        Learning Content: {learning_content}
        
        Guidelines:
        - Keep it conversational and engaging
        - Use hook in the first 3 seconds
        - Break down complex concepts into simple terms
        - Include a call-to-action at the end
        - Script should be 15-25 seconds when spoken at normal pace (about 40-60 words)
        - Use short sentences and pauses for emphasis
        - Make it sound natural, not robotic
        - Be extremely concise - every word counts
        - Focus on ONE key point only
        - IMPORTANT: Use ONLY plain text - NO hashtags, asterisks, underscores, or special formatting characters
        - The script will be converted to speech, so avoid any characters that would be read aloud
        
        Format your response as a clean script without any additional formatting or explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating script: {e}")
            return None
    
    def generate_hashtags(self, learning_content):
        """Generate relevant hashtags for the reel"""
        prompt = f"""
        Generate 20 relevant Instagram hashtags for a learning reel about: {learning_content}
        
        Mix of:
        - Popular general hashtags (#learning, #education, #tech)
        - Specific topic hashtags
        - Trending hashtags
        - Community hashtags
        
        Return only the hashtags separated by spaces, no explanations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating hashtags: {e}")
            return "#learning #education #tech #ai #coding #developer #student #knowledge #growth #tutorial"
