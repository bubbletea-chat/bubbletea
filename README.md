# BubbleTea

[![Python 3.9+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-bubbletea.chat-purple.svg)](https://bubbletea.chat)

> Platform for Developers

**The Frontend Platform for AI Agents & Chatbots**

Share your AI creations with the world through beautiful, instant chat interfaces.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Quick Start Guide](#quick-start-guide)
- [How to Use](#how-to-use)
- [Types of Bots](#types-of-bots)
- [Developer Tools](#developer-tools)
- [API Reference](#api-reference)
- [Deployment Guide](#deployment-guide)
- [Examples](#examples)
- [Component Documentation](#component-documentation)
- [Troubleshooting Guide](#troubleshooting-guide)
- [Performance Best Practices](#performance-best-practices)
- [Security Guidelines](#security-guidelines)
- [FAQ](#faq)
- [Community & Support](#community--support)

---

## Quick Start Guide

### 🚀 Build Your First Bot in 5 Minutes

Get your AI bot live on the web in just a few steps:

#### Step 1: Install the SDK
```bash
pip install bubbletea-chat
```

#### Step 2: Create Your Bot
Create a file `my_first_bot.py`:

```python
from bubbletea_chat import bt

@bt.chatbot
async def echo_bot(message: str):
    """A simple bot that echoes messages"""
    yield bt.Text(f"You said: {message}")
    yield bt.Text("I'm your first BubbleTea bot! 🎉")

if __name__ == "__main__":
    bt.run_server(echo_bot, port=8000)
```

#### Step 3: Run Your Bot
```bash
python my_first_bot.py
# Your bot is now running at http://localhost:8000
```
---

## Overview

### What is BubbleTea?

BubbleTea is a frontend platform that gives your AI agents and chatbots a home on the web. Think of it as the "user interface layer" for AI - where developers can instantly share their creations with the world through beautiful, accessible chat interfaces.

### 🎯 Core Purpose

- **Instant web interface for any AI bot** - Get a professional chat UI without writing frontend code
- **Share bots via simple URLs** - Each bot gets its own public URL at `bubbletea.chat/your-bot-name`
- **Unified chat experience for users** - Consistent, polished interface across all bots
- **Conversation history & user dashboard** - Users can access all their chats in one place

### 💡 Key Benefits

- **No frontend development needed** - Focus on your bot's logic, not UI code
- **Professional UI out of the box** - Mobile-friendly, accessible, and beautiful
- **Focus on AI logic, not UI code** - Build in any language, deploy anywhere
- **Built-in user management** - Authentication, sessions, and history handled for you

> **Note:** BubbleTea backend follows specific standards for bot integration. Check out the [Developer Tools](#developer-tools) section to learn about the API specifications and SDK.

### Bot Flow

Your bot connects to a foundational model, and probably contains some unique agentic functionality. It then connects to BubbleTea's API, which in turn, connects to a frontend.

### Who Benefits?

#### 🤖 For Bot Creators
Build your AI bot in any language, host it anywhere, and BubbleTea provides the chat interface

#### 🌍 For End Users
Access all your favorite AI bots in one place with a consistent, beautiful interface

#### 🛡️ Platform Benefits
Secure authentication, conversation history, and a unified dashboard for all interactions

---

## How to Use

### Getting Started with BubbleTea

Your journey from sign-up to sharing your first bot.

#### 1️⃣ Sign Up with Email
Enter your email address and we'll send you a verification code. No passwords needed!

**What happens next:**
- You'll receive a 6-digit verification code via email
- Enter the code to access your dashboard
- Your account is automatically created with secure authentication

[Sign Up Now →](https://bubbletea.chat/)

#### 2️⃣ Quickstart - E2E Echobot
Get your first bot running in minutes. This complete example shows you how to build, deploy, and share a working chatbot in just 3 steps.

**Step 1: Create an Echo Bot**

First, install the Bubbletea SDK and create a simple bot that echoes messages back to users. The @bt.chatbot decorator automatically handles all the HTTP endpoint setup for you.
```
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

```
# Install ngrok: https://ngrok.com/download
# Start your bot locally
python echobot.py

# In another terminal, expose it to internet
ngrok http 8000

# Your bot URL will be: https://abc123.ngrok-free.app
```

**URL Features:**
#### Option B: Deploy on Replit (Cloud Hosting)
- Replit provides free, always-on hosting with zero configuration:
- Go to replit.com and create a new Python repl
- Copy your bot code into main.py
- Click "Run" to start your bot
- Get instant URL: https://your-bot.username.repl.co
- Free hosting, SSL included, always online
- Click "Deploy" button and ensure deployment type is set to "Public"

#### Step 3: Register Your Bot & Access Everywhere

Finally, register your bot through the Developer Dashboard to make it accessible to users:


- Go to https://bubbletea.chat/developer
- Enable Developer Mode to get your API key
- Use the API or dashboard UI to register your bot
- Your bot is now accessible at:
- 🌐 Web: https://bubbletea.chat/echobot
- 📱 iOS & Android: Bubbletea mobile app

**Dashboard Features:**
- View all chat histories in one place
- Search through past conversations
- Export chat data for analysis
- Monitor bot usage statistics
- Manage multiple bots from a single interface


## Types of Bots

### Types of Bots You Can Build

BubbleTea supports any type of AI bot - from simple chatbots to complex AI agents.

#### 💬 Conversational Assistants
Build Q&A bots, customer support agents, or personal assistants that can understand context and provide helpful responses.

**Examples:** FAQ bots, documentation assistants, language tutors

#### ✨ Creative AI Tools
Create bots that generate images, write stories, compose music, or help with creative projects.

**Examples:** Image generators, story writers, code assistants

#### ⚡ Task Automation Bots
Automate workflows, integrate with APIs, or perform complex multi-step tasks through conversation.

**Examples:** Data analysis bots, API integrators, workflow automators

#### 🌐 Specialized Domain Experts
Deploy bots with deep knowledge in specific fields like medicine, law, finance, or education.

**Examples:** Medical advisors, legal assistants, financial analysts

> **The best part?** You can build your bot in any language, using any framework. BubbleTea provides the chat interface so you can focus on your bot's unique capabilities.

### Bot Capabilities

#### What Your Bots Can Do
- Process text, images, and files
- Stream responses in real-time
- Maintain conversation context
- Integrate with external APIs

#### Rich Response Types
- Plain text and markdown
- Images and media
- Code blocks with syntax highlighting
- Custom UI components

---

## Developer Tools

### Tools for Building AI Bots & Agents

Everything you need to create bots that seamlessly integrate with BubbleTea's frontend.

These developer tools simplify the process of creating AI bots and agents that work perfectly with BubbleTea's chat interface. Build once, deploy anywhere, and let BubbleTea handle the user experience.

### 📦 Python SDK

Build powerful AI bots with our feature-rich Python SDK.

#### 🚀 Quick Start

```bash
# Install the SDK
pip install bubbletea-chat

# Create your first bot
from bubbletea_chat import bt

@bt.chatbot
async def my_bot(message: str):
    yield bt.Text(f"You said: {message}")

```

**What this code does:**
- `@bt.chatbot` - Decorator that transforms your function into a chat endpoint
- `message: str` - Receives user messages as input
- `yield bt.Text()` - Sends responses back to the user
- Supports async/await for non-blocking operations

#### 🖥️ Server Setup
```python
if __name__ == "__main__":
    # Run the server
    bt.run_server(my_bot, port=8000)
```

**Server Features:**
- Runs the chatbot server on port 8000
- Automatically creates a `/chat` endpoint for your bot
- The `/chat` endpoint accepts POST requests with chat messages
- Supports both streaming and non-streaming responses
- Built-in CORS support for web integration
- Automatic error handling and logging
- Health check endpoint at `/health`

**Testing Your Bot Locally:**
```bash
# Start your bot
python my_bot.py

# Test with curl (in another terminal)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello bot!"}'
```



## 🤖 LLM Integration

#### 🔧 Environment Variables

To use different LLM (Large Language Model) providers, set the appropriate API keys as environment variables:

```bash
# OpenAI
export OPENAI_API_KEY=your-openai-api-key

# Anthropic Claude
export ANTHROPIC_API_KEY=your-anthropic-api-key

# Google Gemini
export GEMINI_API_KEY=your-gemini-api-key
```

**Security Tips:**
- Never hardcode API keys in your source code
- Use `.env` files for local development
- Set environment variables in your deployment platform
- Rotate keys regularly for production bots

#### 🧠 Using the LLM Module
```python
from bubbletea_chat import LLM

# Use any LLM provider
# Make sure to set OPENAI_API_KEY environment variable
llm = LLM(model="gpt-4")
response = await llm.acomplete("Hello!")

# Stream responses for better user experience
async for chunk in llm.stream("Tell me a story"):
    yield bt.Text(chunk)
```

**Available Models:**
- **OpenAI:** `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- **Anthropic:** `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- **Google:** `gemini-pro`, `gemini-pro-vision`
- **Open Source:** Support for Llama, Mistral, and more via LiteLLM

**Advanced Features:**
```python
# Custom parameters
llm = LLM(
    model="gpt-4",
    temperature=0.7,      # Control creativity (0-1)
    max_tokens=1000,      # Limit response length
    system_prompt="You are a helpful assistant"  # Set behavior
)

```

#### 📸 Vision & Media Support

```python
# Analyze images
@bt.chatbot
async def vision_bot(message: str, images: list = None):
    if images:
        # Make sure to set OPENAI_API_KEY environment variable
        llm = LLM(model="gpt-4-vision-preview")
        response = await llm.acomplete_with_images(message, images)
        yield bt.Text(response)

# Generate images
image_url = await llm.agenerate_image("A sunset over mountains")
yield bt.Image(image_url)
```

**Supported Media Types:**
- **Image Analysis:** JPG, PNG, GIF, WebP
- **Image Generation:** DALL-E 3, Stable Diffusion
- **File Processing:** PDF, TXT, CSV, JSON
- **Audio Support:** Coming soon!

> **Note:** The BT package automatically creates these endpoints for your bot:
> - `/chat` - Main bot endpoint for BubbleTea integration
> - `/docs` - Swagger API documentation


### 📚 Developer Resources

#### Documentation
- [API Reference](#)
- [Tutorial Guide](#)
- [Best Practices](#)

#### Example Bots
- [Echo Bot](https://github.com/bubbletea/examples)
- [AI Assistant](https://github.com/bubbletea/examples)
- [Image Generator](https://github.com/bubbletea/examples)

[PyPI Package](https://pypi.org/project/bubbletea-chat/) | [GitHub](https://github.com/bubbletea)

---

## API Reference

### Core Decorators

#### `@bt.chatbot`
The main decorator that transforms your function into a chat endpoint.

```python
@bt.chatbot
async def my_bot(
    message: str,           # User's message (required)
    images: list = None,    # List of uploaded images
    files: list = None,     # List of uploaded files
    history: list = None,   # Conversation history
    user_id: str = None,    # Unique user identifier
    metadata: dict = None   # Additional metadata
):
    yield bt.Text("Response")
```

**Parameters:**
- `message` (str, required): The user's input message
- `images` (list, optional): Base64-encoded images from the user
- `files` (list, optional): Uploaded files with metadata
- `history` (list, optional): Previous conversation messages
- `user_id` (str, optional): Unique identifier for the user
- `metadata` (dict, optional): Additional context data

### Response Components

#### Text Components
```python
# Plain text
bt.Text(content: str, typing_speed: int = 30)

# Markdown with formatting
bt.Markdown(content: str)

# Code with syntax highlighting
bt.Code(content: str, language: str = "python")

# Preformatted text
bt.Pre(content: str)
```

#### Media Components
```python
# Images
bt.Image(
    url: str,
    alt: str = None,
    width: int = None,
    height: int = None,
    caption: str = None
)

# Video
bt.Video(
    url: str,
    thumbnail: str = None,
    caption: str = None
)

# Audio
bt.Audio(
    url: str,
    title: str = None
)

# Files
bt.File(
    url: str,
    filename: str,
    size: int = None
)
```

#### Interactive Components
```python
# Buttons
bt.Button(
    label: str,
    action: str,
    style: str = "primary",  # primary, secondary, danger
    disabled: bool = False
)

# Button group
bt.ButtonGroup(buttons: list[Button])

# Pills (quick replies)
bt.Pills(
    options: list[str],
    action: str = "select"
)

# Cards
bt.Card(
    title: str,
    description: str = None,
    image: str = None,
    buttons: list[Button] = None
)

# Forms
bt.Form(
    fields: list[Field],
    submit_action: str = "submit"
)

# Input fields for forms
bt.TextField(name: str, label: str, required: bool = False)
bt.EmailField(name: str, label: str, required: bool = False)
bt.NumberField(name: str, label: str, min: float = None, max: float = None)
bt.SelectField(name: str, label: str, options: list[str])
bt.CheckboxField(name: str, label: str)
```

#### Layout Components
```python
# Lists
bt.List(items: list[str], ordered: bool = False)

# Tables
bt.Table(
    headers: list[str],
    rows: list[list[str]]
)

# Divider
bt.Divider()

# Spacer
bt.Spacer(height: int = 20)

# Container
bt.Container(
    children: list[Component],
    style: dict = None
)
```

### Server Configuration

#### `bt.run_server()`
Start the bot server with custom configuration.

```python
bt.run_server(
    bot_function,
    port: int = 8000,
    host: str = "0.0.0.0",
    cors_origins: list = ["*"],
    max_request_size: int = 10485760,  # 10MB
    timeout: int = 30,
    workers: int = 1,
    ssl_cert: str = None,
    ssl_key: str = None
)
```

**Parameters:**
- `bot_function`: Your decorated chatbot function
- `port`: Server port (default: 8000)
- `host`: Server host (default: "0.0.0.0")
- `cors_origins`: Allowed CORS origins
- `max_request_size`: Maximum request size in bytes
- `timeout`: Request timeout in seconds
- `workers`: Number of worker processes
- `ssl_cert`: Path to SSL certificate
- `ssl_key`: Path to SSL key

---

## Deployment Guide

### Local Development

#### Using ngrok (Recommended for Testing)
```bash
# Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Start your bot
python my_bot.py

# In another terminal, expose it to the internet
ngrok http 8000

# Use the ngrok URL to register with BubbleTea
# Example: https://abc123.ngrok.io/chat
```

### Cloud Deployment

#### Deploy to Heroku
1. Create `requirements.txt`:
```
bubbletea-chat
gunicorn
```

2. Create `Procfile`:
```
web: gunicorn my_bot:app -w 1 --worker-class uvicorn.workers.UvicornWorker
```

3. Deploy:
```bash
heroku create my-bubbletea-bot
git push heroku main
```

#### Deploy to AWS Lambda
1. Install dependencies:
```bash
pip install bubbletea-chat mangum -t .
```

2. Create Lambda handler:
```python
from mangum import Mangum
from my_bot import app

handler = Mangum(app)
```

3. Package and deploy:
```bash
zip -r function.zip .
aws lambda create-function --function-name my-bot ...
```

#### Deploy to Google Cloud Run
1. Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "my_bot.py"]
```

2. Build and deploy:
```bash
gcloud builds submit --tag gcr.io/PROJECT_ID/my-bot
gcloud run deploy --image gcr.io/PROJECT_ID/my-bot
```

#### Deploy to DigitalOcean App Platform
1. Connect your GitHub repository
2. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python my_bot.py`
3. Set environment variables
4. Deploy

### Production Best Practices

#### 1. Use Environment Variables
```python
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

#### 2. Implement Health Checks
```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
```

#### 3. Add Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bt.chatbot
async def bot(message: str):
    logger.info(f"Received message: {message[:50]}...")
    # Bot logic here
```

#### 4. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/chat")
@limiter.limit("30/minute")
async def chat_endpoint(request: Request):
    # Handle chat
```

#### 5. Database Integration
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

@bt.chatbot
async def bot_with_db(message: str):
    db = SessionLocal()
    try:
        # Database operations
        user_data = db.query(User).filter_by(id=user_id).first()
        yield bt.Text(f"Hello {user_data.name}")
    finally:
        db.close()
```

---

## Examples

### Example Bots

Get inspired by these example implementations.

#### 🎨 Image Generation Bot
Generate images from text descriptions using DALL-E

```python
@bt.chatbot
async def art_bot(prompt: str):
    # Make sure to set OPENAI_API_KEY environment variable
    llm = LLM(model="dall-e-3")
    image_url = await llm.agenerate_image(prompt)
    yield bt.Image(image_url)
    yield bt.Text("Your image is ready!")
```

#### 📚 Knowledge Assistant
Answer questions using GPT-4 with streaming

```python
@bt.chatbot
async def assistant(message: str):
    # Make sure to set OPENAI_API_KEY environment variable
    llm = LLM(model="gpt-4")
    yield bt.Text("Let me help you with that...")
    
    async for chunk in llm.stream(message):
        yield bt.Text(chunk)
```

#### 👁️ Vision Analyzer
Analyze images and answer questions about them

```python
@bt.chatbot
async def vision_bot(message: str, images: list = None):
    if images:
        # Make sure to set OPENAI_API_KEY environment variable
        llm = LLM(model="gpt-4-vision-preview")
        analysis = await llm.acomplete_with_images(message, images)
        yield bt.Markdown(analysis)
```

[View More Examples →](https://github.com/bubbletea/examples)

---

## Component Documentation

### Available UI Components

BubbleTea provides rich UI components for enhanced chat experiences:

#### Text Components
```python
# Plain text
yield bt.Text("Simple message")

# Markdown formatting
yield bt.Markdown("**Bold** and *italic* text with [links](https://example.com)")

# Code blocks with syntax highlighting
yield bt.Code("print('Hello World')", language="python")
```

#### Media Components
```python
# Images
yield bt.Image("https://example.com/image.jpg", alt="Description")

# Cards with rich content
yield bt.Card(
    title="Product Name",
    description="Product details",
    image="https://example.com/product.jpg",
    buttons=[bt.Button("Buy Now", action="purchase")]
)

# Lists and tables
yield bt.List(["Item 1", "Item 2", "Item 3"])
```

#### Interactive Components
```python
# Buttons for user actions
yield bt.Button("Click me", action="button_clicked")

# Pills for quick replies
yield bt.Pills(["Yes", "No", "Maybe"], action="user_choice")

# Forms for data collection
yield bt.Form(fields=[
    bt.TextField("name", label="Your Name"),
    bt.EmailField("email", label="Email Address")
])
```

---

## Troubleshooting Guide

### Common Issues and Solutions

#### Bot Not Responding
**Problem:** Your bot doesn't respond to messages

**Solutions:**
- Verify your bot server is running: `curl http://localhost:8000/health`
- Check the `/chat` endpoint is accessible
- Ensure proper CORS headers are set
- Review server logs for error messages

#### Authentication Errors
**Problem:** API key or authentication issues

**Solutions:**
- Verify environment variables are set correctly
- Check API key validity and permissions
- Ensure keys are not expired
- Use `.env` file for local development

#### Streaming Not Working
**Problem:** Responses appear all at once instead of streaming

**Solutions:**
```python
# Ensure you're using async generator
@bt.chatbot
async def streaming_bot(message: str):
    # Use yield for streaming
    for word in message.split():
        yield bt.Text(word + " ")
        await asyncio.sleep(0.1)  # Small delay for effect
```

#### Image Upload Issues
**Problem:** Images not processing correctly

**Solutions:**
- Check file size limits (max 10MB)
- Verify supported formats (JPG, PNG, WebP)
- Ensure proper base64 encoding if needed
- Test with smaller images first

---

## Performance Best Practices

### Optimize Your Bot for Speed

#### 1. Use Streaming for Long Responses
```python
# Good - Stream responses
async for chunk in llm.stream(prompt):
    yield bt.Text(chunk)

# Avoid - Waiting for complete response
response = await llm.acomplete(prompt)
yield bt.Text(response)
```

#### 2. Implement Caching
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_operation(input_data):
    # Cache results for repeated queries
    return process_data(input_data)
```

#### 3. Handle Errors Gracefully
```python
@bt.chatbot
async def robust_bot(message: str):
    try:
        response = await process_message(message)
        yield bt.Text(response)
    except Exception as e:
        yield bt.Text("I encountered an issue. Please try again.")
        # Log error for debugging
        print(f"Error: {e}")
```

#### 4. Optimize Context Management
```python
# Keep conversation context reasonable
MAX_CONTEXT_LENGTH = 10  # Last 10 messages

@bt.chatbot
async def context_aware_bot(message: str, history: list):
    # Limit context to prevent token overflow
    recent_history = history[-MAX_CONTEXT_LENGTH:]
    response = await llm.acomplete_with_context(message, recent_history)
    yield bt.Text(response)
```

---

## Security Guidelines

### Protecting Your Bot and Users

#### API Key Management
```python
# ❌ NEVER do this
API_KEY = "sk-abc123xyz789"

# ✅ Use environment variables
import os
API_KEY = os.getenv("API_KEY")

# ✅ Use a .env file for local development
from dotenv import load_dotenv
load_dotenv()
```

#### Input Validation
```python
@bt.chatbot
async def secure_bot(message: str):
    # Validate and sanitize input
    if len(message) > 1000:
        yield bt.Text("Message too long. Please keep it under 1000 characters.")
        return
    
    # Escape special characters for safety
    safe_message = html.escape(message)
    
    # Process safely
    response = await process_safe_input(safe_message)
    yield bt.Text(response)
```

#### Rate Limiting & DDoS Protection
```python
from collections import defaultdict
from datetime import datetime, timedelta

request_counts = defaultdict(list)

@bt.chatbot
async def rate_limited_bot(message: str, user_id: str):
    # Check rate limit (10 requests per minute)
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)
    
    # Clean old requests
    request_counts[user_id] = [
        req_time for req_time in request_counts[user_id]
        if req_time > minute_ago
    ]
    
    # Check limit
    if len(request_counts[user_id]) >= 10:
        yield bt.Text("Too many requests. Please wait a moment.")
        return
    
    request_counts[user_id].append(now)
    # Process request
```

#### Data Privacy
```python
@bt.chatbot
async def privacy_conscious_bot(message: str, user_id: str):
    # Don't log sensitive information
    logger.info(f"User {user_id[:8]}... sent message")  # Partial ID only
    
    # Encrypt sensitive data before storage
    encrypted_data = encrypt(sensitive_info)
    
    # Use secure connections
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://api.example.com/secure",
            ssl=True,
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            data = await response.json()
```

#### Authentication & Authorization
```python
@bt.chatbot
async def authenticated_bot(message: str, user_id: str, metadata: dict):
    # Verify user permissions
    if not await verify_user_access(user_id):
        yield bt.Text("You don't have permission to use this bot.")
        return
    
    # Check for admin commands
    if message.startswith("/admin"):
        if not await is_admin(user_id):
            yield bt.Text("Admin access required.")
            return
```

---

## FAQ

### Frequently Asked Questions

#### General Questions

**Q: What is BubbleTea?**
A: BubbleTea is a platform that provides instant web interfaces for AI chatbots and agents. Build your bot in any language, and we provide the beautiful chat UI.

**Q: Is BubbleTea free to use?**
A: Yes! BubbleTea offers a free tier for developers to build and deploy bots. Premium features are available for production use.

**Q: What programming languages are supported?**
A: Any language that can create HTTP endpoints! We provide official SDKs for Python, with JavaScript/TypeScript coming soon.

**Q: Can I use my own domain?**
A: Custom domains are available on premium plans. Free bots use the bubbletea.chat subdomain.

#### Technical Questions

**Q: How do I handle file uploads?**
A: Files are automatically handled by the platform and passed to your bot:
```python
@bt.chatbot
async def file_handler(message: str, files: list = None):
    if files:
        for file in files:
            yield bt.Text(f"Received file: {file['name']}")
            # Process file content
```

**Q: Can I maintain conversation history?**
A: Yes! Conversation history is automatically provided:
```python
@bt.chatbot
async def bot_with_memory(message: str, history: list = None):
    if history:
        context = "\n".join([f"{h['role']}: {h['content']}" for h in history[-5:]])
        # Use context in your response
```

**Q: How do I stream responses?**
A: Use async generators with yield:
```python
@bt.chatbot
async def streaming_bot(message: str):
    for word in message.split():
        yield bt.Text(word + " ")
        await asyncio.sleep(0.1)
```

**Q: Can I integrate with databases?**
A: Absolutely! Use any database library:
```python
import asyncpg

@bt.chatbot
async def db_bot(message: str, user_id: str):
    conn = await asyncpg.connect(DATABASE_URL)
    data = await conn.fetch("SELECT * FROM users WHERE id = $1", user_id)
    await conn.close()
    yield bt.Text(f"Welcome back, {data[0]['name']}!")
```

**Q: How do I handle errors gracefully?**
A: Implement try-catch blocks and provide user-friendly messages:
```python
@bt.chatbot
async def robust_bot(message: str):
    try:
        result = await risky_operation(message)
        yield bt.Text(result)
    except SpecificError as e:
        yield bt.Text("Sorry, something went wrong. Please try again.")
        logger.error(f"Error: {e}")
    except Exception as e:
        yield bt.Text("An unexpected error occurred.")
        logger.critical(f"Critical error: {e}")
```

#### Deployment Questions

**Q: Can I deploy on my own server?**
A: Yes! Deploy your bot anywhere that can run Python. Just ensure the `/chat` endpoint is accessible.

**Q: What are the server requirements?**
A: Minimum requirements:
- Python 3.8+
- 512MB RAM
- 1 CPU core
- SSL certificate (for production)

**Q: How do I scale my bot?**
A: Use load balancers and multiple instances:
```python
# Run with multiple workers
bt.run_server(bot, workers=4)

# Or use Gunicorn
# gunicorn my_bot:app -w 4 --worker-class uvicorn.workers.UvicornWorker
```

**Q: Can I use WebSockets?**
A: Server-Sent Events (SSE) are used for streaming. WebSocket support is on the roadmap.

#### Business Questions

**Q: Can I monetize my bot?**
A: Yes! You can charge users directly or through the BubbleTea marketplace (coming soon).

**Q: Is there an SLA?**
A: Enterprise plans include SLA guarantees. Contact sales@bubbletea.chat for details.

**Q: Can I white-label the interface?**
A: White-labeling is available on enterprise plans.

---

## Community & Support

### Join Our Growing Community

#### 📚 Resources
- [Documentation](https://docs.bubbletea.chat)
- [Video Tutorials](https://youtube.com/bubbletea)
- [Blog](https://blog.bubbletea.chat)
- [API Status](https://status.bubbletea.chat)

#### 🤝 Contributing
We welcome contributions! See our [Contributing Guide](https://github.com/bubbletea/contributing).

#### 📧 Support Channels
- **Community Support**: GitHub Discussions
- **Email Support**: support@bubbletea.chat
- **Enterprise Support**: enterprise@bubbletea.chat

#### 🐛 Bug Reports
Found a bug? Report it on [GitHub Issues](https://github.com/bubbletea/issues).

---

## Ready to Build?

Join developers building the next generation of AI assistants.

[Get Started Free](https://bubbletea.chat/login)

### Quick Links
- 📚 [Full Documentation](https://docs.bubbletea.chat)
- 💬 [Community Forum](https://forum.bubbletea.chat)
- 🐛 [Report Issues](https://github.com/bubbletea/issues)
- 📧 [Contact Support](mailto:support@bubbletea.chat)

---

Built with ❤️ by the Bubbletea team
