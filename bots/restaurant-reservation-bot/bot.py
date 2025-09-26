"""
Simple Restaurant Reservations Bot
"""

import json
import os
from datetime import datetime

import bubbletea_chat as bt
from bubbletea_chat.components import Pill, Pills, Text
from dotenv import load_dotenv

load_dotenv()

# Simple storage using Replit Object Storage
try:
    from replit.object_storage import Client

    storage_client = Client()
    use_replit_storage = True
except ImportError:
    storage_client = None
    use_replit_storage = False


def storage_get(key):
    """Get value from storage"""
    if use_replit_storage:
        try:
            return storage_client.download_as_text(key)
        except Exception:
            return None
    else:
        # Fallback to local file
        try:
            with open(f"data_{key}.json", "r") as f:
                return f.read()
        except Exception:
            return None


def storage_set(key, value):
    """Set value in storage"""
    if use_replit_storage:
        try:
            storage_client.upload_from_text(key, value)
            return True
        except Exception:
            return False
    else:
        # Fallback to local file
        try:
            with open(f"data_{key}.json", "w") as f:
                f.write(value)
            return True
        except Exception:
            return False


@bt.chatbot("restaurant-reservations")
def restaurant_bot(message: str, user_uuid: str = None, conversation_uuid: str = None):
    # Get user state from storage
    state_key = f"{user_uuid}_{conversation_uuid}_state"
    state_data = storage_get(state_key)
    if state_data:
        state = json.loads(state_data)
    else:
        state = {"step": 0, "data": {}}

    step = state["step"]
    data = state["data"]

    # Get conversation history from storage
    conv_key = f"{user_uuid}_{conversation_uuid}_conversation"
    conv_data = storage_get(conv_key)
    if conv_data:
        conversations = json.loads(conv_data)
    else:
        conversations = []
    conversations.append({"user": message, "timestamp": datetime.now().isoformat()})

    # Simple linear flow
    response = []

    if step == 0:
        if message.lower() == "start":
            state["step"] = 1
            response = [
                Text(
                    "Hi! What are you in the mood for today? I have some great new Thai spots if you'd like a recommendation."
                ),
                Text("💡 Try typing: 'I want Mexican, with availability for 4 people around 6/6:30'"),
            ]
        else:
            response = [Text("Type 'start' to begin")]

    elif step == 1:
        if "mexican" in message.lower() and "4" in message:
            state["step"] = 2
            data["request"] = message
            response = [
                Text("Sure - I can help with that. Can I confirm what day you are looking for?"),
                Pills(
                    pills=[
                        Pill("Tonight", pill_value="tonight"),
                        Pill("Tomorrow", pill_value="tomorrow"),
                        Pill("Another day", pill_value="another_day"),
                    ]
                ),
            ]
        else:
            response = [
                Text("Please tell me what cuisine you want, for how many people, and what time."),
                Text("💡 Try typing: 'I want Mexican, with availability for 4 people around 6/6:30'"),
            ]

    elif step == 2:
        if message.lower() in ["tonight", "tomorrow", "another_day"]:
            state["step"] = 3
            data["day"] = message
            response = [
                Text("Sure! Here are option for reasonably priced Mexican tomorrow for 4 people around 6-6:30:"),
                Text("🍽️ Rosa Mexicano - $$, 0.4 miles, Trendy, vibey spot known for their tacos"),
                Text("Type 'Rosa Mexicano' to select this option"),
            ]
        else:
            response = [
                Text("Please select a day option"),
                Text("💡 Click one of the buttons above or type: 'tomorrow'"),
            ]

    elif step == 3:
        if "rosa" in message.lower():
            state["step"] = 4
            data["restaurant"] = "Rosa Mexicano"
            response = [
                Text("Here are the times available for 4 people:"),
                Pills(
                    pills=[
                        Pill("5:30", pill_value="5:30"),
                        Pill("6:00", pill_value="6:00"),
                        Pill("6:30", pill_value="6:30"),
                    ]
                ),
            ]
        else:
            response = [Text("Please type 'Rosa Mexicano' to continue"), Text("💡 Type exactly: 'Rosa Mexicano'")]

    elif step == 4:
        if message in ["5:30", "6:00", "6:30"]:
            state["step"] = 5
            data["time"] = message
            response = [
                Text("Ok, can I book the following?"),
                Text("Rosa Mexicano"),
                Text("4 people"),
                Text(f"{message}pm on 6/22"),
                Pills(pills=[Pill("Cancel", pill_value="cancel"), Pill("Confirm", pill_value="confirm")]),
            ]
        else:
            response = [Text("Please select a time"), Text("💡 Click one of the time buttons above or type: '6:00'")]

    elif step == 5:
        if message.lower() == "confirm":
            state["step"] = 0
            # Save complete reservation to storage
            reservation_key = f"{user_uuid}_{conversation_uuid}_reservation"
            storage_set(
                reservation_key,
                json.dumps(
                    {"conversation": conversations, "reservation": data, "confirmed_at": datetime.now().isoformat()}
                ),
            )
            response = [
                Text("✅ Great! Your reservation is confirmed."),
                Text("Type 'start' to make another reservation."),
            ]
        elif message.lower() == "cancel":
            state["step"] = 0
            response = [Text("Cancelled. Type 'start' to begin again.")]
        else:
            response = [
                Text("Please type 'confirm' or 'cancel'"),
                Text("💡 Click one of the buttons above or type: 'confirm'"),
            ]

    else:
        response = [Text("Type 'start' to begin")]

    # Save state and conversation back to storage
    storage_set(state_key, json.dumps(state))
    storage_set(conv_key, json.dumps(conversations))

    return response


@restaurant_bot.config
def get_config():
    return bt.BotConfig(
        name="restaurant-reservations",
        display_name="Resy Bot",
        url=os.getenv("BOT_URL", "http://localhost:5006"),
        icon_url="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=400",
        is_streaming=False,
        initial_text="Hi! Type 'start' to begin making a reservation.",
        discoverable=False,
    )


if __name__ == "__main__":
    bt.run_server(restaurant_bot, port=8080, host="0.0.0.0")
