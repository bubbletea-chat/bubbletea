# Claude Assistant Bot

## Description
An advanced AI assistant powered by Anthropic's Claude, offering intelligent conversations, complex reasoning, and helpful assistance across a wide range of topics. This bot provides access to Claude's capabilities including analysis, creative writing, coding help, and general knowledge.

## Features
- Advanced conversational AI with Claude
- Context-aware responses
- Multi-turn conversations with memory
- Code generation and debugging assistance
- Creative writing and content generation
- Research and analysis capabilities
- Markdown formatting support
- Streaming responses for better UX

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd claude_bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Add your Anthropic API key to `.env`
6. Run the bot: `python bot.py`

## Configuration
### Getting an Anthropic API Key
1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Navigate to API keys section
3. Create a new API key
4. Add it to your `.env` file

### Model Selection
- Default: Claude 3 Sonnet (balanced performance)
- Options: Claude 3 Opus (most capable), Claude 3 Haiku (fastest)
- Configure in `.env` with CLAUDE_MODEL variable

## Commands
- Send any message to start a conversation
- `/new` - Start a new conversation thread
- `/help` - Display available commands
- `/model` - Check current model
- `/clear` - Clear conversation history

## Use Cases
- **Coding Assistance**: Debug code, generate functions, explain algorithms
- **Writing Help**: Essays, emails, creative content, documentation
- **Research**: Summarize articles, analyze data, answer questions
- **Learning**: Explain concepts, provide tutorials, answer questions
- **Problem Solving**: Logic puzzles, math problems, strategic planning
- **Creative Tasks**: Story writing, brainstorming, idea generation

### Example Interactions
- "Help me write a Python function to sort a list"
- "Explain quantum computing in simple terms"
- "Review this code for potential bugs"
- "Write a professional email declining a meeting"
- "What are the main causes of climate change?"
- "Help me plan a 7-day trip to Japan"

## Technical Details
- **AI Model**: Anthropic Claude (configurable version)
- **Context Window**: Up to 100k tokens
- **Response Format**: Markdown with code highlighting
- **Streaming**: Real-time response streaming
- **Rate Limiting**: Handled automatically

### Best Practices
- Be specific in your requests for better responses
- Use clear, concise language
- Provide context when asking follow-up questions
- Use code blocks for code-related queries
- Break complex tasks into smaller steps

## Deployment Options
- **Local**: Run directly with Python
- **Docker**: Container deployment supported
- **Cloud**: Deploy to any Python-supporting platform
- **Serverless**: AWS Lambda, Google Cloud Functions

### Advanced Features
- Custom system prompts
- Temperature and parameter tuning
- Response length control
- Token usage tracking
- Conversation export

### Limitations
- No real-time information or web browsing
- Cannot execute code (only generate)
- Knowledge cutoff based on training data
- Rate limits apply based on API tier

## Support
For Anthropic API documentation, visit [docs.anthropic.com](https://docs.anthropic.com)
For BubbleTea platform issues: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)