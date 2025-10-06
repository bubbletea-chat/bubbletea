# 🤖 Bubbletea Public Bots Repository

Welcome to the official Bubbletea community bots repository! This is where developers can contribute and share their AI bots with the Bubbletea community.

## 🚀 Quick Start

### What is Bubbletea?

Bubbletea is a frontend platform for AI agents and chatbots. You build the bot logic, we provide the beautiful chat interface. Your bot gets:
- 🌐 Instant web access at `bubbletea.chat/your-bot`
- 📱 iOS & Android app support
- 👥 User management & chat history
- 🎨 Rich UI components
- 💬 Real-time streaming support

### How to Contribute a Bot

1. **Clone this repository**
   ```bash
   git clone https://github.com/bubbletea-chat/bots-public.git
   cd bots-public
   ```

2. **Create a new folder with your bot name** (lowercase, hyphenated)
   ```bash
   mkdir my-awesome-bot
   cd my-awesome-bot
   ```

3. **Develop your bot** following the structure guidelines below

4. **Test your bot locally**
   ```bash
   cd your-bot-name
   pip install -r requirements.txt
   python bot.py
   # Bot will run on http://localhost:8000
   ```

5. **Submit a Pull Request** against the master branch

6. **Get reviewed and merged** - Your bot will be live on Bubbletea!

## 📚 Documentation & Resources

- **[Bubbletea Platform Documentation](https://bubbletea.chat/docs)** - Complete reference and component guide
- **[Python Package (PyPI)](https://pypi.org/project/bubbletea-chat/)** - `pip install bubbletea-chat`
- **[Developer Dashboard](https://bubbletea.chat/developer)** - Manage your bots
- **[Video Tutorial](https://www.youtube.com/embed/Op5cbkJylm8)** - Step-by-step guide

## 📁 Repository Structure

Each bot MUST have its own folder with the following structure:

```
bots/
├── your-bot-name/              # Folder name = bot name (lowercase, hyphenated)
│   ├── README.md               # REQUIRED: Bot documentation
│   ├── bot.py                  # REQUIRED: Main bot code
│   ├── requirements.txt        # REQUIRED: Python dependencies
│   ├── .env.example            # REQUIRED: Example environment variables
│   └── tests/                  # OPTIONAL: Test files
│       └── test_bot.py
```

## 📝 Bot Submission Requirements

### 1. Folder Naming Rules

- **Must be lowercase**: `my-bot` ✅ `My-Bot` ❌
- **Use hyphens for spaces**: `weather-bot` ✅ `weather_bot` ❌
- **Be descriptive**: `recipe-finder` ✅ `bot1` ❌
- **Match your bot's registered name**: Folder name should match the name in BotConfig
- **No special characters**: Only letters, numbers, and hyphens allowed

### 2. Required Files

#### README.md
Your bot's README must include:

```markdown
# Bot Name

## Description
Clear explanation of what your bot does and its key features.

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd your-bot-name`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Add your API keys to `.env`
6. Run the bot: `python bot.py`

## Deployment Options
- **Replit**: [Quick deployment guide]
- **Docker**: See `Dockerfile` # Deploy anywhere
- **Local**: Use ngrok for testing


#### bot.py (or main.py)
Your main bot file should:
- Import bubbletea_chat: `import bubbletea_chat as bt`
- Define @bt.config() with proper bot configuration
- Implement @bt.chatbot() function for handling messages
- Include `if __name__ == "__main__":` block to run the server
- Handle environment variables with python-dotenv when needed

#### requirements.txt
List all dependencies with versions:
```
bubbletea-chat>=0.6.3
python-dotenv>=1.0.0
# Add other dependencies your bot needs
```

#### .env.example
Template for environment variables:
```bash
# API Keys
OPENAI_API_KEY=your_openai_key_here
WEATHER_API_KEY=your_weather_api_key_here
...
```

### 3. Code Standards

- ✅ **Clear variable names**: `user_message` not `msg`
- ✅ **Error handling**: Handle API failures gracefully
- ✅ **Comments**: Explain complex logic
- ✅ **No hardcoded secrets**: Use environment variables
- ✅ **Python 3.8+**: Ensure compatibility
- ✅ **Testing**: Test locally before submitting

### 4. Bot Testing Checklist

Before submitting your PR, ensure:

- [ ] Bot responds to `/chat` endpoint correctly
- [ ] Bot provides `/config` endpoint (if using @bt.config decorator)
- [ ] All environment variables are documented in .env.example
- [ ] No API keys or secrets in code (use .env file)
- [ ] requirements.txt includes all dependencies with versions
- [ ] README has clear setup instructions
- [ ] Code follows Python conventions (PEP 8)
- [ ] Bot runs without errors: `python bot.py`
- [ ] Test with sample inputs to verify functionality
- [ ] Remove any test files or debug code before submission


### Deployment Templates

#### Replit Configuration
```python
# .replit file
run = "python bot.py"
language = "python3"

[deployment]
run = ["python", "bot.py"]
deploymentTarget = "cloudrun"

[env]
PYTHON_VERSION = "3.11"
```

#### Docker Template
```dockerfile
FROM python:3.11-slim
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot files
COPY . .

# Expose the default Bubbletea port
EXPOSE 8000

# Run the bot
CMD ["python", "bot.py"]
```

### Environment Configuration
- Use `.env` for local development
- Use platform-specific secrets for production (Replit Secrets, Docker env, etc.)
- Never commit actual API keys

## 🎯 Example Bots in This Repository

Explore these existing bots to learn different implementation patterns:

### 🔧 Available Example Bots

1. **echo-bot** - Simple echo bot demonstrating basic structure
2. **openai-bot** - ChatGPT-powered conversational AI bot
3. **claude-bot** - Anthropic Claude integration example
4. **gemini-bot** - Google Gemini AI bot implementation
5. **morning-bot** - Daily greeting and weather bot with scheduling
6. **movie-game-bot** - Interactive movie guessing game
7. **photo-to-video-bot** - Media processing bot for image to video conversion
8. **restaurant-reservation-bot** - Booking system demonstration
9. **bt-components-showcase-bot** - Showcases all Bubbletea UI components
10. **bt-developers-help-bot** - Developer assistance and documentation bot

### Bot Structure Examples

#### Simple Structure (echo-bot/)
```
echo-bot/
├── README.md
├── bot.py
├── requirements.txt
└── echo-bot-demo.gif    # Optional: Demo screenshot/video
```

#### Standard Structure (openai-bot/)
```
openai-bot/
├── README.md
├── bot.py
├── requirements.txt
├── openai-bot-demo.gif
└── tests/               # Optional: Test files
    └── test_bot.py
```

#### Advanced Structure (morning-bot/)
```
morning-bot/
├── README.md
├── bot.py
├── requirements.txt
├── config/
│   └── settings.py
├── utils/
│   └── helpers.py
└── tests/
    └── test_bot.py
```

## 🚫 What NOT to Include

- ❌ API keys or secrets (use .env files)
- ❌ User data or logs
- ❌ `__pycache__` or `.pyc` files
- ❌ Virtual environment folders (`venv/`, `env/`)
- ❌ IDE configuration (`.vscode/`, `.idea/`)
- ❌ Large files (models, datasets > 10MB)
- ❌ Copyrighted content without permission
- ❌ Test files with hardcoded credentials
- ❌ Temporary or backup files (`.tmp`, `.bak`, `~`)

## 🤝 Pull Request Process

1. **Create your bot folder** with all required files
2. **Test thoroughly** on your local machine
3. **Create a pull request** with title: `Add [bot-name] bot`
4. **PR Description** should include:
   - What your bot does
   - Any special features
   - Deployment tested on (Replit/Docker/etc.)
   - Screenshot or demo video (optional)
5. **Address review feedback** if requested
6. **Get merged** and celebrate! 🎉

## 🆘 Getting Help

- **SDK Documentation**: [bubbletea.chat/docs](https://bubbletea.chat/docs)
- **Python Package**: [PyPI - bubbletea-chat](https://pypi.org/project/bubbletea-chat/)
- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)
- **Developer Dashboard**: [bubbletea.chat/developer](https://bubbletea.chat/developer)
- **Example Bots**: Check the existing bots in this repository for implementation patterns

## 📄 License

All bots in this repository should be open source. By contributing, you agree to make your bot's code available for the community to learn from and build upon.

## 🎉 Start Building!

1. **Clone the repo**: `git clone https://github.com/bubbletea-chat/bots-public.git`
2. **Create your bot folder**: Follow the structure above
3. **Build something awesome**: Check the docs for component reference
4. **Submit your PR**: Share your creation with the world!
5. **See it live**: Access at `bubbletea.chat/your-bot-name`

---

<div align="center">
  <b>Built with ❤️ by Bubbletea</b>
  <br>
  <a href="https://bubbletea.chat">Website</a> •
  <a href="https://github.com/bubbletea-chat">GitHub</a> •
  <a href="https://pypi.org/project/bubbletea-chat/">PyPI</a>
</div>