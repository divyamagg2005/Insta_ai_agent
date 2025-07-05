import os
from instagrapi import Client
from config import config
import time

class InstagramAgent:
    def __init__(self):
        self.client = Client()
        self.username = config.ig_username
        self.password = config.ig_password
        self.logged_in = False
    
    def login(self):
        """Login to Instagram"""
        if not self.username or not self.password:
            print("Error: Instagram credentials not configured")
            return False
            
        try:
            # Try to load existing session
            session_file = "session.json"
            if os.path.exists(session_file):
                self.client.load_settings(session_file)
                self.client.login(self.username, self.password)
                self.logged_in = True
                print("Logged in using existing session")
            else:
                # Fresh login
                self.client.login(self.username, self.password)
                self.client.dump_settings(session_file)
                self.logged_in = True
                print("Logged in successfully")
            
            return True
            
        except Exception as e:
            print(f"Login failed: {e}")
            self.logged_in = False
            return False
    
    def upload_reel(self, video_path, caption, hashtags=""):
        """Upload reel to Instagram"""
        if not self.logged_in:
            if not self.login():
                return False
        
        try:
            # Prepare caption with hashtags
            full_caption = f"{caption}\n\n{hashtags}"
            
            # Upload reel
            media = self.client.clip_upload(
                video_path,
                caption=full_caption
            )
            
            print(f"Reel uploaded successfully! Media ID: {media.id}")
            return True
            
        except Exception as e:
            print(f"Failed to upload reel: {e}")
            return False
    
    def schedule_reel(self, video_path, caption, hashtags, schedule_time):
        """Schedule reel for later (placeholder - Instagram API doesn't support scheduling)"""
        print("Note: Instagram API doesn't support scheduling. Use third-party tools like Later or Buffer.")
        return False
    
    def get_account_info(self):
        """Get account information"""
        if not self.logged_in:
            if not self.login():
                return None
        
        try:
            user_id = self.client.user_id_from_username(self.username)
            info = self.client.user_info(user_id)
            return {
                'username': info.username,
                'followers': info.follower_count,
                'following': info.following_count,
                'posts': info.media_count
            }
        except Exception as e:
            print(f"Error getting account info: {e}")
            return None