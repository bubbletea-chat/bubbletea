# Managing a Bot

## Table of Contents
- [Dashboard](#dashboard)
- [Examples & Showcase](#examples--showcase)
- [Contributing & License](#contributing--license)

## Dashboard

The Bubbletea Dashboard is your central command center for managing bots, monitoring usage, and configuring settings. Access it at:

**Dashboard URL:**
- 🌐 Main Dashboard: https://bubbletea.chat

The dashboard provides everything you need to run successful AI bots:

## Examples & Showcase

Bubbletea empowers you to build any type of AI bot - from simple utilities to complex agents. Here are some popular examples with complete code you can copy and customize. Each example demonstrates different capabilities and best practices:

### 🎨 Image Generation Bot

Create stunning images from text descriptions using DALL-E 3. This bot transforms your ideas into visual art instantly. Perfect for creative projects, marketing materials, or just having fun:

```python
@bt.chatbot
async def art_bot(message: str):
    llm = LLM(model="dall-e-3")

    # Generate image from prompt
    image_url = await llm.agenerate_image(message)

    # Return the generated image
    return [bt.Image(image_url), bt.Text("Your image is ready!")]
```

### 👁️ Vision Analyzer

Analyze images and answer questions about visual content using GPT-4 Vision. This bot can describe images, identify objects, read text in images, and answer specific questions about what it sees:

```python
@bt.chatbot
async def vision_bot(message: str, images: list = None):
    if images:
        # Analyze images with GPT-4 Vision
        llm = LLM(model="gpt-4-vision-preview")
        response = await llm.acomplete_with_images(
            message, images
        )
        return bt.Markdown(response)
    else:
        return bt.Text("Please upload an image to analyze")
```

### 🤖 Multiple Specialized Bots

Create multiple bots in one application, each specialized for different tasks. Perfect for businesses that need separate customer support, sales, and general assistance bots:

```python
# Run multiple bots with unique configurations
@bt.config()
def tech_support_config():
    return bt.BotConfig(
        name="tech-support",
        display_name="Tech Support",
        icon_emoji="🔧",
        initial_text="Technical support here!"
    )

@bt.chatbot("tech-support")
def tech_bot(message: str):
    return bt.Text("Let me help with that technical issue...")

@bt.config()
def sales_config():
    return bt.BotConfig(
        name="sales",
        display_name="Sales Assistant",
        icon_emoji="💼",
        subscription_monthly_price=999  # Premium bot
    )

@bt.chatbot("sales")
def sales_bot(message: str):
    return bt.Text("I can help you find the perfect solution!")

# Run all bots on one server
bt.run_server(port=8000)
```

### 📦 Multi-Modal Showcase Bot

Showcase all of Bubbletea's UI components in one bot. This example demonstrates how to combine text, markdown, images, cards, and interactive elements to create rich, engaging conversations:

```python
@bt.chatbot
async def multimodal_bot(message: str):
    return [bt.Markdown("# Welcome!"), bt.Text("I can show different content types:")

    , bt.Markdown("""
    - 📝 **Text** messages
    - 🎨 **Images** and media
    - 📊 **Cards** with actions
    """),
     bt.Cards(cards=[
        bt.Card(
            image=bt.Image(url="https://picsum.photos/400/300"),
            text="Example Card",
            card_value="card_1"
        )
          ])]
```

## Contributing & License

Bubbletea is open source and welcomes contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or creating example bots, your contributions help make Bubbletea better for everyone. Join our growing community of contributors:

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### License

MIT License - See LICENSE file for details

[View on GitHub](https://github.com/bubbletea-chat/bubbletea) | [Report Issue](https://github.com/bubbletea-chat/bubbletea/issues)