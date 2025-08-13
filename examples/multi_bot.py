"""
Multiple bots with individual configurations example
"""

import bubbletea_chat as bt
from bubbletea_chat import Text, Markdown, Image, Card, Cards


# ========== Bot 1: Weather Bot ==========
@bt.chatbot("weather", stream=False)
def weather_bot(message: str):
    """Weather information bot at /weather endpoint"""
    cities = {
        "new york": {"temp": "72°F", "condition": "🌤️ Partly cloudy", "humidity": "65%"},
        "london": {"temp": "59°F", "condition": "🌧️ Light rain", "humidity": "80%"},
        "tokyo": {"temp": "77°F", "condition": "☀️ Sunny", "humidity": "55%"},
        "paris": {"temp": "68°F", "condition": "⛅ Cloudy", "humidity": "70%"},
    }
    
    components = []
    city = message.lower().strip()
    
    if city in cities:
        weather = cities[city]
        components.append(Markdown(f"## Weather in {city.title()}"))
        components.append(Text(f"Temperature: {weather['temp']}"))
        components.append(Text(f"Condition: {weather['condition']}"))
        components.append(Text(f"Humidity: {weather['humidity']}"))
    else:
        components.append(Text("Please tell me a city name!"))
        components.append(Text("Available cities: New York, London, Tokyo, Paris"))
    
    return components


# Weather bot configuration
@weather_bot.config
def weather_config():
    return bt.BotConfig(
        name="Weather Bot",
        url="http://localhost:8012/weather",
        is_streaming=False,
        emoji="🌤️",
        initial_text="Tell me a city name for weather info!",
        subtitle="Real-time weather updates",
        description="Get weather information for major cities"
    )


# ========== Bot 2: News Bot ==========
@bt.chatbot("news", stream=False)
async def news_bot(message: str):
    """News bot at /news endpoint"""
    categories = ["tech", "sports", "business", "science"]
    components = []
    
    if any(cat in message.lower() for cat in categories):
        components.append(Markdown(f"## 📰 Latest News"))
        components.append(Text("Here are today's top stories..."))
        
        # Simulate fetching news
        stories = [
            "🔹 Breaking: Major tech announcement today",
            "🔹 Markets show strong growth this quarter",
            "🔹 New scientific discovery announced",
        ]
        
        for story in stories:
            components.append(Text(story))
    else:
        components.append(Text("What news category interests you?"))
        components.append(Text("Available: tech, sports, business, science"))
    
    return components


# News bot configuration
@news_bot.config
def news_config():
    return bt.BotConfig(
        name="News Bot",
        url="http://localhost:8012/news",
        is_streaming=False,
        emoji="📰",
        initial_text="Ask me about the latest news!",
        subtitle="Breaking news & updates",
        description="Get the latest news from various categories"
    )


# ========== Bot 3: Shopping Bot ==========
@bt.chatbot("shop", stream=False)
def shopping_bot(message: str):
    """Shopping assistant bot at /shop endpoint"""
    components = []
    
    if "products" in message.lower() or "shop" in message.lower():
        # Create product cards
        products = [
            Card(
                image=Image("https://picsum.photos/200/150?random=1", alt="Product 1"),
                text="Premium Headphones",
                markdown=Markdown("**$299** - Noise cancelling"),
                card_value="product:headphones"
            ),
            Card(
                image=Image("https://picsum.photos/200/150?random=2", alt="Product 2"),
                text="Smart Watch",
                markdown=Markdown("**$399** - Health tracking"),
                card_value="product:watch"
            ),
            Card(
                image=Image("https://picsum.photos/200/150?random=3", alt="Product 3"),
                text="Wireless Earbuds",
                markdown=Markdown("**$199** - True wireless"),
                card_value="product:earbuds"
            ),
        ]
        
        components.append(Markdown("## 🛍️ Featured Products"))
        components.append(Cards(cards=products, orient="wide"))
        components.append(Text("Click on a product to learn more!"))
    else:
        components.append(Text("Welcome to Shopping Bot!"))
        components.append(Text("Say 'products' or 'shop' to see our catalog"))
    
    return components


# Shopping bot configuration
@shopping_bot.config
def shop_config():
    return bt.BotConfig(
        name="Shopping Assistant",
        url="http://localhost:8012/shop",
        is_streaming=False,
        emoji="🛍️",
        initial_text="Welcome! Type 'products' to browse our catalog!",
        subtitle="Your shopping assistant",
        description="Browse and shop our product catalog",
        visibility="public",
        entrypoint="products"
    )


# ========== Bot 4: Calculator Bot ==========
@bt.chatbot("calc", stream=False)
def calculator_bot(message: str):
    """Simple calculator bot at /calc endpoint"""
    components = []
    
    try:
        # Basic math evaluation (be careful with eval in production!)
        # Only allow basic math operations
        allowed_chars = "0123456789+-*/()., "
        if all(c in allowed_chars for c in message):
            result = eval(message)
            components.append(Markdown(f"## 🧮 Calculation Result"))
            components.append(Text(f"{message} = **{result}**"))
        else:
            components.append(Text("Please enter a valid mathematical expression"))
            components.append(Text("Allowed: numbers and +, -, *, /, (, )"))
    except Exception as e:
        components.append(Text("Invalid expression!"))
        components.append(Text("Example: 2 + 2 * 3"))
    
    return components


# Calculator bot configuration
@calculator_bot.config
def calc_config():
    return bt.BotConfig(
        name="Calculator",
        url="http://localhost:8012/calc",
        is_streaming=False,
        emoji="🧮",
        initial_text="Enter a math expression to calculate!",
        subtitle="Quick calculations",
        description="Simple calculator for basic math"
    )


# ========== Bot 5: Helper Bot (Main Bot) ==========
@bt.chatbot(stream=False)  # Default endpoint at /chat
def helper_bot(message: str):
    """Main helper bot that guides to other bots"""
    components = []
    
    components.append(Markdown("""
## 🤖 BubbleTea Multi-Bot Hub

Welcome! We have several specialized bots available:

### Available Bots:
1. **Weather Bot** (`/weather`) - Get weather information
2. **News Bot** (`/news`) - Latest news updates
3. **Shopping Bot** (`/shop`) - Browse products
4. **Calculator** (`/calc`) - Quick calculations
5. **Helper Bot** (`/chat`) - This bot!

### How to use:
Each bot has its own endpoint. You're currently talking to the Helper Bot.
To use other bots, your application should make requests to their specific endpoints.

Type 'help' for more information about each bot!
    """))
    
    if "help" in message.lower():
        components.append(Markdown("""
### Detailed Bot Information:

**Weather Bot** 🌤️
- Endpoint: `/weather`
- Purpose: Weather information for major cities
- Example: "New York"

**News Bot** 📰
- Endpoint: `/news`
- Purpose: Latest news from various categories
- Example: "tech news"

**Shopping Bot** 🛍️
- Endpoint: `/shop`
- Purpose: Product catalog and shopping
- Example: "show products"

**Calculator** 🧮
- Endpoint: `/calc`
- Purpose: Basic math calculations
- Example: "2 + 2 * 3"
        """))
    
    return components


# Helper bot configuration
@helper_bot.config
def helper_config():
    return bt.BotConfig(
        name="Helper Bot",
        url="http://localhost:8012",
        is_streaming=False,
        emoji="🤖",
        initial_text="Welcome to Multi-Bot Hub! Type 'help' to learn about available bots!",
        subtitle="Your guide to all bots",
        description="Central hub for accessing multiple specialized bots"
    )


if __name__ == "__main__":
    # This will automatically register ALL decorated chatbots
    # Each bot will be available at its specified endpoint:
    # - http://localhost:8012/weather
    # - http://localhost:8012/news
    # - http://localhost:8012/shop
    # - http://localhost:8012/calc
    # - http://localhost:8012/chat (default)
    
    print("Starting Multi-Bot Server with 5 bots...")
    print("Endpoints:")
    print("  - http://localhost:8012/chat (Helper Bot)")
    print("  - http://localhost:8012/weather (Weather Bot)")
    print("  - http://localhost:8012/news (News Bot)")
    print("  - http://localhost:8012/shop (Shopping Bot)")
    print("  - http://localhost:8012/calc (Calculator Bot)")
    print("  - http://localhost:8012/health (Health check)")
    
    bt.run_server(
        port=8012,
        register_all=True  # This ensures all decorated bots are registered
    )