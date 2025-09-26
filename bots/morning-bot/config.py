"""
Configuration module to load environment variables from .env file
"""

import os
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Configuration class for environment variables"""

    def __init__(self):
        """Initialize configuration by loading environment variables"""
        load_dotenv()

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return os.getenv("OPENAI_API_KEY")

    @property
    def bubbletea_api_key(self) -> Optional[str]:
        """Get BubbleTea API key"""
        return os.getenv("BUBBLETEA_API_KEY")

    @property
    def bubbletea_api_url(self) -> str:
        """Get BubbleTea API URL"""
        return os.getenv("BUBBLETEA_API_URL", "http://localhost:8007")

    @property
    def bubbletea_bot_name(self) -> str:
        """Get BubbleTea bot name"""
        return os.getenv("BUBBLETEA_BOT_NAME", "morning-brief-bot")

    @property
    def bot_port(self) -> int:
        """Get bot server port"""
        return int(os.getenv("BOT_PORT", "8008"))

    @property
    def bot_host(self) -> str:
        """Get bot server host"""
        return os.getenv("BOT_HOST", "0.0.0.0")

    @property
    def supabase_url(self) -> Optional[str]:
        """Get Supabase URL"""
        return os.getenv("SUPABASE_URL")

    @property
    def supabase_key(self) -> Optional[str]:
        """Get Supabase service role key"""
        return os.getenv("SUPABASE_KEY")


config = Config()

OPENAI_API_KEY = config.openai_api_key
BUBBLETEA_API_KEY = config.bubbletea_api_key
BUBBLETEA_API_URL = config.bubbletea_api_url
BUBBLETEA_BOT_NAME = config.bubbletea_bot_name
SUPABASE_URL = config.supabase_url
SUPABASE_KEY = config.supabase_key
