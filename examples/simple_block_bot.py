"""
Simple example bot demonstrating Block response with minimal setup.
This bot shows the basic usage of Block for testing purposes.
"""

import asyncio
import bubbletea_chat as bt
import httpx
import os
import json
from datetime import datetime

# Bot configuration
@bt.config()
def get_config():
    return bt.BotConfig(
        name="simple-block-bot",
        url="http://localhost:8003",
        is_streaming=False,
        emoji="⏳",
        initial_text="I'm a simple bot that demonstrates blocking. Say anything!",
        sample_questions=[
            "Test the block feature",
            "Show me a long operation",
            "Process something slowly"
        ]
    )

# Configuration
BOT_API_KEY = os.getenv("BUBBLETEA_API_KEY", "bt_fU78vGeD8S0pBngm0gKKtOjbNXo0bvne")
BUBBLETEA_API_URL = os.getenv("BUBBLETEA_API_URL", "http://localhost:8010")

@bt.chatbot()
def simple_block_bot(message: str, conversation_uuid: str):
    """
    Simple bot that always returns a Block response
    """
    # Return block immediately
    print("Reqest received:", message)
    print("Conversation UUID:", conversation_uuid)
    responses = [
        bt.Text("I'll process your message in the background."),
        bt.Block(timeout=30)  # 30 second timeout
    ]
    
    # Start background processing
    asyncio.create_task(process_message_async(message, conversation_uuid))

    print("Responses prepared:", responses)
    
    return responses

async def process_message_async(message: str, conversation_uuid: str):
    """
    Simple background processing
    """
    try:
        print(f"[{datetime.now()}] Starting background processing")
        print(f"  Message: {message}")
        print(f"  Conversation UUID: {conversation_uuid}")
        print(f"  API URL: {BUBBLETEA_API_URL}")
        print(f"  API Key: {BOT_API_KEY[:10]}...") # Show first 10 chars
        
        # Wait 15 seconds
        print(f"[{datetime.now()}] Waiting 15 seconds...")
        await asyncio.sleep(15)
        
        # Send response
        url = f"{BUBBLETEA_API_URL}/v1/developer/conversation/{conversation_uuid}/message"
        headers = {
            "x-api-key": BOT_API_KEY,
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        
        print(f"[{datetime.now()}] Sending completion message to: {url}")
        
        # Create structured content for the message
        content = {
            "type": "text",
            "text": f"✅ Processing complete!\nYou said: '{message}'\nProcessed at: {datetime.now().strftime('%H:%M:%S')}"
        }
        
        # Create payload matching the API format
        payload = {
            "sender": "agent",
            "content": content
        }
        
        print(f"[{datetime.now()}] Request payload: {json.dumps(payload, indent=2)}")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            print(f"[{datetime.now()}] Response status: {response.status_code}")
            print(f"[{datetime.now()}] Response body: {response.text}")
            
            response.raise_for_status()
            print(f"[{datetime.now()}] Processing completed successfully!")
        
    except Exception as e:
        import traceback
        print(f"[{datetime.now()}] ERROR in background processing:")
        print(f"  Exception type: {type(e).__name__}")
        print(f"  Exception message: {str(e)}")
        print(f"  Traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    bt.run_server(simple_block_bot, port=8003)