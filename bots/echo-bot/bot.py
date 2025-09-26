"""
Echo Bot - Simple message echo demonstration
"""
import os

import bubbletea_chat as bt
from dotenv import load_dotenv

load_dotenv()


@bt.chatbot('echo-bot')
def echo_bot(message: str):
    # Simple echo functionality - returns the message with "Echo: " prefix
    return bt.Text(f"Echo: {message}")


@echo_bot.config
def get_config():
    return bt.BotConfig(
        # Required fields
        name="echo-simple",
        url="localhost:5000",
        is_streaming=False,

        # Metadata for discovery and display
        display_name="Echo Bot",  # Max 20 characters
        subtitle="Echoes your messages",  # Max 30 characters
        icon_url="",  # Optional icon URL
        preview_video_url="",  # Optional preview video
        description="""
# Echo Bot 🔊

A simple demonstration bot that echoes back whatever you type. Perfect for testing and learning BubbleTea bot development.

## 💡 Features
- **Instant Echo** - Returns your message immediately
- **Simple Implementation** - Great for learning
- **No External APIs** - Works standalone
- **Lightweight** - Minimal dependencies

## ✨ Example Commands
- Type anything and get it echoed back
- Send emojis, text, or numbers
- Perfect for testing message flow

## 🔄 Best For
- Testing BubbleTea integration
- Learning bot development
- Quick message verification
- Development template

## ⚙️ Setup
No API keys required! Just run and start chatting.
        """,
        visibility="public",

        # Welcome message
        initial_text="👋 Hi there! I'm Echo Bot. Just type something, and I'll echo it back to you!",
    )


if __name__ == "__main__":
    bt.run_server(echo_bot, port=8080, host="0.0.0.0")
