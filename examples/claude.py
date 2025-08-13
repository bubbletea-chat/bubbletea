"""
Example BubbleTea bot using Anthropic's Claude models
"""

from bubbletea_chat import chatbot, Text, LLM


@chatbot(stream=False)
async def claude_bot(prompt: str):
    """
    A helpful AI assistant powered by Claude

    Make sure to set your Anthropic API key:
    export ANTHROPIC_API_KEY=your-api-key-here
    """
    # Initialize Claude model
    llm = LLM(model="claude-3-7-sonnet-20250219", temperature=0.7)

    # Get the complete response
    response = await llm.acomplete(prompt)
    return [Text(response)]


if __name__ == "__main__":
    from bubbletea_chat import run_server

    run_server(claude_bot, port=8004)
