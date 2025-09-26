# Echo Bot

## Description
A simple demonstration bot that echoes back user messages. This bot is perfect for testing BubbleTea platform integration, understanding basic bot structure, and serving as a starting template for more complex bots. It demonstrates the minimal setup required to create a functional chatbot.

## Features
- Simple echo functionality
- Instant message reflection
- Minimal dependencies
- Clean code structure
- Easy to understand and modify
- Perfect starting template
- Lightweight and fast
- No external API requirements

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd echo-bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Configure your BubbleTea settings in `.env`
6. Run the bot: `python bot.py`


### Example Interactions
- "Hello" → "Echo: Hello"
- "How are you?" → "Echo: How are you?"
- "Test message" → "Echo: Test message"
- "123" → "Echo: 123"
- "🎉 Party!" → "Echo: 🎉 Party!"
- Any message gets echoed back with "Echo: " prefix

## Technical Details
- **Framework**: BubbleTea Python SDK
- **Response Type**: Synchronous (non-streaming)
- **Dependencies**: Minimal (bubbletea-chat only)
- **Python Version**: 3.8+
- **Memory**: Stateless operation

### Code Structure
- `bot.py`: Main bot logic and configuration
- `.env.example`: Environment variable template
- `requirements.txt`: Python dependencies
- Simple decorator-based implementation

## Support
For BubbleTea SDK documentation: [docs.bubbletea.chat](https://bubbletea.chat/docs)
For platform issues: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)