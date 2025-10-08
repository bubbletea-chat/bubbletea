"""
Echo bot with payment integration example for BubbleTea

This bot demonstrates how to:
1. Detect payment-related keywords in messages
2. Request payment for the echo service
3. Process payment confirmations
4. Echo messages after payment
"""

import bubbletea_chat as bt


@bt.chatbot(name="echo-payment-bot", stream=False)
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

        components.append(bt.Text("After payment, I'll confirm and start echoing your messages!"))
        return components

    # Check if message contains greeting
    components.append(bt.Text(f"Echo: {message}!"))
    return components


if __name__ == "__main__":
    bt.run_server(echo_payment_bot, port=8000)
