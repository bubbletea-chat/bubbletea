"""
Image Generation Bot Example

Demonstrates how to create images using AI models.
Requires: OPENAI_API_KEY for DALL-E generation
"""

import bubbletea_chat as bt
from bubbletea_chat import LLM, Text, Image, Markdown


@bt.chatbot(stream=False)
async def image_generator(prompt: str):
    """
    An AI image generation bot that creates images from text
    """
    components = []
    
    if not prompt:
        components.append(Markdown("""
## 🎨 AI Image Generator

I can create images from text! Try:
- "A futuristic city at sunset"
- "A cute robot in a forest"
- "Abstract art with vibrant colors"

Just type your description!
        """))
        return components

    # Initialize image generation model
    llm = LLM(model="dall-e-3")

    components.append(Text(f"🎨 Creating: {prompt}"))

    # Generate the image
    image_url = await llm.agenerate_image(prompt)
    components.append(Image(image_url, alt=prompt))
    components.append(Text("✨ Your image is ready!"))
    
    return components


if __name__ == "__main__":
    bt.run_server(image_generator, port=8007)
