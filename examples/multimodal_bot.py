"""
Multi-modal bot example showing various component types (without LLM)
"""

import bubbletea as bt
import random

# Sample data for the bot
GREETINGS = [
    "Hello there! 👋",
    "Hi! Welcome to the multi-modal bot!",
    "Greetings! Ready to see some cool components?",
]

IMAGES = [
    ("https://picsum.photos/400/300?random=1", "Beautiful landscape"),
    ("https://picsum.photos/400/300?random=2", "Abstract art"),
    ("https://picsum.photos/400/300?random=3", "Nature photography"),
    ("https://source.unsplash.com/400x300/?technology", "Technology"),
    ("https://source.unsplash.com/400x300/?nature", "Nature scene"),
]

# Simple predefined responses for different keywords
RESPONSES = {
    "hello": "Hello! How can I help you today?",
    "hi": "Hi there! Nice to meet you!",
    "help": "I'm here to demonstrate BubbleTea components. Try asking about 'tech', 'nature', or 'demo'!",
    "tech": "Here's some cool tech content!",
    "nature": "Nature is beautiful! Let me show you.",
    "demo": "Let me demonstrate all the components I can use!",
}

@bt.chatbot(stream=False)  # Force non-streaming mode
def multimodal_bot(message: str):
    """A bot that returns multiple component types at once"""
    
    components = []
    
    # Random greeting
    components.append(bt.Text(random.choice(GREETINGS)))
    
    # Echo the message
    components.append(bt.Text(f"You said: '{message}'"))
    
    # Simple keyword-based response
    message_lower = message.lower()
    response_text = "Thanks for your message!"
    
    for keyword, response in RESPONSES.items():
        if keyword in message_lower:
            response_text = response
            break
    
    components.append(bt.Text(response_text))
    
    # Add markdown content based on message
    components.append(bt.Markdown(f"""
## 🎨 Multi-Modal Response

This bot demonstrates all the available BubbleTea components:

### 📝 Text Components
Simple text messages like the greeting above.

### 📸 Image Components
Beautiful images with descriptions.

### 📋 Markdown Components
Rich formatted text with:
- **Bold** and *italic* text
- Lists and tables
- Code blocks
- And more!

### Your Message Analysis:
- Length: {len(message)} characters
- Words: {len(message.split())} words
- Uppercase letters: {sum(1 for c in message if c.isupper())}
- Contains numbers: {"Yes" if any(c.isdigit() for c in message) else "No"}
    """))
    
    # Add an image based on message content
    if any(word in message.lower() for word in ["tech", "computer", "ai", "robot"]):
        components.append(bt.Text("I see you're interested in technology!"))
        components.append(bt.Image(
            "https://source.unsplash.com/600x400/?artificial-intelligence,technology",
            alt="Technology and AI"
        ))
    elif any(word in message.lower() for word in ["nature", "tree", "forest", "ocean"]):
        components.append(bt.Text("Nature lover, I see!"))
        components.append(bt.Image(
            "https://source.unsplash.com/600x400/?nature,landscape",
            alt="Beautiful nature scene"
        ))
    else:
        # Random image
        img_url, img_alt = random.choice(IMAGES)
        components.append(bt.Text("Here's a random image for you:"))
        components.append(bt.Image(img_url, alt=img_alt))
    
    # Code example
    components.append(bt.Markdown("""
### 💻 Code Example

Here's how you can create your own bot:

```python
import bubbletea as bt

@bt.chatbot
def my_bot(message: str):
    yield bt.Text("Hello from my bot!")
    yield bt.Image("https://example.com/image.jpg")
    yield bt.Markdown("# Amazing!")
```
    """))
    
    # Interactive elements
    components.append(bt.Text("Want to try something specific? Try sending: 'tech', 'nature', or 'help'"))
    
    # Footer
    components.append(bt.Markdown("""
---
*This response was generated in non-streaming mode. All components were sent at once!* 🚀
    """))
    
    return components


if __name__ == "__main__":
    bt.run_server(multimodal_bot, port=8003)