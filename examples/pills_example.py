"""
Example bot demonstrating the use of Pills components in BubbleTea.
This bot shows various ways to use pills for interactive options.
"""

import bubbletea_chat as bt
from bubbletea_chat.components import Pill, Pills

@bt.config()
def get_config():
    return bt.BotConfig(
        name="Pills Example Bot",
        url="http://localhost:8004",
        is_streaming=False,
        initial_text="Hello! I can show you different pill interssfaces. Try asking me about:\n• Food preferences\n• Travel destinations\n• Programming languages\n• Or just say 'show me pills'"
    )

@bt.chatbot()
def pills_bot(message: str) -> list:
    message_lower = message.lower()
    
    pill1 = Pill(text="Italian", pill_value="cuisine:italian")
    pill2 = Pill(text="Japanese", pill_value="cuisine:japanese") 
    pill3 = Pill(text="Mexican", pill_value="cuisine:mexican")
    pill4 = Pill(text="Indian", pill_value="cuisine:indian")
    pill5 = Pill(text="Spanish", pill_value="cuisine:spanish")
    pill6 = Pill(text="American", pill_value="cuisine:american")
    
    # Create a Pills component with the individual pills
    food_pills = Pills(pills=[pill1, pill2, pill3, pill4, pill5, pill6])
    
    return [
        bt.Text("What type of cuisine do you prefer?"),
        food_pills
    ]


if __name__ == "__main__":
    bt.run_server(pills_bot, port=8004)