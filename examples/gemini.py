"""
Example BubbleTea bot using Google's Gemini models
"""

from bubbletea_chat import chatbot, Text, LLM


@chatbot(stream=False)
async def gemini_bot(prompt: str):
    """
    A helpful AI assistant powered by Google's Gemini

    Make sure to set your Google API key:
    export GEMINI_API_KEY=your-api-key-here
    """
    # Initialize with Gemini model
    llm = LLM(model="gemini/gemini-pro", temperature=0.7)

    # Get the complete response
    response = await llm.acomplete(prompt)
    return [Text(response)]


if __name__ == "__main__":
    from bubbletea_chat import run_server

    run_server(gemini_bot, port=8003)
