"""
Chat history example for BubbleTea bots
"""

import bubbletea_chat as bt


@bt.chatbot(stream=False)
async def history_bot(message: str, **kwargs):
    """
    Bot that demonstrates chat history access

    The chat_history parameter contains previous messages
    """
    components = []
    
    # Access chat history if available
    chat_history = kwargs.get("chat_history", [])

    components.append(bt.Text(f"Current message: {message}"))

    if chat_history:
        components.append(bt.Markdown(
            f"## Chat History\nYou have {len(chat_history)} previous messages"
        ))

        # Show last few messages
        recent = chat_history[-3:] if len(chat_history) > 3 else chat_history
        for msg in recent:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")[:50]  # First 50 chars
            components.append(bt.Text(f"- {role}: {content}..."))
    else:
        components.append(bt.Text("This is the start of our conversation!"))

    components.append(bt.Text("Keep chatting to build up history!"))
    
    return components


if __name__ == "__main__":
    bt.run_server(history_bot, port=8008)
