"""
Example bot demonstrating the @config decorator
"""

import bubbletea_chat as bt

# Define bot configuration
@bt.config()
def get_config():
    return bt.BotConfig(
        name="Weather Bot",
        url="http://localhost:8020",
        is_streaming=False,
        emoji="🌤️",
        initial_text="Hello! I can help you check the weather. Which city would you like to know about?"
    )

# Define the chatbot
@bt.chatbot(name="Weather Bot", stream=True)
def weather_bot(message: str):
    # Simple weather bot logic
    message_lower = message.lower()
    
    if any(city in message_lower for city in ["new york", "nyc"]):
        yield bt.Text("Here's the weather for New York:")
        yield bt.Text("🌤️ Partly cloudy, 72°F (22°C)")
        yield bt.Text("Humidity: 65%")
        yield bt.Text("Wind: 10 mph")
    elif any(city in message_lower for city in ["london"]):
        yield bt.Text("Here's the weather for London:")
        yield bt.Text("🌧️ Light rain, 59°F (15°C)")
        yield bt.Text("Humidity: 80%")
        yield bt.Text("Wind: 15 mph")
    elif any(city in message_lower for city in ["tokyo"]):
        yield bt.Text("Here's the weather for Tokyo:")
        yield bt.Text("☀️ Sunny, 77°F (25°C)")
        yield bt.Text("Humidity: 55%")
        yield bt.Text("Wind: 5 mph")
    else:
        yield bt.Text("Please tell me which city you'd like to check the weather for!")
        yield bt.Text("I know about: New York, London, and Tokyo")

if __name__ == "__main__":
    # Run the server
    bt.run_server(weather_bot, port=8020)