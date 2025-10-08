# Echo Payment Bot

A demonstration bot that shows how to integrate payment requests with chatbot functionality. This bot requests payment when users say "pay" and then provides echo services.

## Features

- 💰 **Payment Request**: Automatically requests payment when user mentions "pay"
- 🔊 **Echo Service**: Echoes user messages after payment
- ✅ **Payment Confirmation**: Receives and processes payment confirmations from the backend
- 📝 **Payment Note**: Includes clear payment purpose in the note

## How It Works

1. **User says "pay"**
   - Bot displays payment request for $2.50
   - Payment note: "Payment for Echo Bot service"

2. **User clicks Pay button**
   - Backend creates payment record
   - Backend sends confirmation message from bot: "✅ Payment successful! Payment code: PAYMENT_123"

3. **Bot receives payment confirmation**
   - Message contains payment code
   - Bot can verify and activate service

4. **Service Active**
   - Bot echoes all user messages
   - Service continues until chat ends

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the bot:
```bash
python bot.py
```

The bot will start on `http://localhost:8000`

## Testing

Test with curl:
```bash
# Request payment
curl -X POST 'http://localhost:8000/chat' \
  -H 'Content-Type: application/json' \
  -d '{"type": "user", "message": "pay"}'

# Test echo functionality
curl -X POST 'http://localhost:8000/chat' \
  -H 'Content-Type: application/json' \
  -d '{"type": "user", "message": "Hello world"}'
```

## Payment Flow

```
┌─────────────────────────────────────────────────────────────┐
│ User: "pay"                                                 │
├─────────────────────────────────────────────────────────────┤
│ Bot: Payment request for $2.50                              │
│      [PaymentRequest component]                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ User clicks "Pay" button                                    │
├─────────────────────────────────────────────────────────────┤
│ Backend:                                                    │
│  1. Creates payment record                                  │
│  2. Generates payment code (PAYMENT_123)                    │
│  3. Creates message from bot with payment confirmation      │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ Bot receives: "✅ Payment successful!                       │
│                Payment code: PAYMENT_123                    │
│                Amount: $2.50"                               │
├─────────────────────────────────────────────────────────────┤
│ Bot: Confirms and activates echo service                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│ User: "Hello world"                                         │
├─────────────────────────────────────────────────────────────┤
│ Bot: "Echo: Hello world!"                                   │
└─────────────────────────────────────────────────────────────┘
```

## Code Structure

```python
@bt.chatbot(name="echo-payment-bot", stream=False)
def echo_payment_bot(message: str):
    # Detect "pay" keyword
    if "pay" in message.lower():
        # Return PaymentRequest component
        return [
            bt.Text("💰 Echo Bot Service Payment"),
            bt.PaymentRequest(
                amount=2.50,
                note="Payment for Echo Bot service"
            )
        ]

    # Echo other messages
    return [bt.Text(f"Echo: {message}!")]
```

## Configuration

- **Bot Name**: `echo-payment-bot`
- **Default Port**: `8000`
- **Payment Amount**: `$2.50`
- **Streaming**: `False` (non-streaming mode)

## Integration with BubbleTea Platform

When deployed to BubbleTea:

1. Users interact with bot through web or mobile app
2. Payment button triggers backend payment creation
3. Backend automatically sends confirmation message from bot
4. Bot processes the confirmation and continues service
5. All messages appear in chronological order in chat

## Customization

You can customize:

- **Payment Amount**: Change `amount=2.50` to your price
- **Payment Note**: Modify the `note` parameter
- **Echo Format**: Update the echo response format
- **Additional Features**: Add more functionality after payment

## Related Examples

- `/examples/payment.py` - Comprehensive payment examples
- `/bots/echo-bot/` - Simple echo bot without payments
- `/examples/simple.py` - Basic bot structure

## Learn More

- [BubbleTea Documentation](https://docs.bubbletea.dev)
- [Payment Component Guide](https://docs.bubbletea.dev/components/payment)
- [Bot Development Tutorial](https://docs.bubbletea.dev/getting-started)
