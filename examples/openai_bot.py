"""
Example BubbleTea bot using OpenAI GPT models via LiteLLM
"""

import os
from bubbletea_chat import chatbot, Text, LLM


@chatbot
async def openai_assistant(prompt: str):
    """
    A helpful AI assistant powered by OpenAI's GPT-4
    
    Make sure to set your OpenAI API key:
    export OPENAI_API_KEY=your-api-key-here
    """
    # Initialize the LLM with GPT-4
    llm = LLM(model="gpt-4", temperature=0.7)
    
    # Simple completion
    response = await llm.acomplete(prompt)
    yield Text(response)


@chatbot
async def streaming_openai_bot(prompt: str):
    """
    A streaming bot that uses GPT-3.5-turbo for faster responses
    """
    llm = LLM(model="gpt-3.5-turbo", temperature=0.5)
    
    # Stream the response for better UX
    async for chunk in llm.stream(prompt):
        yield Text(chunk)


@chatbot
async def creative_writer(prompt: str):
    """
    A creative writing assistant using GPT-4 with higher temperature
    """
    llm = LLM(
        model="gpt-4", 
        temperature=0.9,
        max_tokens=1000,
        top_p=0.95
    )
    
    # Add a creative writing system prompt
    messages = [
        {"role": "system", "content": "You are a creative writing assistant. Help users write engaging stories, poems, and creative content."},
        {"role": "user", "content": prompt}
    ]
    
    # Stream the creative response
    async for chunk in llm.astream_with_messages(messages):
        yield Text(chunk)


if __name__ == "__main__":
    # Run the streaming bot by default
    # You can change this to any of the other bots
    from bubbletea_chat import run_server
    run_server(openai_assistant, port=8002)