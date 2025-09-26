"""
BubbleTea Developers Help Bot - AI assistant for BubbleTea developers
"""

import bubbletea_chat as bt
from bubbletea_chat import LLM
import os


# Load the BubbleTea documentation
def load_documentation():
    """Load the BubbleTea README documentation"""
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        return f.read()


@bt.chatbot("bt-developers-help")
async def bt_developers_help_bot(message: str):
    """
    Help developers with BubbleTea SDK questions
    """
    # Load documentation
    documentation = load_documentation()

    # Create context for the LLM with the entire documentation
    context = f"""You are a helpful assistant specifically designed to help developers with the BubbleTea SDK.
You have access to the official BubbleTea documentation and should provide accurate, helpful answers based on it.

Here is the complete BubbleTea SDK documentation:

{documentation}

Based on this documentation, please answer the user's question. If the question asks for code examples, provide them from the documentation.
Make sure to:
1. Be concise and direct
2. Provide code examples when relevant
3. Reference specific components or methods from BubbleTea
4. If the documentation doesn't contain the answer, say so clearly

User Question: {message}"""

    # Use LLM to generate response
    llm = LLM(model="gpt-4-turbo-preview")

    # Get the complete response
    response = await llm.acomplete(context)

    # Create response components
    responses = [
        bt.Text("💡 "),
        bt.Markdown(response),
        bt.Markdown(
            "\n\n---\n*Need more help? Check the [full documentation](https://pypi.org/project/bubbletea-chat/) or ask a more specific question!*"
        ),
    ]

    # Return all components as a single response
    return responses


@bt_developers_help_bot.config
def get_config():
    return bt.BotConfig(
        # Required fields
        name="bt-developers-help",
        url=os.getenv("BOT_URL", "http://localhost:8002"),
        is_streaming=False,
        # App store metadata
        display_name="BT Dev Helper",
        subtitle="Help with BubbleTea SDK",
        icon_emoji="📚",
        description="""
# BubbleTea Developers Help Bot 📚

An AI assistant specifically trained on the BubbleTea SDK documentation to help developers build amazing chatbots.

## Features
- **Quick Answers** - Get instant help with BubbleTea SDK questions
- **Code Examples** - See practical examples for common tasks
- **Component Reference** - Learn about Text, Image, Markdown, Cards, Pills, and more
- **LLM Integration** - Guidance on using OpenAI, Claude, Gemini and 100+ models
- **Best Practices** - Tips for building production-ready bots

        """,
        # Access control
        visibility="public",
        # User experience
        initial_text="👋 Hi! I'm the BubbleTea Developer Helper. Ask me anything about building bots with the BubbleTea SDK! For example: 'How do I create a simple chatbot?' or 'Show me how to use images in my bot'.",
    )


if __name__ == "__main__":
    bt.run_server(bt_developers_help_bot, port=8080, host="0.0.0.0")
