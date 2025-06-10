"""
Simple echo bot example for BubbleTea
"""

import bubbletea_chat as bt

@bt.chatbot
def echo_bot(message: str):
    """A simple bot that echoes back the user's message"""
    yield bt.Text(f"You said: {message}")
    yield bt.Text("I'm a simple echo bot!")
    
    if "?" in message:
        yield bt.Markdown("*Looks like you asked a question!*")


if __name__ == "__main__":
    # Run the bot locally
    bt.run_server(echo_bot, port=8000)