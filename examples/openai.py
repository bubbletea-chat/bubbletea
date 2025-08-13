"""
Example BubbleTea bot using OpenAI GPT models
"""

from bubbletea_chat import chatbot, Text, LLM


@chatbot(stream=False)
async def openai_bot(prompt: str):
    """
    A helpful AI assistant powered by OpenAI's GPT

    Make sure to set your OpenAI API key:
    export OPENAI_API_KEY=your-api-key-here
    """
    # Initialize with GPT model
    llm = LLM(model="gpt-4", temperature=0.7)

    # Get the complete response
    response = await llm.acomplete(prompt)
    return [Text(response)]


if __name__ == "__main__":
    from bubbletea_chat import run_server

    run_server(openai_bot, port=8002)
