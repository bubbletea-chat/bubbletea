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

4. **Submit a Pull Request** against the master branch

5. **Get reviewed and merged** - Your bot will be live on Bubbletea!

## 📚 Documentation & Resources

- **[Bubbletea Platform Documentation](https://bubbletea.chat/docs)** - Complete reference and component guide
- **[Python Package (PyPI)](https://pypi.org/project/bubbletea-chat/)** - `pip install bubbletea-chat`
- **[Developer Dashboard](https://bubbletea.chat/developer)** - Manage your bots
- **[Video Tutorial](https://www.youtube.com/embed/Op5cbkJylm8)** - Step-by-step guide

## 📁 Repository Structure

Each bot MUST have its own folder with the following structure:

```
bots-public/
├── your-bot-name/              # Folder name = bot name (lowercase, hyphenated)
│   ├── README.md               # REQUIRED: Bot documentation
│   ├── bot.py                  # REQUIRED: Main bot code
│   ├── requirements.txt        # REQUIRED: Python dependencies
│   ├── .env.example            # REQUIRED: Example environment variables
│   └── tests/                  # OPTIONAL: Test files
│       └── test_bot.py
```

### Example: Weather Bot Structure

```
weather-bot/
├── README.md                   # Explains what the bot does
├── weather_bot.py              # Main bot implementation
├── requirements.txt            # Lists: bubbletea-chat, requests, python-dotenv
├── .env.example                # Contains: WEATHER_API_KEY=your_key_here
└── tests/
    └── test_weather.py        # Unit tests
```

## 📝 Bot Submission Requirements

### 1. Folder Naming Rules

- **Must be lowercase**: `my-bot` ✅ `My-Bot` ❌
- **Use hyphens for spaces**: `weather-bot` ✅ `weather_bot` ❌
- **Be descriptive**: `recipe-finder` ✅ `bot1` ❌
- **Match your bot's registered name**: Folder name should match the name in BotConfig

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
- import bubbletea_chat
- Define @bt.config() with proper bot configuration
- Implement @bt.chatbot() function
- Include `if __name__ == "__main__":` block

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

- [ ] Bot responds to `/chat` endpoint
- [ ] Bot provides `/config` endpoint (if using @bt.config decorator)
- [ ] All environment variables are documented
- [ ] No API keys or secrets in code
- [ ] requirements.txt includes all dependencies
- [ ] README has clear setup instructions
- [ ] Code follows Python conventions


### Replit Template
```python
# .replit file
run = "python bot.py"
language = "python3"

[deployment]
run = ["python", "bot.py"]
deploymentTarget = "cloudrun"
```

### Docker Template
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "bot.py"]
```

### Environment Configuration
- Use `.env` for local development
- Use platform-specific secrets for production (Replit Secrets, Docker env, etc.)
- Never commit actual API keys

## 🎯 Bot Examples to Follow

Look at these well-structured bots for inspiration:

### Simple Structure (echo-bot/)
```
echo-bot/
├── README.md
├── echo_bot.py
├── requirements.txt
└── .env.example
```

### Advanced Structure (ai-assistant/)
```
ai-assistant/
├── README.md
├── main.py
├── requirements.txt
├── .env.example
├── config/
│   └── settings.py
├── utils/
│   ├── llm_helper.py
│   └── validators.py
├── deploy/
│   ├── README.md
│   ├── Dockerfile
│   └── docker-compose.yml
└── tests/
    ├── test_main.py
    └── test_utils.py
```

## 🚫 What NOT to Include

- ❌ API keys or secrets
- ❌ User data or logs
- ❌ `__pycache__` or `.pyc` files
- ❌ Virtual environment folders (`venv/`, `env/`)
- ❌ IDE configuration (`.vscode/`, `.idea/`)
- ❌ Large files (models, datasets)
- ❌ Copyrighted content without permission

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
- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)
- **Developer Dashboard**: [bubbletea.chat/developer](https://bubbletea.chat/developer)

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