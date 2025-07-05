import unittest
from unittest.mock import Mock, patch
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.content_agent import ContentAgent
from agents.voice_agent import VoiceAgent
from agents.video_agent import VideoAgent
from agents.instagram_agent import InstagramAgent

class TestContentAgent(unittest.TestCase):
    def setUp(self):
        self.content_agent = ContentAgent()
    
    @patch('google.generativeai.GenerativeModel')
    def test_generate_script(self, mock_model):
        # Mock the API response
        mock_response = Mock()
        mock_response.text = "Today I learned about AI and it's amazing!"
        mock_model.return_value.generate_content.return_value = mock_response
        
        script = self.content_agent.generate_script("AI is cool")
        self.assertIsInstance(script, str)
        self.assertGreater(len(script), 0)
    
    @patch('google.generativeai.GenerativeModel')
    def test_generate_hashtags(self, mock_model):
        mock_response = Mock()
        mock_response.text = "#AI #learning #tech #coding #education"
        mock_model.return_value.generate_content.return_value = mock_response
        
        hashtags = self.content_agent.generate_hashtags("AI learning")
        self.assertIsInstance(hashtags, str)
        self.assertIn("#", hashtags)

class TestVoiceAgent(unittest.TestCase):
    def setUp(self):
        self.voice_agent = VoiceAgent()
    
    @patch('requests.post')
    def test_generate_voiceover(self, mock_post):
        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response
        
        with patch('builtins.open', mock_open()):
            result = self.voice_agent.generate_voiceover("Test script")
            self.assertIsNotNone(result)

class TestVideoAgent(unittest.TestCase):
    def setUp(self):
        self.video_agent = VideoAgent()
    
    def test_create_simple_background(self):
        # Test background creation
        background = self.video_agent.create_simple_background(5)
        self.assertIsNotNone(background)
        self.assertEqual(background.duration, 5)

class TestInstagramAgent(unittest.TestCase):
    def setUp(self):
        self.instagram_agent = InstagramAgent()
    
    @patch('instagrapi.Client')
    def test_login(self, mock_client):
        # Mock successful login
        mock_client.return_value.login.return_value = True
        
        result = self.instagram_agent.login()
        # Note: This will depend on actual environment variables
        # In a real test, you'd mock the environment variables too

if __name__ == '__main__':
    unittest.main() 