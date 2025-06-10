"""
Streaming bot example with mixed content
"""

import asyncio
import bubbletea_chat as bt

@bt.chatbot
async def streaming_bot(message: str):
    """A bot that streams different types of content"""
    
    # Initial greeting
    yield bt.Text("Hello! I'm a streaming bot. Let me show you what I can do...")
    await asyncio.sleep(1)
    
    # Stream some text word by word
    words = message.split()
    yield bt.Text("You said: ")
    for word in words:
        yield bt.Text(f"{word} ")
        await asyncio.sleep(0.2)
    
    await asyncio.sleep(0.5)
    
    # Add some markdown
    yield bt.Markdown(f"""
## Analysis of your message

- **Length**: {len(message)} characters
- **Words**: {len(words)} words
- **Contains question**: {"Yes" if "?" in message else "No"}
    """)
    
    await asyncio.sleep(1)
    
    # Add an image
    if any(word in message.lower() for word in ["image", "picture", "photo"]):
        yield bt.Text("Since you mentioned images, here's one for you:")
        yield bt.Image(
            "https://picsum.photos/400/300",
            alt="A random beautiful image"
        )
    
    # Final message
    yield bt.Text("That's all from the streaming bot! 🎉")


if __name__ == "__main__":
    bt.run_server(streaming_bot, port=8001)