"""
Bubble Tea Components Showcase Bot
This bot demonstrates all available Bubble Tea components with example data
"""

import logging
from typing import Any, List
import os

import bubbletea_chat as bt
from dotenv import load_dotenv

load_dotenv()
from bubbletea_chat.components import (
    Text,
    Image,
    Markdown,
    Card,
    Cards,
    Pill,
    Pills,
    Video,
    Block,
    Error,
)

logger = logging.getLogger(__name__)


def show_text_component():
    """Show Text component example"""
    return [
        Text("📝 Text Component Example:"),
        Text("This is a simple text component. It displays plain text messages."),
        Text("You can use it for basic communication with users."),
        Text("Example: Hello, welcome to our chatbot! 👋"),
    ]


def show_markdown_component():
    """Show Markdown component example"""
    markdown_content = """
## 📄 Markdown Component Example

The Markdown component supports **rich text formatting**:

- **Bold text** with `**text**`
- *Italic text* with `*text*`
- ~~Strikethrough~~ with `~~text~~`
- `Code snippets` with backticks
- [Links](https://example.com) with `[text](url)`

### Lists:
1. Ordered item 1
2. Ordered item 2
   - Nested unordered item
   - Another nested item

> Blockquotes are also supported!

```python
# Code blocks too!
def hello():
    return "Hello, Bubble Tea!"
```
"""
    return [Text("📄 Markdown Component Example:"), Markdown(markdown_content)]


def show_image_component():
    """Show Image component example"""
    return [
        Text("🖼️ Image Component Example:"),
        Image(
            url="https://images.unsplash.com/photo-1558857563-b371033873b8?w=600",
            alt="A delicious bubble tea",
            content="Beautiful bubble tea with tapioca pearls",
        ),
        Text("Images can have captions and alt text for accessibility!"),
    ]


def show_cards_component():
    """Show Cards component example"""
    components = [Text("🎴 Cards Component Example (Wide orientation):")]

    wide_cards = Cards(
        cards=[
            Card(
                image=Image(
                    url="https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=300",
                    alt="Taro Bubble Tea",
                ),
                text="Taro Milk Tea",
                markdown=Markdown("**Price:** $5.99\n*Our bestseller!*"),
                card_value="taro_tea",
            ),
            Card(
                image=Image(
                    url="https://images.unsplash.com/photo-1541696490-8744a5dc0228?w=300",
                    alt="Matcha Bubble Tea",
                ),
                text="Matcha Latte",
                markdown=Markdown("**Price:** $6.49\n*Premium grade matcha*"),
                card_value="matcha_tea",
            ),
            Card(
                image=Image(
                    url="https://images.unsplash.com/photo-1525803377221-4f6ccdaa5133?w=300",
                    alt="Brown Sugar Bubble Tea",
                ),
                text="Brown Sugar Boba",
                markdown=Markdown("**Price:** $5.49\n*Classic favorite*"),
                card_value="brown_sugar_tea",
            ),
        ],
        orient="wide",
    )
    components.append(wide_cards)

    components.append(Text("\n🎴 Cards Component Example (Tall orientation):"))
    tall_cards = Cards(
        cards=[
            Card(
                image=Image(
                    url="https://images.unsplash.com/photo-1478145046317-39f10e56b5e9?w=200&h=300",
                    alt="City Skyline",
                ),
                text="Urban Adventures",
                markdown=Markdown("*Explore the city*"),
                card_value="urban",
            ),
            Card(
                image=Image(
                    url="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=200&h=300",
                    alt="Mountain View",
                ),
                text="Mountain Escapes",
                markdown=Markdown("*Find your peace*"),
                card_value="mountain",
            ),
        ],
        orient="tall",
    )
    components.append(tall_cards)

    return components


def show_pills_component():
    """Show Pills component example"""
    return [
        Text("💊 Pills Component Example:"),
        Text("Pills are clickable buttons for quick actions:"),
        Pills(
            pills=[
                Pill("Order Now", pill_value="order"),
                Pill("View Menu", pill_value="menu"),
                Pill("Store Locations", pill_value="locations"),
                Pill("Contact Us", pill_value="contact"),
                Pill("Special Offers", pill_value="offers"),
            ]
        ),
        Text("Each pill can have a value that gets sent when clicked!"),
    ]


def show_video_component():
    """Show Video component example"""
    return [
        Text("🎥 Video Component Example:"),
        Video(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        Text("Videos are embedded directly in the chat interface!"),
    ]


def show_block_component():
    """Show Block component example"""
    return [
        Text("⏳ Block Component Example:"),
        Block(timeout=30),
        Text("The Block component shows a loading state."),
        Text("It's useful for indicating long-running operations."),
        Text("This one has a 30-second timeout."),
    ]


def show_error_component():
    """Show Error component example"""
    return [
        Text("❌ Error Component Example:"),
        Error(
            title="Connection Error",
            description="Unable to connect to the server. Please check your internet connection and try again.",
            code="ERR_NETWORK_001",
        ),
        Text("Errors can include title, description, and error codes."),
    ]


def show_all_components():
    """Show all components in one response"""
    components = []

    components.append(Text("🎨 Complete Bubble Tea Components Showcase:"))
    components.append(Text("\n"))

    # Add all component examples
    components.extend(show_text_component())
    components.append(Text("\n"))

    components.extend(show_markdown_component())
    components.append(Text("\n"))

    components.extend(show_image_component())
    components.append(Text("\n"))

    components.extend(show_cards_component())
    components.append(Text("\n"))

    components.extend(show_pills_component())
    components.append(Text("\n"))

    components.extend(show_video_component())
    components.append(Text("\n"))

    components.extend(show_block_component())
    components.append(Text("\n"))

    components.extend(show_error_component())

    return components


def show_component_menu():
    """Show the main menu with component options"""
    return [
        Text("🎨 Bubble Tea Components Showcase"),
        Text("Click on any component to see an example:"),
        Pills(
            pills=[
                Pill("📝 Text", pill_value="show_text"),
                Pill("📄 Markdown", pill_value="show_markdown"),
                Pill("🖼️ Image", pill_value="show_image"),
                Pill("🎴 Cards", pill_value="show_cards"),
                Pill("💊 Pills", pill_value="show_pills"),
                Pill("🎥 Video", pill_value="show_video"),
                Pill("⏳ Block", pill_value="show_block"),
                Pill("❌ Error", pill_value="show_error"),
                Pill("🎯 Show All Components", pill_value="show_all"),
            ]
        ),
    ]


@bt.chatbot("components-showcase")
def components_showcase_bot(
    message: str, user_uuid: str = None, conversation_uuid: str = None
) -> List[Any]:
    """
    Bot that showcases all available Bubble Tea components
    """
    text = message.strip()

    # Check if user wants to go back to menu first
    if text == "show_menu":
        return show_component_menu()

    # Check if it's a pill click
    if text.startswith("show_"):
        components = []

        if text == "show_text":
            components = show_text_component()
        elif text == "show_markdown":
            components = show_markdown_component()
        elif text == "show_image":
            components = show_image_component()
        elif text == "show_cards":
            components = show_cards_component()
        elif text == "show_pills":
            components = show_pills_component()
        elif text == "show_video":
            components = show_video_component()
        elif text == "show_block":
            components = show_block_component()
        elif text == "show_error":
            components = show_error_component()
        elif text == "show_all":
            components = show_all_components()

        # Add a way to go back to menu
        if text != "show_all":
            components.append(Text("\n"))
            components.append(
                Pills(
                    pills=[
                        Pill("🔙 Back to Menu", pill_value="show_menu"),
                        Pill("🎯 Show All Components", pill_value="show_all"),
                    ]
                )
            )
        else:
            components.append(Text("\n"))
            components.append(
                Pills(pills=[Pill("🔙 Back to Menu", pill_value="show_menu")])
            )

        return components

    # Default: show menu for any message (except pill clicks which are handled above)
    return show_component_menu()


@components_showcase_bot.config
def get_config():
    return bt.BotConfig(
        name="components-showcase",
        display_name="Components Bot",
        url=os.getenv("BOT_URL", "http://localhost:5004"),
        icon_url="https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=400",
        is_streaming=False,
        initial_text="🎨 Ask me to 'show components' or click on a component pill to see examples!",
    )

if __name__ == "__main__":
    bt.run_server(components_showcase_bot, port=8080, host="0.0.0.0")
