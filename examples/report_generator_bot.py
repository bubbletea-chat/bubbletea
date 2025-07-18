"""
Example bot that generates detailed reports using Block response.
This bot simulates report generation that takes 30-45 seconds.
"""

import asyncio
import bubbletea_chat as bt
import httpx
from datetime import datetime
import os
import random

# Bot configuration
@bt.config()
def get_config():
    return bt.BotConfig(
        name="report-generator-bot",
        url="http://localhost:8002",
        is_streaming=False,  # Non-streaming bot
        emoji="📊",
        initial_text="Hello! I can generate detailed reports for you. What kind of report do you need?",
        sample_questions=[
            "Generate a sales report for Q4 2023",
            "Create a performance analysis report",
            "Build a market research report on AI trends"
        ]
    )

# Global client for making API calls
client = httpx.AsyncClient()

# Bot API key (set this as environment variable)
BOT_API_KEY = os.getenv("BUBBLETEA_API_KEY", "bt_fU78vGeD8S0pBngm0gKKtOjbNXo0bvne")
BUBBLETEA_API_URL = os.getenv("BUBBLETEA_API_URL", "http://localhost:8000")

@bt.chatbot()
def report_generator(message: str, conversation_uuid: str):
    """
    Main bot function that returns Block response for report generation
    """
    # Determine processing time based on report complexity
    processing_time = random.randint(30, 45)
    
    # Send initial messages and block
    responses = [
        bt.Text(f"📋 I'll generate a report on: '{message}'"),
        bt.Text(f"Estimated time: {processing_time} seconds"),
        bt.Block(timeout=60)  # 60 second timeout
    ]
    
    # Start background task to generate report
    asyncio.create_task(generate_report_async(message, conversation_uuid, processing_time))
    
    return responses

async def generate_report_async(topic: str, conversation_uuid: str, processing_time: int):
    """
    Background task that simulates report generation
    """
    try:
        print(f"[{datetime.now()}] Starting report generation for conversation {conversation_uuid}")
        
        # Simulate different stages of report generation
        stages = [
            "Collecting data...",
            "Analyzing information...",
            "Generating insights...",
            "Formatting report..."
        ]
        
        for i, stage in enumerate(stages):
            await asyncio.sleep(processing_time / len(stages))
            print(f"[{datetime.now()}] {stage}")
        
        # Generate mock report content
        report_content = f"""
# Report: {topic}

## Executive Summary
This report provides a comprehensive analysis of {topic.lower()}.

## Key Findings
1. **Data Point 1**: Significant growth observed in the analyzed period
2. **Data Point 2**: Market trends indicate positive outlook
3. **Data Point 3**: Strategic recommendations for improvement

## Detailed Analysis
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

### Section 1: Market Overview
- Current market size: $XX billion
- Growth rate: XX% YoY
- Key players: Company A, Company B, Company C

### Section 2: Performance Metrics
| Metric | Q1 | Q2 | Q3 | Q4 |
|--------|----|----|----|----|
| Revenue | $1M | $1.2M | $1.5M | $1.8M |
| Growth | 10% | 20% | 25% | 20% |

## Recommendations
1. Focus on growth areas identified in the analysis
2. Implement suggested optimizations
3. Monitor key metrics quarterly

## Conclusion
Based on our analysis, the outlook for {topic.lower()} is positive with several opportunities for growth.

---
*Report generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        # Create proper bt components for the response
        components = [
            bt.Text("✅ Report generation complete!"),
            bt.Markdown(report_content),
            bt.Pills([
                bt.Pill("Download PDF", "download_pdf"),
                bt.Pill("Share Report", "share"),
                bt.Pill("Generate Another", "new_report")
            ])
        ]
        
        # Send completion message via Developer API
        await send_completion_message(conversation_uuid, components)
        print(f"[{datetime.now()}] Report generation completed for conversation {conversation_uuid}")
        
    except Exception as e:
        print(f"Error in report generation: {e}")
        error_component = bt.Text(f"❌ Sorry, report generation failed: {str(e)}")
        await send_completion_message(conversation_uuid, [error_component])

async def send_completion_message(conversation_uuid: str, components: list):
    """
    Send message to BubbleTea backend via Developer API
    """
    url = f"{BUBBLETEA_API_URL}/v1/developer/conversation/{conversation_uuid}/message"
    headers = {
        "Authorization": f"Bearer {BOT_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Convert bt components to dict format for the API
    components_dict = [component.model_dump() for component in components]
    content = {"components": components_dict}
    
    try:
        response = await client.post(
            url,
            json={"content": content},
            headers=headers
        )
        response.raise_for_status()
        print(f"Message sent successfully to conversation {conversation_uuid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    # Run the bot server
    bt.run_server(report_generator, port=8002)