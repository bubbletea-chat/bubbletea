# Documentation

## Introduction

### 1. Intro Concept - Frontend for your AI Agent

Bubbletea is the **frontend platform for AI agents & chatbots**. Share your AI creations with the world through beautiful, instant chat interfaces. Build your bot in any language, host it anywhere, and Bubbletea provides the user interface.

- No frontend development needed
- Share bots with simple URLs
- Professional UI out of the box
- Built-in user management & history

### 2. Quickstart - E2E Echobot

Get your first bot running in minutes. This complete example shows you how to build, deploy, and share a working chatbot in just 3 steps.

**🎬 Video Demonstration**

Watch this step-by-step video guide that walks you through the entire process:
[Bubbletea Quickstart Tutorial](https://www.youtube.com/embed/Op5cbkJylm8)

#### Step 1: Create an Echo Bot

First, install the Bubbletea SDK and create a simple bot that echoes messages back to users. The @bt.chatbot decorator automatically handles all the HTTP endpoint setup for you.

```python
# Install SDK with LLM support
pip install 'bubbletea-chat[llm]'

# echobot.py
import bubbletea_chat as bt

@bt.chatbot
def echo_bot(message: str):
    # Simple echo bot
    return bt.Text(f"Echo: {message}")

if __name__ == "__main__":
    # Creates /chat endpoint automatically
    bt.run_server(echo_bot, port=8000, host="0.0.0.0")
```

#### Step 2: Deploy with ngrok or Replit

Now make your bot accessible from the internet. Choose either ngrok for local development or Replit for instant cloud hosting. Both options are free and take less than a minute to set up.

**Option A: Deploy with ngrok (Local Development)**

```bash
# Install ngrok: https://ngrok.com/download
# Start your bot locally
python echobot.py

# In another terminal, expose it to internet
ngrok http 8000

# Your bot URL will be: https://abc123.ngrok-free.app
```

**Option B: Deploy on Replit (Cloud Hosting)**

Replit provides free, always-on hosting with zero configuration:

- Go to [replit.com](https://replit.com) and create a new Python repl
- Copy your bot code into main.py
- Click "Run" to start your bot
- Get instant URL: https://your-bot.username.repl.co
- Free hosting, SSL included, always online
- Click "Deploy" button and ensure deployment type is set to "Public"

#### Step 3: Register Your Bot & Access Everywhere

Finally, register your bot through the Dashboard to make it accessible to users:

- Go to [https://bubbletea.chat](https://bubbletea.chat)
- Create or select a subaccount for your bot
- Use BT Agent or the dashboard UI to register your bot

Your bot is now accessible at:
- 🌐 Web: https://bubbletea.chat/echobot
- 📱 iOS & Android: Bubbletea mobile app

---

## Components / Package

### 1. Bot Configuration

Every bot needs configuration to tell Bubbletea how to display and interact with it. The @config decorator defines your bot's identity, appearance, and behavior. This configuration is what users see when browsing available bots:

```python
import bubbletea_chat as bt

@bt.config()
def get_config():
    return bt.BotConfig(
        # REQUIRED FIELDS (Must be provided)
        name="your-bot",                 # URL-safe handle (no spaces, lowercase)
                                         # Pattern: ^[a-zA-Z0-9_-]+$
                                         # Used in URLs: bubbletea.chat/weather-bot
        
        url="https://your-bot.com/chat", # Your bot's endpoint URL
                                         # Where your bot is hosted
        
        is_streaming=False,              # Whether bot supports streaming
                                         # True if using yield, False for return
        
        # APP STORE METADATA
        display_name="Weather Bot",      # User-facing name (max 20 chars)
                                         # Shown in bot cards and headers
        
        subtitle="Real-time weather",    # Brief tagline (max 30 chars)
                                         # Appears under display name
        
        icon_url="https://...",          # 1024x1024 PNG icon URL
                                         # Bot's profile picture (HTTPS required)
        
        icon_emoji="🌤️",                 # Emoji icon alternative
                                         # Used if icon_url not provided (max 10 chars)
        
        preview_video_url="https://...", # Demo video URL (HTTPS required)
                                         # Shows bot capabilities
        
        description="Get accurate weather forecasts worldwide.",
                                         # Full Markdown description
                                         # Supports **bold**, *italic*, etc.
        
        example_chats=[                  # Sample example chats from bubbletea
            "https://bubbletea.chat/chat/your-bot/shared/token-generated",
            "https://bubbletea.chat/chat/your-bot/shared/token-generated"
        ],
        
        discoverable=True,               # Show in Bot Discovery page
                                         # False to hide from listings
        
        entrypoint="/weather",           # Launch context/action (optional)
                                         # Initial page or command
        
        # ACCESS CONTROL
        visibility="public",             # Bot visibility: "public" or "private"
                                         # Controls who can access the bot
        
        authorized_emails=[              # Whitelist for private bots
            "user@example.com",          # Only these emails can access
            "team@company.com"           # if visibility="private"
        ],
        
        # SUBSCRIPTION & PAYMENT
        subscription_monthly_price=0,    # Monthly price in cents
                                         # 0 = free
                                         # 499 = $4.99/month
                                         # 999 = $9.99/month
        
        # USER EXPERIENCE
        initial_text="Hello! Which city's weather would you like?",
                                         # First message shown to users
                                         # Sets the conversation tone
        
        # ADVANCED CONFIGURATION
        cors_config={                    # Custom CORS settings (optional)
            "allow_origins": ["*"],      # Override default CORS
            "allow_credentials": True,
            "allow_methods": ["GET", "POST"],
            "allow_headers": ["*"]
        },
    )
```

### 2. Components

Bubbletea provides a rich set of UI components that let your bot communicate beyond plain text. Each component is designed for specific use cases. Here's each component with detailed examples:

#### 💬 Text Component

Simple text messages for basic communication. The foundation of all bot responses.

```python
import bubbletea_chat as bt

# Simple text message
return bt.Text("Hello, world!")

# Multiple text messages
return [bt.Text("Processing your request..."), bt.Text("Done! Here are the results.")]
```

#### 📝 Markdown Component

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


#### 🎨 Image Component

Display images with optional alt text for accessibility.

```python
# Display an image
return bt.Image(
    url="https://picsum.photos/300/200",
    alt="A beautiful sunset"
)
```

#### 🎬 Video Component

Embed videos with built-in player controls.

```python
# Embed a video
return bt.Video(
    url="https://www.w3schools.com/html/mov_bbb.mp4"
)

# Video with context
return [bt.Text("Watch this tutorial:"), bt.Video("https://example.com/demo.mp4")]
```

#### 🎴 Card Component

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

#### 💊 Pills Component

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

#### ⚠️ Error Component

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

#### ⏳ Block Component

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

### 3. Streaming Responses

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

### 4. Context - User & Conversation Tracking

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

### 5. Thread-based Conversation Support

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

### 6. Multiple Bots with Configurations

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

### 7. Environment Variables

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

### 8. Swagger API Documentation

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

### 9. API Reference

The API lets you programmatically manage your bots and subaccounts. To get started:

1. Go to https://bubbletea.chat
2. Sign in with your Bubbletea account
3. Navigate to Settings → API Keys
4. Create a new API key for your account or subaccount
5. Copy and store your API key securely

*Note: Keep your API key secret. You can regenerate it anytime from the dashboard if compromised.*

#### Authentication

All API requests require your API key in the X-API-Key header:

```bash
# Add this header to all requests
-H "X-API-Key: your-api-key-here"
```

#### Get Developer Profile

Retrieve your developer account information

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/profile \
  -H "X-API-Key: your-api-key-here"
```

#### Create Bot

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

#### List Your Bots

Get all bots you've created

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots \
  -H "X-API-Key: your-api-key-here"
```

#### Get Bot Details

Retrieve specific bot configuration

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots/my-bot \
  -H "X-API-Key: your-api-key-here"
```

#### Update Bot

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

#### Refresh Bot Config

Sync bot configuration from its API URL

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/bots/my-bot/refresh-config \
  -H "X-API-Key: your-api-key-here"
```

#### Delete Bot

Remove a bot from Bubbletea

```bash
curl -X DELETE https://backend.bubbletea.chat/v1/developer/bots/my-bot \
  -H "X-API-Key: your-api-key-here"
```

#### List Bot Conversations

Get all conversations for your bot

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/bots/my-bot/conversations \
  -H "X-API-Key: your-api-key-here"
```

#### Get Conversation Messages

Retrieve all messages from a conversation

```bash
curl -X GET https://backend.bubbletea.chat/v1/developer/conversations/{conversation-uuid}/messages \
  -H "X-API-Key: your-api-key-here"
```

#### Test Bot

Send a test message to your bot

```bash
curl -X POST https://backend.bubbletea.chat/v1/developer/bots/my-bot/test \
  -H "X-API-Key: your-api-key-here" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello, bot!"
  }'
```

### 10. LiteLLM Integration

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

---

## Subaccounts

### Organize Your Bots with Subaccounts

Subaccounts allow you to organize and manage multiple bots under a single parent account. Each subaccount operates independently with its own bots, settings, and API keys, while the parent account maintains full oversight and control.

#### Parent Account & Subaccount Relationship
- **Parent Account**: Your main account that can create and manage multiple subaccounts
- **Subaccounts**: Child accounts under your parent that isolate bots and resources
- **Hierarchy**: Parent → Subaccounts → Bots (each bot belongs to one subaccount)
- **Access Control**: Parent account has full access to all subaccounts and their bots

#### Key Features
- **Project Organization**: Group bots by project, client, or environment
- **Isolated API Keys**: Each subaccount has its own API key for enhanced security
- **Usage Tracking**: Monitor usage and billing per subaccount
- **Easy Switching**: Switch between accounts seamlessly in the dashboard
- **Parent Oversight**: Parent account can view and manage all subaccounts

#### Parent Account Capabilities
The parent account has special privileges:
- **Create/Delete Subaccounts**: Manage the lifecycle of all subaccounts
- **Access All Bots**: View and manage bots across all subaccounts
- **Consolidated Billing**: All subaccount usage is billed to the parent
- **Global API Key**: Parent API key can access any subaccount's resources
- **Usage Analytics**: View aggregated metrics across all subaccounts
- **Transfer Bots**: Move bots between subaccounts as needed

#### Creating a Subaccount
1. Navigate to [bubbletea.chat](https://bubbletea.chat)
2. Click on your profile menu
3. Select "Manage Subaccounts"
4. Click "Create New Subaccount"
5. Enter a unique handle for your subaccount
6. Your subaccount is ready to use!
7. Switch to the subaccount to start adding bot(each subaccount can have 1)


## Deploying Bots

### 1. Ngrok - Local Development Made Easy

Ngrok is the fastest way to test your bot during development. It creates a secure tunnel from the internet to your local machine, giving you a public URL instantly. Perfect for testing and debugging before deploying to production:

```bash
# Step 1: Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Step 2: Start your bot
python your_bot.py

# Step 3: Expose to internet
ngrok http 8000

# Your bot is now accessible at:
# https://abc123.ngrok.io
```

### 2. Replit - Instant Cloud Hosting

Replit provides free, always-on hosting for your bot with zero configuration. Just write your code in the browser and click Run. No server setup, no deployment scripts, no DevOps knowledge required. Your bot gets a permanent URL and stays online 24/7:

```bash
# 1. Fork the Bubbletea template on Replit
# 2. Add your bot code to main.py
# 3. Click "Run"
# 4. Your bot URL: https://botname.username.repl.co

# Replit automatically handles:
# - SSL certificates
# - Always-on hosting
# - Environment variables
```

### 3. CORS Support - Cross-Origin Configuration

CORS (Cross-Origin Resource Sharing) allows Bubbletea's frontend to communicate with your bot's backend. The SDK handles this automatically, but if you're building a custom implementation, you'll need to configure CORS headers properly:

```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Testing Your Bot

Before registering with Bubbletea, test your bot locally to ensure it's working correctly. Use these curl commands to verify your endpoints are responding properly. Each test simulates what Bubbletea will send to your bot:

```bash
# Test your bot endpoint
curl -X POST https://your-bot.com/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "message": "Hello"}'

# Test config endpoint
curl https://your-bot.com/config

# Test with images
curl -X POST https://your-bot.com/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "message": "What is this?",
       "images": [{"url": "https://example.com/img.jpg"}]}'
```

---

## Examples / Showcase / What can you build?

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

---

## Dashboard

The Bubbletea Dashboard is your central command center for managing bots, monitoring usage, and configuring settings. Access it at:

**Dashboard URL:**
- 🌐 Main Dashboard: https://bubbletea.chat

The dashboard provides everything you need to run successful AI bots:
---

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

---

## Contributing / License

Bubbletea is open source and welcomes contributions from the community! Whether you're fixing bugs, adding features, improving documentation, or creating example bots, your contributions help make Bubbletea better for everyone. Join our growing community of contributors:

### How to Contribute

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### License

MIT License - See LICENSE file for details

[View on GitHub](https://github.com/bubbletea-chat/bubbletea) | [Report Issue](https://github.com/bubbletea-chat/bubbletea/issues)
