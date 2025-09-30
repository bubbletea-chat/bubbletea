"""
Claude Assistant Bot - Simple conversations with AI
"""
import os

import bubbletea_chat as bt
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


@bt.chatbot('claude-assistant')
def claude_assistant(message: str):
    # Get API key from environment variable
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        return bt.Text("Please set your ANTHROPIC_API_KEY environment variable")

    # Initialize Anthropic client
    client = Anthropic(api_key=api_key)


    try:
        # Create message with Claude API
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": message}
            ]
        )

        # Extract text from response
        response_text = response.content[0].text

        # Return the response as markdown
        return bt.Markdown(response_text)
    except Exception as e:
        return bt.Text(f"Sorry, I encountered an error: {str(e)}")


@claude_assistant.config
def get_config():
    return bt.BotConfig(
        # Required fields
        name="claude-bot",
        url=os.getenv("BOT_URL", "localhost:5000"),
        is_streaming=False,

        # Metadata for discovery and display
        display_name="Claude Bot",  # Max 20 characters
        subtitle="Chat with AI",  # Max 30 characters
        icon_url="https://www.anthropic.com/images/icons/apple-touch-icon.png",
        preview_video_url="",  # Optional
        description="""
# Claude Bot 🤖

This bot provides a simple AI chat experience powered by Anthropic's Claude API directly.

## 💡 Features
- **Natural Language Conversations**
- **Quick Responses**
- **Direct Anthropic Integration**
- **Multi-turn Dialog** – Great for brainstorming, questions, and writing help

## ✨ Example Commands
- Start typing anything to chat
- Ask questions and get instant responses

## 🔄 Best For
- Quick questions
- Brainstorming ideas
- Writing and coding assistance

## ⚙️ Setup
Make sure to set your ANTHROPIC_API_KEY environment variable
        """,
        visibility="public",

        # Welcome message
        initial_text="👋 Hi! I'm Claude Bot. Just type a message to get started!",
    )


if __name__ == "__main__":
    bt.run_server(claude_assistant, port=8080, host="0.0.0.0")
