"""
Echo Payment Bot - Demonstrates payment integration with echo functionality

This bot shows how to:
1. Detect payment keywords and request payment
2. Receive payment confirmation messages
3. Provide services after payment
"""

import bubbletea_chat as bt


@bt.chatbot("echo-payment-bot")
def echo_payment_bot(message: str):
    """
    An echo bot that requests payment when user says 'pay'.
    After receiving payment confirmation, it echoes the message.
    """
    components = []
    message_lower = message.lower()

    # Check if user wants to pay
    if "pay" in message_lower:
        components.append(bt.Text("💰 Echo Bot Service Payment"))
        components.append(bt.Markdown("""
Welcome to **Echo Bot Premium**!

To use this echo service, please complete the payment below.
After payment, I'll echo all your messages with style!
        """))

        # Request payment with note explaining the service
        components.append(bt.PaymentRequest(
            amount=2.50,
            note="Payment for Echo Bot service"
        ))

        return components

    # Check if message contains greeting
    components.append(bt.Text(f"Echo: {message}!"))
    return components


@echo_payment_bot.config
def get_config():
    return bt.BotConfig(
        # Required fields
        name="echo-payment-bot",
        url="localhost:8000",
        is_streaming=False,

        # Metadata for discovery and display
        display_name="Echo Payment Bot",  # Max 20 characters
        subtitle="Echo with payment demo",  # Max 30 characters
        icon_url="",  # Optional icon URL
        preview_video_url="",  # Optional preview video
        description="""
# Echo Payment Bot 💰🔊

A demonstration bot that shows how to integrate payment requests with chatbot functionality. Request payment with a simple keyword and echo messages!

## 💡 Features
- **Payment Integration** - Request payment when user says "pay"
- **Payment Confirmation** - Receives payment codes from backend
- **Echo Service** - Echoes your messages after setup
- **Simple Implementation** - Great for learning payment flow

## ✨ How to Use
1. Say **"pay"** to see a payment request
2. Click the **Pay** button to complete payment
3. Bot receives confirmation with payment code
4. Start chatting and get your messages echoed back!

## 💳 Payment Flow
- **Amount**: $2.50
- **Note**: "Payment for Echo Bot service"
- **Confirmation**: Automatic message from bot with payment code

## 🔄 Best For
- Learning payment integration
- Testing payment components
- Building payment-based bots
- Understanding payment confirmations

## ⚙️ Technical Details
- Payment messages sent from bot's account
- Backend generates unique payment codes (PAYMENT_XXX)
- Bot can detect and process payment confirmations
- Clean separation between payment and service logic
        """,
        visibility="public",

        # Welcome message
        initial_text='👋 Welcome to Echo Payment Bot! Say "pay" to request payment for the echo service, or just type a message to see it echoed back.',
    )


if __name__ == "__main__":
    bt.run_server(echo_payment_bot, port=8080, host="0.0.0.0")
