"""
Cards component example for BubbleTea
"""

import bubbletea_chat as bt
from bubbletea_chat import Card, Cards, Text, Markdown, Image


@bt.chatbot(stream=False)
def cards_bot(message: str):
    """Example bot demonstrating Cards component usage"""
    components = []

    # Check what type of cards the user wants
    if "tall" in message.lower():
        # Create tall cards
        card1 = Card(
            image=Image("https://picsum.photos/300/200?random=1", alt="Product 1"),
            text="First product with simple text",
        )

        card2 = Card(
            image=Image("https://picsum.photos/300/200?random=2", alt="Product 2"),
            markdown=Markdown("**Second product** with *markdown*"),
        )

        components.append(Cards(cards=[card1, card2], orient="tall"))
        components.append(Text("These are tall cards!"))

    else:
        # Create wide cards with card_value
        card1 = Card(
            image=Image("https://picsum.photos/300/200?random=1", alt="Product 1"),
            text="Great product for everyone",
            card_value="product:001",
        )

        card2 = Card(
            image=Image("https://picsum.photos/300/200?random=2", alt="Product 2"),
            markdown=Markdown("**Amazing product** with features"),
            card_value="product:002",
        )

        card3 = Card(
            image=Image("https://picsum.photos/300/200?random=3", alt="Product 3"),
            text="Premium quality product",
            card_value="product:003",
        )

        components.append(Cards(cards=[card1, card2, card3], orient="wide"))
        components.append(Text("These are wide cards! Say 'tall' to see tall cards."))
    
    return components


if __name__ == "__main__":
    bt.run_server(cards_bot, port=8020)
