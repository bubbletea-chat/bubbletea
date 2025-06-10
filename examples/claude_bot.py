"""
Example BubbleTea bot using Anthropic's Claude models via LiteLLM
"""

import os
from bubbletea_chat import chatbot, Text, Markdown, LLM


@chatbot
async def claude_assistant(prompt: str):
    """
    A helpful AI assistant powered by Claude 3 Opus
    
    Make sure to set your Anthropic API key:
    export ANTHROPIC_API_KEY=your-api-key-here
    """
    # Initialize with Claude 3 Opus
    llm = LLM(model="claude-3-7-sonnet-20250219", temperature=0.7)
    
    response = await llm.acomplete(prompt)
    yield Text(response)


@chatbot
async def claude_sonnet_bot(prompt: str):
    """
    A balanced bot using Claude 3 Sonnet for good performance and quality
    """
    llm = LLM(model="claude-3-7-sonnet-20250219", temperature=0.5)
    
    # Stream the response
    async for chunk in llm.stream(prompt):
        yield Text(chunk)


@chatbot
async def claude_haiku_bot(prompt: str):
    """
    A fast and efficient bot using Claude 3 Haiku
    """
    llm = LLM(model="claude-3-7-sonnet-20250219", temperature=0.5)
    
    # Haiku is fast, so streaming provides great UX
    async for chunk in llm.stream(prompt):
        yield Text(chunk)


@chatbot
async def claude_analyst(prompt: str):
    """
    An analytical assistant using Claude with structured thinking
    """
    llm = LLM(
        model="claude-3-7-sonnet-20250219",
        temperature=0.3,  # Lower temperature for analytical tasks
        max_tokens=2000
    )
    
    # Add an analytical system prompt
    messages = [
        {"role": "system", "content": "You are a thoughtful analyst. Break down problems systematically, consider multiple perspectives, and provide well-reasoned responses. Use clear structure in your answers."},
        {"role": "user", "content": prompt}
    ]
    
    # Stream with markdown for better formatting
    full_response = ""
    async for chunk in llm.astream_with_messages(messages):
        full_response += chunk
        yield Markdown(full_response)


@chatbot
async def claude_creative_bot(prompt: str):
    """
    A creative assistant using Claude with higher temperature
    """
    llm = LLM(
        model="claude-3-7-sonnet-20250219",
        temperature=0.9,  # Higher temperature for creativity
        max_tokens=1500,
        top_p=0.95
    )
    
    messages = [
        {"role": "system", "content": "You are a creative companion. Help users explore ideas, create stories, brainstorm solutions, and think outside the box. Be imaginative and engaging."},
        {"role": "user", "content": prompt}
    ]
    
    async for chunk in llm.astream_with_messages(messages):
        yield Text(chunk)


if __name__ == "__main__":
    # Run the Claude Sonnet bot by default (good balance of speed and quality)
    from bubbletea_chat import run_server
    run_server(claude_assistant, port=8004)