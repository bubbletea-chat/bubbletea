"""
ChatGPT Assistant Bot - Threaded conversations with AI
"""
import bubbletea_chat as bt
from bubbletea_chat import LLM
import asyncio
import httpx
from datetime import datetime
from typing import List
import time
import os

from dotenv import load_dotenv
load_dotenv()

async def process_message_async(message: str,
                                conversation_uuid: str,
                                user_uuid: str = None,
                                thread_id: str = None,
                                images: List[bt.ImageInput] = None):

    llm = LLM(model="gpt-4", llm_provider="openai")

    if thread_id:
        # Handle images if provided
        response = llm.get_assistant_response(thread_id, message)

    # Create the message component
    result = bt.Markdown(response)
    content = result.model_dump()

    # API endpoint and headers
    b = time.time()
    url = f"https://backend.bubbletea.chat/v1/developer/conversation/{conversation_uuid}/message"
    headers = {
        "x-api-key": os.getenv("BUBBLETEA_API_KEY"),
        "Content-Type": "application/json",
        "accept": "application/json"
    }

    # Create payload matching the API format
    payload = {
        "sender": "agent",
        "sender_account_id": user_uuid,
        "content": content
    }

    async with httpx.AsyncClient() as client:
        try:
            response_api = await client.post(url,
                                             json=payload,
                                             headers=headers)

            response_api.raise_for_status()
            print("time taken: ", time.time() - b)
        except Exception as e:
            print(f"[{datetime.now()}] Error sending message to API: {e}")


@bt.chatbot('chatgpt-assistant')
def gpt_assistant(message: str,
                  user_uuid: str = None,
                  thread_id: str = None,
                  conversation_uuid: str = None):
    # Start async processing in background

    llm = LLM(model="gpt-4", llm_provider="openai")
    print(f"Processing ChatGPT message for conversation: {conversation_uuid}")

    # Check if thread_id exists, if not create one
    if not thread_id:
        thread_id = llm.create_thread(user_uuid)

    asyncio.create_task(
        process_message_async(message=message,
                              conversation_uuid=conversation_uuid,
                              user_uuid=user_uuid,
                              thread_id=thread_id))

    responses = [
        bt.Text(
            "Processing your message... You'll receive a response shortly!"),
        bt.Block(timeout=120)  # 120 second timeout
    ]

    result = bt.BaseComponent(thread_id=thread_id, payload=responses)
    return result


@gpt_assistant.config
def get_config():
    return bt.BotConfig(
        # Required fields
        name="chatgpt-wrapper",
        url="localhost:5000",
        is_streaming=False,  # Useful for ChatGPT-like typing behavior

        # Metadata for discovery and display
        display_name="ChatGPT Thread Bot",  # Max 20 characters
        subtitle="Chat in threads with AI",  # Max 30 characters
        icon_url=
        "https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        preview_video_url="",  # Optional
        description="""
# ChatGPT Thread Bot 🤖🧵

This bot provides an AI chat experience powered by ChatGPT, with support for threaded messaging.

## 💡 Features
- **Natural Language Conversations**
- **Threaded Replies** – Keep conversations organized
- **Streamed Responses** – Watch the response generate in real time
- **Context Retention** – Understands previous messages in a thread
- **Multi-turn Dialog** – Great for brainstorming, questions, and writing help

## ✨ Example Commands
- Start typing anything to chat
- Ask follow-ups in a thread to maintain context
- Use `reset` to start over

## 🔄 Best For
- Customer support
- Brainstorming ideas
- Writing and coding assistance
        """,
        visibility="public",

        # Welcome message
        initial_text=
        "👋 Hi! I'm ChatGPT in threads. Just type a message to get started. Reply in threads to keep the context!",

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
