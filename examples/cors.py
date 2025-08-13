"""
CORS configuration example for BubbleTea bots
"""

import bubbletea_chat as bt


@bt.config()
def get_config():
    """Bot configuration with CORS settings"""
    return bt.BotConfig(
        name="CORS Bot",
        url="http://localhost:8011",
        is_streaming=False,
        emoji="🌐",
        initial_text="Bot with custom CORS configuration!",
        # CORS configuration can be added here
        cors_config={
            "allow_origins": ["https://myapp.com", "http://localhost:3000"],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Custom-Header"]
        }
    )


@bt.chatbot(stream=False)
def cors_bot(message: str):
    """Bot demonstrating CORS configuration"""
    components = []
    components.append(bt.Text(f"Echo: {message}"))
    components.append(bt.Markdown("""
## CORS Configuration Active

This bot has custom CORS settings:
- **Allowed Origins**: myapp.com, localhost:3000
- **Credentials**: Enabled
- **Methods**: GET, POST, OPTIONS
- **Custom Headers**: Supported

Perfect for production deployments!
    """))
    return components


# Example of running with different CORS configurations
if __name__ == "__main__":
    # Method 1: Default CORS (allows all origins - good for development)
    # bt.run_server(cors_bot, port=8011)
    
    # Method 2: Custom CORS for production
    bt.run_server(
        cors_bot,
        port=8011,
        cors=True,
        cors_config={
            "allow_origins": [
                "https://bubbletea.app",
                "https://myapp.com",
                "http://localhost:3000",
                "http://localhost:5173"  # Vite dev server
            ],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "OPTIONS", "HEAD"],
            "allow_headers": ["*"],  # Or specify: ["Content-Type", "Authorization"]
            "max_age": 86400  # Cache preflight for 24 hours
        }
    )
    
    # Method 3: Disable CORS (not recommended)
    # bt.run_server(cors_bot, port=8011, cors=False)