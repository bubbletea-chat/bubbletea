# BubbleTea Developers Help Bot

## Description
An intelligent assistant that helps developers learn and use the BubbleTea SDK. Get instant answers to your SDK questions, see code examples, and learn best practices for building chatbots on the BubbleTea platform.

## Features
- **Instant SDK Help**: Ask questions about BubbleTea components and get immediate answers
- **Code Examples**: See practical, working code snippets for common tasks  
- **Component Reference**: Learn about Text, Image, Markdown, Cards, Pills, and more
- **Best Practices**: Get guidance on building production-ready bots
- **LLM Integration Help**: Learn how to use OpenAI, Claude, Gemini and 100+ models
- **Real-time Assistance**: Interactive Q&A based on official documentation

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd bt_developers_help_bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Configure your API keys in `.env`
6. Run the bot: `python bot.py`

## Configuration

### Environment Variables
```env
# OpenAI Configuration (for GPT-powered answers)
OPENAI_API_KEY=your_openai_api_key

# BubbleTea Configuration
BUBBLETEA_API_KEY=your_bubbletea_api_key

# Bot Settings
BOT_URL=http://example.com
```

## Commands
### Example Questions
**You**: "How do I create a simple chatbot?"
**Bot**: Shows complete code example with explanation

**You**: "How do I use images in my bot?"
**Bot**: Demonstrates Image component usage with examples

**You**: "How to handle user messages?"
**Bot**: Explains message handling patterns and best practices

**You**: "Show me how to use Pills for buttons"
**Bot**: Provides interactive button implementation examples

### Available Topics
- **Getting Started**: Bot creation, setup, deployment
- **Components**: All UI components (Text, Markdown, Cards, Pills, etc.)
- **LLM Integration**: Using AI models in your bots
- **Message Handling**: Processing user input and responses
- **State Management**: Tracking conversations and user data
- **Advanced Features**: Streaming, async processing, webhooks
- **Best Practices**: Production tips and optimization

## Use Cases

### Learning the SDK
- Understanding component usage
- Exploring available features
- Learning syntax and patterns
- Finding code examples

### Problem Solving
- Debugging bot issues
- Understanding error messages
- Optimizing performance
- Implementing complex features

### Reference
- Quick component lookup
- Parameter documentation
- Method signatures
- Configuration options

## Technical Details
The bot has access to the complete BubbleTea SDK documentation and uses AI to provide accurate, contextual answers to your development questions. It can:
- Parse your questions to understand what you need
- Search through documentation for relevant information
- Generate working code examples
- Explain concepts in clear, simple terms
- Provide best practice recommendations

### Requirements
- Python 3.8+
- BubbleTea Chat SDK
- OpenAI API key (for AI-powered responses)

## Deployment Options
- **Local**: Run directly with Python
- **Replit**: Fork and run on Replit
- **Docker**: Container deployment supported
- **Cloud**: Deploy to any Python-supporting platform

## Support
For SDK issues or questions not answered by this bot:
- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)
- **PyPI Package**: [pypi.org/project/bubbletea-chat/](https://pypi.org/project/bubbletea-chat/)