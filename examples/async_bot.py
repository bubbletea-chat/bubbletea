"""
Async bot example with mixed content (non-streaming)
"""

import asyncio
import bubbletea_chat as bt


@bt.chatbot(stream=False)
async def async_bot(message: str):
    """An async bot that returns multiple components without streaming"""
    
    # Collect all components
    components = []
    
    # Initial greeting
    components.append(bt.Text("Hello! I'm an async bot. Let me process your message..."))
    
    # Simulate async processing
    await asyncio.sleep(0.5)
    
    # Process the message
    words = message.split()
    components.append(bt.Text(f"You said: {message}"))
    
    # Add analysis
    components.append(bt.Markdown(f"""
## Analysis of your message

- **Length**: {len(message)} characters
- **Words**: {len(words)} words
- **Contains question**: {"Yes" if "?" in message else "No"}
    """))
    
    # Add an image if mentioned
    if any(word in message.lower() for word in ["image", "picture", "photo"]):
        components.append(bt.Text("Since you mentioned images, here's one for you:"))
        components.append(bt.Image("https://picsum.photos/400/300", alt="A random beautiful image"))
    
    # Final message
    components.append(bt.Text("That's all from the async bot! 🎉"))
    
    # Return all components at once (non-streaming)
    return components


if __name__ == "__main__":
    bt.run_server(async_bot, port=8001)