# Creating a Bot

## Table of Contents
- [Subaccounts](#subaccounts)
- [Bot Configuration](#bot-configuration)
- [Quickstart - E2E Echobot](#quickstart---e2e-echobot)

## Subaccounts

### Organize Your Bots with Subaccounts

Subaccounts allow you to organize and manage multiple bots under a single parent account. Each subaccount operates independently with its single bot and settings, while the parent account maintains full oversight and control.

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

Follow these steps to create and manage subaccounts in the Bubbletea platform:

**📱 Step 1: Access Developer Dashboard**

1. Open the dropdown menu from the header of the Chats screen
2. Click on "Developer" to navigate to the subaccounts

**➕ Step 2: Create New Subaccount**

1. Click the "+" icon in the header of the Subaccounts screen
2. The "Add Subaccount" modal will open
3. Enter a unique handle for your subaccount
4. Click "Add Subaccount" to create it

*💡 Handle Behavior:*
- If the handle exists: It will be linked to your account
- If the handle doesn't exist: A new subaccount will be created

**🤖 Step 3: Add Bot to Subaccount**

1. Click on the newly created subaccount from the list to switch from parent to subaccount
2. Click the "Your Bot" button to start adding a bot
3. The "Add New Bot" modal will open
4. Enter your bot's URL (endpoint where your bot is hosted)
5. Click "Create Bot" - the bot configuration will be automatically fetched from your /config endpoint
6. Your bot is now live and ready to chat!

*🔧 Bot Configuration:*
- Bot data is automatically fetched from your bot's /config endpoint
- Make sure your bot URL is accessible and has a /config route
- Each subaccount can have exactly 1 bot

**💡 Best Practices & Tips**

*✅ Bot Development Workflow:*
- Test your bot locally first before adding to Bubbletea
- Ensure your bot has a /config endpoint that returns valid configuration
- Use descriptive subaccount handles (e.g., "customer-support", "sales-bot")
- Keep your bot URL accessible and stable

*🔧 Technical Requirements:*
- Bot URL must be publicly accessible
- Must respond to POST requests at /chat endpoint
- Must have GET /config endpoint for configuration
- HTTPS recommended for production bots

**Switching Between Accounts**

Easily switch between your parent account and subaccounts to manage different bots. This is essential for managing multiple bots across different projects or teams.

**📱 How to Switch to a Subaccount**

1. Go to the Subaccounts page (Developer → Subaccounts)
2. Find the subaccount you want to switch to in the list
3. Click on the subaccount name to switch into that account context
4. You're now working within the selected subaccount
5. All bot operations will now apply to this subaccount

**🏠 Switching Back to Parent Account**

1. Click the parent account name shown above the subaccounts section
2. Wait for the account switch to complete
3. You're now back in your parent account context
4. You can now manage all subaccounts and view the overview

Subaccounts help you keep your bots organized and secure while giving you the flexibility to manage multiple projects under one roof.

## Bot Configuration

Every bot needs configuration to tell Bubbletea how to display and interact with it. The @config decorator defines your bot's identity, appearance, and behavior. This configuration is what users see when browsing available bots:

```python
import bubbletea_chat as bt

@bt.config()088323
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

## Quickstart - E2E Echobot

Get your first bot running in minutes. This complete example shows you how to build, deploy, and share a working chatbot in just 3 steps.

**🎬 Video Demonstration**

Watch this step-by-step video guide that walks you through the entire process:
[Bubbletea Quickstart Tutorial](https://www.youtube.com/embed/Op5cbkJylm8)

### Step 1: Create an Echo Bot

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

### Step 2: Deploy with ngrok or Replit

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

### Step 3: Register Your Bot & Access Everywhere

Finally, register your bot through the Dashboard to make it accessible to users:

- Go to [https://bubbletea.chat](https://bubbletea.chat)
- Create or select a subaccount for your bot
- Use BT Agent or the dashboard UI to register your bot

Your bot is now accessible at:
- 🌐 Web: https://bubbletea.chat/echobot
- 📱 iOS & Android: Bubbletea mobile app

**📱 Note:** Guest mode (try bots without signing up) is currently available on iOS only.