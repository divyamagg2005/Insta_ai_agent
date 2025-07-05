# Learn2Reel API Documentation

## ContentAgent API

### `generate_script(learning_content, duration=30)`
Generates a reel-friendly script from learning content.

**Parameters:**
- `learning_content` (str): The learning content to convert
- `duration` (int): Target duration in seconds (default: 30)

**Returns:**
- `str`: Generated script or None if failed

**Example:**
```python
agent = ContentAgent()
script = agent.generate_script("Today I learned about RAG in AI", 30)
```

### `generate_hashtags(learning_content)`
Generates relevant hashtags for the content.

**Parameters:**
- `learning_content` (str): The learning content

**Returns:**
- `str`: Space-separated hashtags

## VoiceAgent API

### `generate_voiceover(script, output_path="output/voiceover.mp3")`
Generates voiceover from script using ElevenLabs.

**Parameters:**
- `script` (str): The script to convert to speech
- `output_path` (str): Path to save the audio file

**Returns:**
- `str`: Path to generated audio file or None if failed

### `get_available_voices()`
Gets list of available voices from ElevenLabs.

**Returns:**
- `dict`: Voice information or None if failed

## VideoAgent API

### `create_reel(script, voiceover_path, background_video=None, output_path="output/final_reel.mp4")`
Creates Instagram reel from components.

**Parameters:**
- `script` (str): The script text
- `voiceover_path` (str): Path to voiceover audio
- `background_video` (str, optional): Path to background video
- `output_path` (str): Path to save final video

**Returns:**
- `str`: Path to generated video or None if failed

## InstagramAgent API

### `login()`
Logs into Instagram account.

**Returns:**
- `bool`: True if successful, False otherwise

### `upload_reel(video_path, caption, hashtags="")`
Uploads reel to Instagram.

**Parameters:**
- `video_path` (str): Path to video file
- `caption` (str): Caption for the reel
- `hashtags` (str): Hashtags to include

**Returns:**
- `bool`: True if successful, False otherwise

### `get_account_info()`
Gets account information.

**Returns:**
- `dict`: Account info or None if failed

## Configuration

All agents use environment variables for configuration:

```env
GEMINI_API_KEY=your_key
ELEVENLABS_API_KEY=your_key
ELEVENLABS_VOICE_ID=voice_id
IG_USERNAME=username
IG_PASSWORD=password
```

## Error Handling

All methods include error handling and will return None or False on failure. Check the console output for detailed error messages.

## Rate Limits

- **ElevenLabs**: 10,000 characters/month (free tier)
- **Instagram**: No official limits, but avoid rapid posting
- **Gemini**: 15 requests/minute (free tier)

## Best Practices

1. **Content Length**: Keep learning content under 500 words for best results
2. **Video Duration**: 15-60 seconds works best for engagement
3. **Hashtags**: Use 5-10 relevant hashtags, avoid spam
4. **Posting Frequency**: Max 1-2 reels per day
5. **Error Handling**: Always check return values before proceeding 