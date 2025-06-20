"""
Example bot demonstrating automatic CORS support in BubbleTea
"""

import bubbletea as bt

@bt.config()
def get_config():
    return bt.BotConfig(
        name="CORS Enabled Bot",
        url="http://localhost:8001",
        is_streaming=False,
        emoji="🌐",
        initial_text="Hello! I'm a bot with automatic CORS support. No more OPTIONS errors!"
    )

@bt.chatbot()
def cors_bot(message: str):
    return bt.Text(f"Echo: {message}\n\nCORS is automatically handled by BubbleTea!")

if __name__ == "__main__":
    # CORS is enabled by default - no configuration needed!
    bt.run_server(cors_bot, port=8001)
    
    # To disable CORS (not recommended):
    # bt.run_server(cors_bot, port=8001, cors=False)
    
    # To customize CORS (for production):
    # bt.run_server(cors_bot, port=8001, cors_config={
    #     "allow_origins": ["https://bubbletea.app", "http://localhost:3000"],
    #     "allow_credentials": True,
    #     "allow_methods": ["GET", "POST"],
    #     "allow_headers": ["Content-Type", "Authorization"]
    # })