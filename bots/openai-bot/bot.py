"""
ChatGPT Assistant Bot - Threaded conversations with AI
"""

import asyncio
import os

import bubbletea_chat as bt
import httpx
from bubbletea_chat import LLM
from dotenv import load_dotenv

load_dotenv()


async def process_message_async(message: str, conversation_uuid: str, thread_id: str = None):

    llm = LLM(model="gpt-4", llm_provider="openai")

    if thread_id:
        # Handle images if provided
        response = llm.get_assistant_response(thread_id, message)

    # Create the message component
    result = bt.Markdown(response)
    content = result.model_dump()

    # API endpoint and headers
    url = f"https://backend.bubbletea.chat/v1/developer/conversation/{conversation_uuid}/message"
    headers = {
        "x-api-key": os.getenv("BUBBLETEA_API_KEY"),
        "Content-Type": "application/json",
        "accept": "application/json",
    }

    # Create payload matching the API format
    payload = {"sender": "agent", "content": content}

    async with httpx.AsyncClient() as client:
        try:
            response_api = await client.post(url, json=payload, headers=headers)
            response_api.raise_for_status()
        except Exception:
            pass


@bt.chatbot("chatgpt-assistant")
def gpt_assistant(message: str, user_uuid: str = None, thread_id: str = None, conversation_uuid: str = None):
    llm = LLM(model="gpt-4", llm_provider="openai")

    # Check if thread_id exists, if not create one
    if not thread_id:
        thread_id = llm.create_thread(user_uuid)
    else:
        pass

    asyncio.create_task(
        process_message_async(
            message=message, conversation_uuid=conversation_uuid, user_uuid=user_uuid, thread_id=thread_id
        )
    )

    responses = [
        bt.Text("Processing your message... You'll receive a response shortly!"),
        bt.Block(timeout=120),  # 120 second timeout
    ]

    result = bt.BaseComponent(thread_id=thread_id, payload=responses)
    return result


@gpt_assistant.config
def get_config():
    return bt.BotConfig(
        # Required fields - These must be provided
        name="chatgpt-wrapper",
        url="localhost:5000",
        is_streaming=False,  # Useful for ChatGPT-like typing behavior
        # Metadata for discovery and display
        display_name="ChatGPT Thread Bot",  # Max 20 characters
        subtitle="Chat in threads with AI",  # Max 30 characters
        icon_url="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        icon_emoji="🤖",  # Emoji icon alternative if no icon_url
        preview_video_url="",  # Optional demo video URL
        description="""
# ChatGPT Thread Bot 🤖🧵

This bot provides an AI chat experience powered by ChatGPT, with support for threaded messaging.

## 💡 Features
- **Natural Language Conversations**
- **Threaded Replies** – Keep conversations organized
- **Streamed Responses** – Watch the response generate in real time

## ✨ Example Commands
- Start typing anything to chat
- Ask follow-ups in a thread to maintain context
- Use `reset` to start over

## 🔄 Best For
- Customer support
- Brainstorming ideas
- Writing and coding assistance
        """,
        visibility="public",  # Who can see the bot: "public" or "private"
        discoverable=True,  # Whether the bot is discoverable in bot directory

        # Legacy fields (kept for backward compatibility)
        emoji="🤖",  # Deprecated, use icon_emoji instead
        initial_text="👋 Hi! I'm ChatGPT in threads. Just type a message to get started. Reply in threads to keep the context!",
        authorization="public",  # Deprecated, use visibility instead
        authorized_emails=None,  # List of authorized emails for private bots
        subscription_monthly_price=0,  # Monthly subscription price in cents (0 = free, 500 = $5.00)

        # Advanced configuration
        cors_config=None,  # Custom CORS configuration (optional)

        # Bot examples
        example_chats=[
            "https://bubbletea.chat/shared/wrhjUAYmHryp3XFZFauSYyCjypq4n8v3egC9RmvxtD8"
        ],  # Sample prompts users can try
    )


if __name__ == "__main__":
    bt.run_server(gpt_assistant, port=8080, host="0.0.0.0")
