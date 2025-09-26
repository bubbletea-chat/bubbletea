import os
import asyncio
import threading
from typing import Dict, Any, List, Optional
from datetime import datetime
from dotenv import load_dotenv

import httpx
import bubbletea_chat as bt
from services.video_generator import VideoGeneratorService

load_dotenv()


async def process_message_async(message: str, conversation_uuid: str, images: Optional[List[bt.ImageInput]] = None):
    """Process video generation asynchronously."""
    video_service = VideoGeneratorService()

    temp_video_url = await video_service.generate_video_async(
        text_prompt=message, image_url=images[0].url if images else None
    )

    message = bt.Video(url=temp_video_url)
    content = message.model_dump()

    api_key = os.getenv("BUBBLETEA_API_KEY")
    if not api_key:
        return

    url = f"https://backend.bubbletea.chat/v1/developer/conversation/{conversation_uuid}/message"
    headers = {"x-api-key": api_key, "Content-Type": "application/json", "accept": "application/json"}

    payload = {"sender": "agent", "content": content}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()


@bt.chatbot("video-bot")
def video_bot(
    message: str,
    images: Optional[List[bt.ImageInput]] = None,
    user_email: Optional[str] = None,
    user_uuid: Optional[str] = None,
    conversation_uuid: Optional[str] = None,
    chat_history: Optional[List[Dict[str, Any]]] = None,
):
    """BubbleTea chatbot that generates videos from text prompts and images."""

    greetings = [
        "hi",
        "hello",
        "hey",
        "greetings",
        "good morning",
        "good afternoon",
        "good evening",
        "howdy",
        "hola",
        "bonjour",
        "sup",
        "yo",
    ]

    message_lower = message.lower().strip()
    if any(greeting in message_lower.split() for greeting in greetings) or message_lower in greetings:
        return [
            bt.Text("👋 Hello! I'm Photo2Video Bot."),
            bt.Text(""),
            bt.Text("I can help you transform your photos into stunning videos!"),
            bt.Text(""),
            bt.Text("To get started, please:"),
            bt.Text("1. Upload an image"),
            bt.Text("2. Provide a description of the video you want to create"),
            bt.Text(""),
            bt.Text("For example: 'Make this photo zoom in slowly with dramatic music'"),
        ]

    if not images or len(images) == 0:
        return [
            bt.Text("📸 Please upload an image along with your text description."),
            bt.Text(""),
            bt.Text("I need both:"),
            bt.Text("• An image to work with"),
            bt.Text("• A text description of what you want"),
            bt.Text(""),
            bt.Text("Try uploading a photo and describing the video effect you'd like!"),
        ]

    def run_async_task():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(process_message_async(message, conversation_uuid, images))
        finally:
            loop.close()

    thread = threading.Thread(target=run_async_task)
    thread.daemon = True
    thread.start()

    responses = [
        bt.Text("🎬 Great! I'm now creating your video..."),
        bt.Text(""),
        bt.Text(f"📝 Your request: {message}"),
        bt.Text(""),
        bt.Text("This may take a moment. I'll notify you when it's ready!"),
        bt.Block(timeout=120),
    ]
    return responses


@video_bot.config
def get_config():
    return bt.BotConfig(
        name="photo2video-bot",
        url=os.getenv("BOT_URL", "http://localhost:5003"),
        is_streaming=False,
        display_name="Photo to Video",
        subtitle="Convert photos into videos",
        icon_url="https://iafqwfegdftjthhbccyt.supabase.co/storage/v1/object/sign/bubble-tea/logoooooo.jpeg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9kZTJhMWQ4MC0wZTc0LTQ3NjAtYjA4NC02ODg0NjA0OTUxN2MiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJidWJibGUtdGVhL2xvZ29vb29vby5qcGVnIiwiaWF0IjoxNzUyODU3NDcxLCJleHAiOjE3ODQzOTM0NzF9.Yvqwo30tDX1FITZGc_47FtIppXKemOMqak90Z6xWVOQ",
        preview_video_url="http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        description="""
# Photo2Video Bot

Transform your static images into dynamic videos with ease!

## 🎞️ Key Features
- **Upload Photos** – Drag & drop or select multiple images
- **Customize Output** – Choose transitions, speed, and soundtrack
- **Instant Preview** – See the video before downloading
- **Download in HD** – Get a high-quality video output
- **Optional Effects** – Add text overlays, pan-zoom effects, and more

## 🚀 How to Use
1. Type `upload` to start uploading your photos
2. Customize your settings with `options`
3. Type `create` to generate your video
4. Use `preview` to view it or `download` to get the file

Try commands like: `upload`, `create`, `preview`, `options`, `effects`, `download`
        """,
        visibility="public",
        initial_text="📸 Welcome to Photo2Video! Upload your photos and turn them into stunning videos. Type `upload` to begin!",
        example_chats=[
            "https://bubbletea.chat/chat/photo_to_video_bot/shared/ZFEmw2tuUdzOlQ6OtrKAiM6-dkIyC4tBmPqdieN4Eb8"
        ],
    )


if __name__ == "__main__":
    bt.run_server(video_bot, port=8080, host="0.0.0.0")
