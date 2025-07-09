"""
Simple echo bot example for BubbleTea
"""

import bubbletea_chat as bt

@bt.config()
def get_config():
    return bt.BotConfig(
        name="Echo Bot with history",
        url="http://localhost:8004",
        is_streaming=False,
        initial_text="Hello! I will echo your message with user email, uuid and conversation uuid"
    )

@bt.chatbot
def echo_bot(message: str, user_uuid: str = None, conversation_uuid: str = None):
    """A simple bot that echoes back the user's message"""
    response = f"You said: {message}"
    if user_uuid:
        response += f"\nYour User UUID: {user_uuid}"
    if conversation_uuid:
        response += f"\nYour Conversation UUID: {conversation_uuid}"

    return bt.Text(f"You said: {response}")

    

if __name__ == "__main__":
    # Run the bot locally
    bt.run_server(echo_bot, port=8000)