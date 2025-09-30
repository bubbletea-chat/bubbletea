# Building a Bot

## Table of Contents
- [API Reference](#api-reference)
- [Components](#components)
- [Streaming Responses](#streaming-responses)
- [Context - User & Conversation Tracking](#context---user--conversation-tracking)
- [Thread-based Conversation Support](#thread-based-conversation-support)
- [Multiple Bots with Configurations](#multiple-bots-with-configurations)
- [Environment Variables](#environment-variables)
- [Swagger API Documentation](#swagger-api-documentation)
- [LiteLLM Integration](#litellm-integration)
- [Using Bubbletea with Other Languages](#using-bubbletea-with-other-languages)

## API Reference

The Bubbletea API lets you programmatically manage your bots through subaccounts. To get started:

1. Go to https://bubbletea.chat
2. Sign in with your Bubbletea account
3. Navigate to Settings → API Keys
4. Your API key will be displayed
5. Click the copy button to copy your API key
6. You can copy your API key anytime from the dashboard

*Note: Keep your API key secret. You can always access and copy it again from the subaccount dashboard. If compromised, regenerate it immediately.*

### Authentication

All API requests require your API key in the X-API-Key header:

```bash
# Add this header to all requests
-H "X-API-Key: your-api-key-here"
```

### Get Account Profile

Retrieve your account information

```bash
curl -X GET https://backend.bubbletea.chat/v1/profile \
  -H "X-API-Key: your-api-key-here"
```

### Create Bot

Register a new bot with Bubbletea

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/bots \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-bot",
    "display_name": "My Bot",
    "api_url": "https://my-bot.example.com",
    "stream": true,
    "emoji": "🤖",
    "subtitle": "An awesome bot",
    "description": "This bot does amazing things",
    "initial_text": "Hello! How can I help you?",
    "visibility": "public",
    "authorization": "none",
    "subscription_monthly_price": 0
  }'
```

### List Your Bots

Get all bots you've created

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots \
  -H "X-API-Key: your-api-key-here"
```

### Get Bot Details

Retrieve specific bot configuration

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots/my-bot \
  -H "X-API-Key: your-api-key-here"
```

### Update Bot

Modify bot configuration

```bash
curl -X PUT https://backend.bubbletea.chat/v1/developer/bots/my-bot \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "display_name": "My Updated Bot",
    "subtitle": "Now even better!",
    "description": "Updated description",
    "emoji": "🚀"
  }'
```

### Refresh Bot Config

Sync bot configuration from its API URL

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/bots/my-bot/refresh-config \
  -H "X-API-Key: your-api-key-here"
```

### Delete Bot

Remove a bot from Bubbletea

```bash
curl -X DELETE https://backend.bubbletea.chat/v1/developer/bots/my-bot \
  -H "X-API-Key: your-api-key-here"
```

### List Bot Conversations

Get all conversations for your bot

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots/my-bot/conversations \
  -H "X-API-Key: your-api-key-here"
```

### Get Conversation Messages

Retrieve all messages from a conversation

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/conversations/{conversation-uuid}/messages \
  -H "X-API-Key: your-api-key-here"
```

### Test Bot

Send a test message to your bot

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/bots/my-bot/test \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, bot!"
  }'
```

### Create Conversation

Create a new conversation between a user and your bot

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/conversations/create \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "user_uuid": "user-uuid-here",
    "bot_name": "my-bot"
  }'
```

### Create Message in Conversation

Add a new message to an existing conversation

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/conversation/{conversation-uuid}/message \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "type": "text",
      "text": "Hello from user!"
    },
    "sender": "user",
    "sender_account_id": "user-account-id"
  }'
```

### Create Bot Message

Send a message as the bot in a conversation

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/conversation/{conversation-uuid}/bot-message \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "text",
    "text": "Hello from bot!"
  }'
```

**💡 Pro Tip:** Use the conversation APIs to build integrations, webhooks, or custom chat experiences. You can programmatically create conversations and send messages on behalf of users or your bots.

## Components

Bubbletea provides a rich set of UI components that let your bot communicate beyond plain text. Each component is designed for specific use cases. Here's each component with detailed examples:

### 💬 Text Component

Simple text messages for basic communication. The foundation of all bot responses.

```python
import bubbletea_chat as bt

# Simple text message
return bt.Text("Hello, world!")

# Multiple text messages
return [bt.Text("Processing your request..."), bt.Text("Done! Here are the results.")]
```

### 📝 Markdown Component

Rich formatted text with full Markdown support including bold, italic, lists, and more.

```python
# Markdown with rich formatting
return bt.Markdown("""
# Heading
**Bold text** and *italic text*

- Bullet point 1
- Bullet point 2

1. Numbered list
2. Second item

```python
# Code blocks supported
print("Hello")
```


### 🎨 Image Component

Display images with optional alt text for accessibility.

```python
# Display an image
return bt.Image(
    url="https://picsum.photos/300/200",
    alt="A beautiful sunset"
)
```

### 🎬 Video Component

Embed videos with built-in player controls.

```python
# Embed a video
return bt.Video(
    url="https://www.w3schools.com/html/mov_bbb.mp4"
)

# Video with context
return [bt.Text("Watch this tutorial:"), bt.Video("https://example.com/demo.mp4")]
```

### 🎴 Card Component

Interactive cards combining images and text with click actions.

```python
# Single card
return bt.Card(
    image=bt.Image(url="https://example.com/product.jpg"),
    text="Premium Plan",
    card_value="premium_selected"
)

# Multiple cards
return bt.Cards(cards=[
    bt.Card(
        image=bt.Image(url="https://example.com/basic.jpg"),
        text="Basic Plan - $9/month",
        card_value="basic"
    ),
    bt.Card(
        image=bt.Image(url="https://example.com/pro.jpg"),
        text="Pro Plan - $19/month",
        card_value="pro"
    )
], orient="tall")  # or "tall" for vertical layout
```

### 💊 Pills Component

Quick action buttons for user selections and choices.

```python
# Quick selection pills
return bt.Pills(pills=[
    bt.Pill(text="Yes", pill_value="yes_selected"),
    bt.Pill(text="No", pill_value="no_selected"),
    bt.Pill(text="Maybe", pill_value="maybe_selected")
])

# Category selection
return bt.Text("Choose a category:")
return bt.Pills(pills=[
    bt.Pill(text="🏠 Home", pill_value="home"),
    bt.Pill(text="💼 Work", pill_value="work"),
    bt.Pill(text="🎮 Gaming", pill_value="gaming"),
    bt.Pill(text="📚 Education", pill_value="education")
])
```

### ⚠️ Error Component

Display error messages with proper styling and optional error codes.

```python
# Simple error
return bt.Error(
    title="Connection Failed",
    description="Unable to connect to the server",
    code="ERR_CONNECTION"
)

# Error without description
return bt.Error(
    title="Invalid Input",
    code="ERR_VALIDATION"
)

# Detailed error
return bt.Error(
    title="Payment Failed",
    description="Your card was declined. Please try another payment method.",
    code="PAY_001"
)
```

### ⏳ Block Component

Loading indicator for long-running operations. Automatically replaced when next component is yielded.

```python
# Show loading while processing
return bt.Block(timeout=30)  # 30 second timeout

# Simulate long operation
import time
time.sleep(5)

# This replaces the loading indicator
return bt.Text("Processing complete!")

# Example with async operation
return bt.Block(timeout=60)
result = await fetch_data()  # Long operation
return bt.Text(f"Results: {result}")
```

## Streaming Responses

Streaming provides a better user experience by showing responses as they're generated, rather than waiting for the complete answer. Users see immediate feedback and can read while the bot continues thinking. This is especially important for longer responses:

```python
@bt.chatbot(stream=True)
async def stream_bot(message: str):
    # Show loading indicator
    return bt.Block(timeout=1000)

    # Stream response chunks
    llm = LLM(model="gpt-4")
    async for chunk in llm.stream(message):
        yield bt.Text(chunk)
```

## Context - User & Conversation Tracking

Bubbletea automatically provides context about users and conversations. This lets your bot maintain state, personalize responses, and track conversation history. Every message includes optional context parameters you can use:

```python
@bt.chatbot
def contextual_bot(message: str, user_uuid: str = None,
                  conversation_uuid: str = None,
                  user_email: str = None):
    # Access user and conversation context
    response = f"Message: {message}"
    if user_uuid:
        response += f"\nUser: {user_uuid}"
    if conversation_uuid:
        response += f"\nConversation: {conversation_uuid}"
    if user_email:
        response += f"\nEmail: {user_email}"

    return bt.Text(response)
```

## Thread-based Conversation Support

Bubbletea automatically organizes chats into conversation threads, similar to popular messaging apps. Each conversation maintains its own context and history, allowing users to have multiple independent chats with the same bot. This is perfect for complex, multi-turn interactions:

```python
# Each conversation gets a unique ID
# Messages are grouped by conversation
# Context persists within a conversation
# Users can have multiple conversations

@bt.chatbot
def bot_with_memory(message: str,
                    conversation_uuid: str):
    # Access conversation history if needed
    # Bubbletea handles the persistence
    return bt.Text(f"Conversation: {conversation_uuid}")
```

## Multiple Bots with Configurations

You can run multiple bots in the same application, each with its own unique route and configuration. This is perfect for creating specialized bots for different purposes like support, sales, and general assistance:

```python
import bubbletea_chat as bt

# Configuration for Support Bot
@bt.config("support")
def support_config():
    return bt.BotConfig(
        name="support-bot",
        url="https://your-bot.com/support",
        is_streaming=True,
        display_name="Support Assistant",
        subtitle="24/7 Technical Support",
        icon_emoji="🛟",
        description="Get help with technical issues",
        initial_text="Hello! How can I help you today?"
    )

# Support Bot at /support
@bt.chatbot("support")
def support_bot(message: str, user_email: str = None):
    if user_email:
        return bt.Text(f"Hi {user_email}! Let me help with that.")
    return bt.Text("How can I help you today?")

# Configuration for Sales Bot
@bt.config("sales")
def sales_config():
    return bt.BotConfig(
        name="sales-bot",
        url="https://your-bot.com/sales",
        is_streaming=False,
        display_name="Sales Assistant",
        subtitle="Product Info & Pricing",
        icon_emoji="💼",
        description="Learn about our products",
        subscription_monthly_price=999,  # $9.99/month
        initial_text="Welcome! Looking for the perfect plan?"
    )

# Sales Bot at /sales
@bt.chatbot("sales")
def sales_bot(message: str, subscription_status: str = None):
    if subscription_status == "active":
        return bt.Text("As a premium member, you get 20% off!")
    return bt.Text("Let me help you find the perfect plan!")

# Configuration for General Bot (default)
@bt.config()
def general_config():
    return bt.BotConfig(
        name="general-assistant",
        url="https://your-bot.com",
        is_streaming=True,
        display_name="General Assistant",
        subtitle="Your AI Helper",
        icon_emoji="🤖",
        description="General-purpose assistant"
    )

# General Bot at /chat (default)
@bt.chatbot()
def general_bot(message: str):
    return bt.Text("Hello! I'm your general assistant.")

if __name__ == "__main__":
    # Run all registered bots
    bt.run_server(port=8000)

    # Or run specific bots only
    # bt.run_server([support_bot, sales_bot], port=8000)
```

**Configuration Endpoints:** Each bot's configuration is accessible at its route + /config:

- /support → Bot endpoint | /support/config → Configuration
- /sales → Bot endpoint | /sales/config → Configuration
- /chat → Default bot | /config → Default configuration

**Important:** Configuration decorator route must match chatbot decorator route. Each bot maintains its own independent configuration and can have different settings for streaming, authentication, pricing, and UI appearance.

## Environment Variables

Keep your API keys and configuration secure using environment variables. Never hardcode sensitive information in your source code. Create a .env file in your project root (and add it to .gitignore) to manage your bot's settings:

```bash
# .env file for your bot

# LLM API Keys (optional, for AI features)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...

# Bubbletea Settings
BOT_PORT=8000
BOT_HOST=0.0.0.0

# Your bot's public URL (for registration)
BOT_URL=https://your-bot.ngrok.io
```

## Swagger API Documentation

When you run your bot server, automatic API documentation is available via Swagger UI. This interactive documentation lets you explore and test all endpoints directly in your browser:

```bash
# Start your bot server
python my_bot.py

# Access Swagger UI at:
https://your-bot.com/docs

# Interactive API documentation includes:
# - All available endpoints
# - Request/response schemas
# - Try it out functionality
# - Authentication requirements
```

Swagger UI provides a complete reference for your bot's API, making it easy to test endpoints and understand the expected formats.

## LiteLLM Integration

LiteLLM gives you instant access to 100+ language models through a single, unified interface. Switch between OpenAI, Anthropic, Google, and open-source models with just one line of code. This flexibility lets you choose the best model for each task without rewriting your bot:

```python
from bubbletea_chat import LLM

# Use any model via LiteLLM
llm = LLM(model="gpt-4")
llm = LLM(model="claude-3-opus-20240229")
llm = LLM(model="gemini/gemini-pro")

# Generate responses
response = await llm.acomplete("Hello!")

# Stream responses
async for chunk in llm.stream("Tell me a story"):
    yield bt.Text(chunk)
```

**Using Multiple LLMs in One Bot**

Combine different AI models in a single bot to leverage each model's strengths. Use DALL-E for images, Claude for code, GPT-4 for general chat, or any combination that fits your needs:

```python
# Mix different LLMs in one bot
@bt.chatbot
async def multi_llm_bot(message: str):
    if "image" in message:
        # Use DALL-E for images
        llm = LLM(model="dall-e-3")
        url = await llm.agenerate_image(message)
        return bt.Image(url)
    elif "code" in message:
        # Use Claude for code
        llm = LLM(model="claude-3-opus-20240229")
        response = await llm.acomplete(message)
        return bt.Markdown(f"```python\n{response}\n```")
    else:
        # Use GPT-4 for general chat
        llm = LLM(model="gpt-4")
        response = await llm.acomplete(message)
        return bt.Text(response)
```

## Using Bubbletea with Other Languages

While we provide an official Python SDK, Bubbletea works with any programming language that can create HTTP endpoints. All you need to do is implement the chat endpoint that returns the correct response format. Here's how to build a Bubbletea bot in JavaScript/Node.js:

```javascript
// server.js
const express = require('express');
const app = express();

app.use(express.json());

app.post('/chat', async (req, res) => {
  const { message, user_uuid, conversation_uuid } = req.body;

  // Your bot logic here
  const response = await processMessage(message);

  // Return Bubbletea-compatible response format
  res.json({
    responses: [{
      payload: [{
        type: "text",
        content: response
      }]
    }]
  });
});

app.listen(3000, () => {
  console.log('Bot running on port 3000');
});
```

Other supported languages:
• Python (SDK available)
• JavaScript/TypeScript
• Go
• Rust
• Java
• Any language with HTTP support