"""
Example bot demonstrating comprehensive @config decorator usage with all options
"""

import asyncio
import bubbletea_chat as bt
from bubbletea_chat import Block, Text, Markdown, Image


# Define comprehensive bot configuration with ALL available options
@bt.config()
def get_config():
    return bt.BotConfig(
        # Required fields
        name="advanced-weather-bot",  # Handle - unique identifier (no spaces)
        url="http://localhost:8000",  # Bot endpoint URL
        is_streaming=False,  # Whether bot supports streaming
        
        # App Store-like metadata
        display_name="Advanced Weather",  # Display name (max 20 chars)
        subtitle="Global weather insights",  # Subtitle (max 30 chars)
        icon_url="https://picsum.photos/1024/1024?random=weather",  # 1024x1024 PNG icon
        icon_emoji="🌤️",  # Emoji icon alternative
        preview_video_url="https://example.com/preview.mp4",  # Demo video URL
        description="""# Advanced Weather Bot
        
Get comprehensive weather information for cities worldwide with:
- Real-time conditions
- 7-day forecasts  
- Historical data
- Weather alerts
- Air quality index
        
**Perfect for travelers, outdoor enthusiasts, and weather lovers!**
        """,  # Markdown description
        visibility="public",  # "public" or "private"
        discoverable=True,  # Show in bot directory
        entrypoint="weather new york",  # Initial action/page
        
        # Legacy fields (backward compatibility)
        emoji="🌤️",  # Deprecated, use icon_emoji
        initial_text="🌤️ Welcome to Advanced Weather Bot! Ask me about any city's weather!",
        authorization="public",  # Deprecated, use visibility
        authorized_emails=["admin@example.com", "weather@example.com"],  # For private bots
        subscription_monthly_price=0,  # 0 = free, 500 = $5.00
        
        # Advanced configuration
        cors_config={
            "allow_origins": ["https://weather.app", "http://localhost:3000"],
            "allow_credentials": True,
            "allow_methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        },
        
        # Bot examples
        example_chats=[
            "What's the weather in New York?",
            "Show me Tokyo forecast",
            "Is it raining in London?",
            "Weather alerts for Miami",
            "Compare Paris and Berlin weather"
        ]
    )


# Async function to simulate weather data fetching
async def fetch_weather_data(city: str) -> dict:
    """Simulate async weather API call"""
    # Simulate API delay
    await asyncio.sleep(0.5)
    
    weather_data = {
        "new york": {
            "temp": "72°F (22°C)",
            "condition": "🌤️ Partly cloudy",
            "humidity": "65%",
            "wind": "10 mph NW",
            "uv_index": "6 (High)",
            "air_quality": "Good (AQI: 45)"
        },
        "london": {
            "temp": "59°F (15°C)", 
            "condition": "🌧️ Light rain",
            "humidity": "80%",
            "wind": "15 mph SW",
            "uv_index": "2 (Low)",
            "air_quality": "Moderate (AQI: 68)"
        },
        "tokyo": {
            "temp": "77°F (25°C)",
            "condition": "☀️ Sunny",
            "humidity": "55%",
            "wind": "5 mph E",
            "uv_index": "9 (Very High)",
            "air_quality": "Good (AQI: 42)"
        }
    }
    
    return weather_data.get(city.lower(), None)


# Define the chatbot with async functionality and Block components
@bt.chatbot(name="advanced-weather-bot", stream=False)
async def weather_bot(message: str):
    """Advanced weather bot with async data fetching and Block components"""
    message_lower = message.lower()
    
    # Run async function to fetch weather data
    weather_info = None
    city_name = None
    
    for city in ["new york", "nyc", "london", "tokyo"]:
        if city in message_lower:
            city_key = "new york" if city in ["new york", "nyc"] else city
            weather_info = await fetch_weather_data(city_key)
            city_name = city_key.title()
            break
    
    if weather_info:
        # Return Block component with comprehensive weather info
        weather_block = Block(
            components=[
                Image(f"https://picsum.photos/400/200?random={city_name.lower()}", 
                      alt=f"{city_name} skyline"),
                Markdown(f"## 🌤️ Weather in {city_name}"),
                Text(f"🌡️ Temperature: {weather_info['temp']}"),
                Text(f"☁️ Condition: {weather_info['condition']}"),
                Text(f"💧 Humidity: {weather_info['humidity']}"),
                Text(f"💨 Wind: {weather_info['wind']}"),
                Text(f"☀️ UV Index: {weather_info['uv_index']}"),
                Text(f"🏭 Air Quality: {weather_info['air_quality']}"),
                Markdown("*Last updated: Just now*")
            ],
            title=f"Current Weather - {city_name}",
            style="info",
            collapsible=True
        )
        
        return [weather_block]
    else:
        # Return help Block component
        help_block = [
                Markdown("## 🌍 Advanced Weather Bot"),
                Text("I can provide detailed weather information for major cities!"),
                Markdown("### Available Cities:"),
                Text("• New York (NYC)"),
                Text("• London"),
                Text("• Tokyo"),
                Markdown("### Try asking:"),
                Text("• 'What's the weather in Tokyo?'"),
                Text("• 'Show me London weather'"),
                Text("• 'New York forecast'"),
                Block(60)
            ]
        
        return help_block


if __name__ == "__main__":
    # Run the server with the comprehensive config
    print("Starting Advanced Weather Bot with full configuration...")
    print("Available at: http://localhost:8020")
    print("Try asking: 'What's the weather in New York?'")
    bt.run_server(weather_bot, port=8020)
