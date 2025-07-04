"""
Test script to verify Cards component functionality
"""

import bubbletea_chat as bt
from bubbletea_chat import Card, Cards, Text, Markdown, Image

@bt.chatbot(name="mybot", stream=False)
def example_cards_usage_wide(prompt: str):
    """Example of how to use the Cards component"""
  # Create individual cards with card_value
    card1 = Card(
        image=Image(
            "https://picsum.photos/300/200?random=1", 
            alt="Product 1",
            content="## Product 1\nA great product for everyone"
        ),
        text="This is additional text content for the card.",
        card_value="product:001"  # Value that will be inserted when clicked
    )
    
    card2 = Card(
        image=Image(
            "https://picsum.photos/300/200?random=2", 
            alt="Product 2",
            content="**Another amazing product** with special features"
        ),
        markdown=Markdown("**Bold text** and *italic text* with [links](https://picsum.photos/300/200?random=2)"),
        card_value="product:002"  # Different from display text
    )
    
    card3 = Card(
        image=Image(
            "https://picsum.photos/300/200?random=3", 
            alt="Product 3",
            content="*The best product yet* - premium quality"
        ),
        card_value="product:003"
    )
    
    wide_cards = Cards(
        cards=[card1, card2, card3],
        orient="wide"
    )
    return wide_cards


@bt.chatbot(name="mybot", stream=False)
def example_cards_usage_tall(prompt: str):
    """Example of how to use the Cards component"""
  # Create individual cards
    card1 = Card(
        image=Image(
            "https://picsum.photos/300/200?random=1", 
            alt="Product 1",
            content="## Product 1\nA great product for everyone"
        ),
        text="This is additional text content for the card."
    )
    
    card2 = Card(
        image=Image(
            "https://picsum.photos/300/200?random=2", 
            alt="Product 2",
            content="**Another amazing product** with special features"
        ),
        markdown=Markdown("**Bold text** and *italic text* with [links](https://picsum.photos/300/200?random=2)")
    )
    
    # Create a Cards component with tall orientation
    tall_cards = Cards(
        cards=[card1, card2],
        orient="tall"
    )
    
    return tall_cards

if __name__ == "__main__":
    bt.run_server(example_cards_usage_wide, port=8020, host='0.0.0.0')
    bt.run_server(example_cards_usage_tall, port=8021, host='0.0.0.0')
