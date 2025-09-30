# Deploying a Bot

## Table of Contents
- [Ngrok - Local Development Made Easy](#ngrok---local-development-made-easy)
- [Replit - Instant Cloud Hosting](#replit---instant-cloud-hosting)
- [CORS Support - Cross-Origin Configuration](#cors-support---cross-origin-configuration)
- [Testing Your Bot](#testing-your-bot)

## Ngrok - Local Development Made Easy

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

## Replit - Instant Cloud Hosting

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

## CORS Support - Cross-Origin Configuration

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

## Testing Your Bot

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