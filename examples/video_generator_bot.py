"""
Example bot that demonstrates long-running operations using Block response.
This bot simulates video generation that takes 60 seconds.
"""

import asyncio
import bubbletea_chat as bt
import httpx
from datetime import datetime
import os

# Bot configuration
@bt.config()
def get_config():
    return bt.BotConfig(
        name="video-generator-bot",
        url="http://localhost:8001",
        is_streaming=False,  # Non-streaming bot
        emoji="🎬",
        initial_text="Hi! I can generate videos for you. Just tell me what you'd like to create!",
        sample_questions=[
            "Create a video of a sunset over the ocean",
            "Generate a timelapse of a flower blooming",
            "Make a video of a rocket launch"
        ]
    )

# Global client for making API calls
client = httpx.AsyncClient()

# Bot API key (set this as environment variable)
BOT_API_KEY = os.getenv("BUBBLETEA_API_KEY", "bt_fU78vGeD8S0pBngm0gKKtOjbNXo0bvne")
BUBBLETEA_API_URL = os.getenv("BUBBLETEA_API_URL", "http://localhost:8000")

@bt.chatbot()
def video_generator(message: str, conversation_uuid: str):
    """
    Main bot function that returns Block response and triggers background processing
    """
    # Send initial message and block
    responses = [
        bt.Text(f"I'll create a video based on: '{message}'"),
        bt.Text("This process usually takes about 60 seconds. Please wait..."),
        bt.Block(timeout=90)  # 90 second timeout
    ]
    
    # Start background task to generate video
    asyncio.create_task(generate_video_async(message, conversation_uuid))
    
    return responses

async def generate_video_async(prompt: str, conversation_uuid: str):
    """
    Background task that simulates video generation and sends result via API
    """
    try:
        # Simulate video generation (60 seconds)
        print(f"[{datetime.now()}] Starting video generation for conversation {conversation_uuid}")
        await asyncio.sleep(60)  # Simulate long processing
        
        # In real implementation, this would be actual video generation
        video_url = f"https://example.com/videos/generated_{conversation_uuid[:8]}.mp4"
        
        # Create proper bt components for the response
        components = [
            bt.Text("✅ Video generation complete!"),
            bt.Image(url=video_url, alt="Generated video thumbnail"),
            bt.Text(f"Your video is ready: {video_url}")
        ]
        
        # Send completion message via Developer API
        await send_completion_message(conversation_uuid, components)
        print(f"[{datetime.now()}] Video generation completed for conversation {conversation_uuid}")
        
    except Exception as e:
        print(f"Error in video generation: {e}")
        # Send error message
        error_component = bt.Text(f"❌ Sorry, video generation failed: {str(e)}")
        await send_completion_message(conversation_uuid, [error_component])

async def send_completion_message(conversation_uuid: str, components: list):
    """
    Send message to BubbleTea backend via Developer API
    """
    url = f"{BUBBLETEA_API_URL}/v1/developer/conversation/{conversation_uuid}/message"
    headers = {
        "Authorization": f"Bearer {BOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Convert bt components to dict format for the API
    components_dict = [component.model_dump() for component in components]
    content = {"components": components_dict}
    
    try:
        response = await client.post(
            url,
            json={"content": content},
            headers=headers
        )
        response.raise_for_status()
        print(f"Message sent successfully to conversation {conversation_uuid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    # Run the bot server
    bt.run_server(video_generator, port=8001)