"""
Example BubbleTea bot using Google's Gemini models via LiteLLM
"""

import os
from bubbletea_chat import chatbot, Text, Markdown, LLM


@chatbot
async def gemini_assistant(prompt: str):
    """
    A helpful AI assistant powered by Google's Gemini Pro
    
    Make sure to set your Google API key:
    export GEMINI_API_KEY=your-api-key-here
    """
    # Initialize with Gemini Pro
    llm = LLM(model="gemini/gemini-pro", temperature=0.7)
    
    response = await llm.acomplete(prompt)
    yield Text(response)


@chatbot
async def gemini_flash_bot(prompt: str):
    """
    A fast bot using Gemini Flash for quick responses
    """
    llm = LLM(model="gemini/gemini-1.5-flash", temperature=0.5)
    
    # Stream the response
    async for chunk in llm.stream(prompt):
        yield Text(chunk)


@chatbot
async def gemini_code_helper(prompt: str):
    """
    A programming assistant using Gemini with code-focused prompts
    """
    llm = LLM(
        model="gemini/gemini-pro",
        temperature=0.3,  # Lower temperature for more precise code
        max_tokens=2000
    )
    
    # Add a code-focused system prompt
    messages = [
        {"role": "system", "content": "You are an expert programming assistant. Provide clear, concise code examples and explanations. Use markdown for code blocks."},
        {"role": "user", "content": prompt}
    ]
    
    # Get the full response for code (streaming can break formatting)
    response = await llm.astream_with_messages(messages)
    
    # Use Markdown component for better code rendering
    full_response = ""
    async for chunk in response:
        full_response += chunk
        yield Markdown(full_response)


@chatbot
async def gemini_multimodal_bot(prompt: str):
    """
    A multimodal bot that can process text and images
    Note: Image handling would need to be implemented in the chatbot decorator
    """
    llm = LLM(model="gemini/gemini-1.5-pro", temperature=0.5)
    
    # For now, just handle text
    # In a real implementation, you'd check if there are images in the prompt
    async for chunk in llm.stream(prompt):
        yield Text(chunk)


if __name__ == "__main__":
    # Run the Gemini Flash bot by default
    from bubbletea_chat import run_server
    run_server(gemini_flash_bot, port=8003)