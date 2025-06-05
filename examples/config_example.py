#!/usr/bin/env python3
"""
Example of a bot with custom configuration
"""

import bubbletea_chat as bt

# Define bot configuration
@bt.config()
def get_config():
    return bt.BotConfig(
        name="Greeting Bot",
        url="http://localhost:8000",
        is_streaming=True,
        emoji="👋",  # Wave emoji for greeting bot
        initial_text="Hi there! I'm the Greeting Bot. Tell me your name and I'll give you a personalized greeting!"
    )

# Define the chatbot
@bt.chatbot
async def greeting_bot(message: str):
    """A friendly bot that gives personalized greetings"""
    
    # Simple streaming response
    yield bt.Text("Nice to meet you! ")
    
    if any(greeting in message.lower() for greeting in ["hi", "hello", "hey"]):
        yield bt.Text("I see you're being polite! ")
    
    # Extract potential name (simple heuristic)
    words = message.split()
    if len(words) > 0:
        potential_name = words[-1].capitalize()
        yield bt.Text(f"Is your name {potential_name}? ")
        yield bt.Text("What a wonderful name! ")
    
    yield bt.Markdown("## Here's your personalized greeting:")
    yield bt.Text(f"🎉 Welcome to BubbleTea, {potential_name if 'potential_name' in locals() else 'friend'}! 🎉")

if __name__ == "__main__":
    print("Starting Greeting Bot on http://localhost:8000")
    print("Config endpoint: http://localhost:8000/config")
    print("Chat endpoint: http://localhost:8000/chat")
    bt.run_server(greeting_bot)