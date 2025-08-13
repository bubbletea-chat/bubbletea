"""
Example BubbleTea bot with vision/image support
"""

from bubbletea_chat import chatbot, Text, Markdown, LLM


@chatbot(stream=False)
async def vision_bot(prompt: str, images: list = None):
    """
    A vision-enabled bot that can analyze images

    This bot demonstrates:
    - Accepting images along with text prompts
    - Using multimodal models like GPT-4V
    - Processing both URL and base64 images
    """
    # Use GPT-4 Vision model
    llm = LLM(model="gpt-4-vision-preview", max_tokens=1000)
    components = []

    if images:
        # Analyze the provided images
        components.append(Text("Analyzing your image..."))

        # Process with vision model
        response = await llm.acomplete_with_images(prompt, images)
        components.append(Markdown(response))
    else:
        # No images - provide instructions
        components.append(Markdown(
            """
## 📸 Vision Bot

I can analyze images! Send me:
- Screenshots to explain
- Photos to describe
- Diagrams to interpret

Just upload an image with your question!
        """
        ))
    
    return components


if __name__ == "__main__":
    from bubbletea_chat import run_server

    run_server(vision_bot, port=8005)
