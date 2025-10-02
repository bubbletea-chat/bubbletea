import os

import google.generativeai as genai
import bubbletea_chat as bt
from dotenv import load_dotenv

load_dotenv()

@bt.chatbot('gemini-assistant')
def gemini_assistant(message: str,
                     user_uuid: str = None,
                     conversation_uuid: str = None):
    # Configure Gemini API with your API key
    # Make sure to set GOOGLE_API_KEY environment variable
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return bt.Text("Please set your GEMINI_API_KEY environment variable")

    genai.configure(api_key=api_key)

    # Initialize the Gemini model
    model = genai.GenerativeModel('gemini-2.0-flash')


    try:
        # Generate response from Gemini
        response = model.generate_content(message)
        response_text = response.text

        # Return the response as markdown
        return bt.Markdown(response_text)
    except Exception as e:
        return bt.Text(f"Sorry, I encountered an error: {str(e)}")


@gemini_assistant.config
def get_config():
    return bt.BotConfig(
        name="gemini-wrapper",
        url=os.getenv("BOT_URL", "localhost:5001"),
        is_streaming=False,
        display_name="Gemini Thread Bot",
        subtitle="Chat in threads with AI",
        icon_url="https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg",
        preview_video_url="",
        description="""
# Gemini Thread Bot 🤖🧵

This bot provides an AI chat experience powered by Google's Gemini, with support for threaded messaging.

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
        initial_text="👋 Hi! I'm Gemini in threads. Just type a message to get started. Reply in threads to keep the context!",
    )


if __name__ == "__main__":
    bt.run_server(gemini_assistant, port=8080, host="0.0.0.0")
