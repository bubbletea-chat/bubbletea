import bubbletea_chat as bt

steps = [
    "add walk the dog",
    "add buy milk",
    "add call mom",
    "remove walk the dog",
    "list",
    "clear",
    "add meditate",
    "list"
]

responses = [
    bt.Text(
        "Sure! 🐶 I've added \"walk the dog\" to your to-do list.\nTo-Do List:\n1. Walk the dog"
    ),
    bt.Text(
        "Done! 🛒 I've added \"buy milk\".\nTo-Do List:\n1. Walk the dog\n2. Buy milk"
    ),
    bt.Text(
        "Absolutely! 📞 I've added \"call mom\".\nTo-Do List:\n1. Walk the dog\n2. Buy milk\n3. Call mom"
    ),
    bt.Text(
        "Removed \"walk the dog\" from your list.\nTo-Do List:\n1. Buy milk\n2. Call mom"
    ),
    bt.Text(
        "Here's your to-do list:\n1. Buy milk\n2. Call mom"
    ),
    bt.Text(
        "All clear! 🧹 Your to-do list is now empty."
    ),
    bt.Text(
        "Nice! 🧘 I've added \"meditate\".\nTo-Do List:\n1. Meditate"
    ),
    bt.Text(
        "Here's your to-do list:\n1. Meditate"
    )
]

@bt.chatbot
def todo_bot(chat: bt.Chat):
    user_msg = chat.last_user_message().strip().lower()
    step = chat.state.get("step", 0)

    if step < len(steps) and user_msg == steps[step]:
        chat.state["step"] = step + 1
        return responses[step]
    elif step < len(steps):
        return bt.Text(f"Please type: '{steps[step]}' to continue.")
    else:
        return bt.Text("✅ You've completed the to-do list walkthrough! Want to start over? Just refresh the session.")

if __name__ == "__main__":
    bt.run_server(todo_bot)
