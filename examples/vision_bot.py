"""
Example BubbleTea bot with vision/image support using multimodal LLMs
"""

import os
from bubbletea_chat import chatbot, Text, Markdown, LLM, ImageInput, Image


@chatbot
async def vision_bot(prompt: str, images: list = None):
    """
    A vision-enabled bot that can analyze images
    
    This bot demonstrates:
    - Accepting images along with text prompts
    - Using multimodal models (GPT-4V, Claude 3, Gemini)
    - Handling both URL and base64 images
    """
    # Use GPT-4 Vision by default
    llm = LLM(model="gpt-4-vision-preview", max_tokens=1000)
    
    if images:
        # Bot received images - analyze them
        yield Text("I can see you've shared some images. Let me analyze them...")
        
        # Use the LLM with images
        response = await llm.acomplete_with_images(prompt, images)
        yield Markdown(response)
    else:
        # No images - provide instructions
        yield Markdown("""
## 📸 Vision Bot

I can analyze images! Try sending me:
- Screenshots to explain
- Photos to describe
- Diagrams to interpret
- Art to analyze

Just upload an image along with your question!

**Supported formats**: JPEG, PNG, GIF, WebP
        """)


@chatbot
async def gpt4v_analyst(prompt: str, images: list = None):
    """
    GPT-4 Vision analyst for detailed image analysis
    """
    if not images:
        yield Text("Please send me an image to analyze!")
        return
    
    llm = LLM(model="gpt-4-vision-preview", temperature=0.5)
    
    # Streaming analysis
    yield Text("🔍 Analyzing image with GPT-4 Vision...")
    
    async for chunk in llm.stream_with_images(prompt or "What's in this image?", images):
        yield Text(chunk)


@chatbot
async def claude_vision_bot(prompt: str, images: list = None):
    """
    Claude 3 vision bot for image understanding
    """
    if not images:
        yield Text("Send me an image and I'll analyze it with Claude 3!")
        return
    
    # Claude 3 models support vision
    llm = LLM(model="claude-3-sonnet-20240229", temperature=0.7)
    
    yield Text("🎨 Analyzing with Claude 3...")
    
    response = await llm.acomplete_with_images(
        prompt or "Describe this image in detail.",
        images
    )
    
    yield Markdown(response)


@chatbot
async def gemini_vision_bot(prompt: str, images: list = None):
    """
    Gemini Pro Vision for multimodal understanding
    """
    if not images:
        yield Text("Share an image for Gemini to analyze!")
        return
    
    llm = LLM(model="gemini/gemini-pro-vision", temperature=0.5)
    
    yield Text("🌟 Processing with Gemini Vision...")
    
    response = await llm.acomplete_with_images(
        prompt or "What can you tell me about this image?",
        images
    )
    
    yield Markdown(response)


@chatbot(stream=False)
async def multi_image_analyzer(prompt: str, images: list = None):
    """
    Analyzes multiple images at once (non-streaming)
    """
    if not images:
        return Text("Please upload one or more images for analysis!")
    
    llm = LLM(model="gpt-4-vision-preview")
    
    # Build a detailed prompt based on number of images
    if len(images) == 1:
        analysis_prompt = f"Analyze this image: {prompt or 'Provide a detailed description.'}"
    else:
        analysis_prompt = f"Compare and analyze these {len(images)} images: {prompt or 'What are the similarities and differences?'}"
    
    # Get complete analysis
    response = await llm.acomplete_with_images(analysis_prompt, images)
    
    return [
        Markdown(f"## 🖼️ Analysis of {len(images)} Image(s)"),
        Markdown(response),
        Text(f"✅ Analyzed {len(images)} image(s) successfully!")
    ]


@chatbot
async def image_to_code_bot(prompt: str, images: list = None):
    """
    Converts UI screenshots to code
    """
    if not images:
        yield Markdown("""
## 💻 Image to Code Bot

Send me a screenshot of a UI and I'll help you recreate it in code!

**I can generate:**
- HTML/CSS from mockups
- React components from designs  
- Python GUI code from screenshots
- And more!

Just upload a UI screenshot and optionally specify your preferred framework.
        """)
        return
    
    llm = LLM(model="gpt-4-vision-preview", temperature=0.3)
    
    code_prompt = prompt or "Generate HTML and CSS code to recreate this UI design."
    if "react" in prompt.lower():
        code_prompt = "Generate a React component that recreates this UI design."
    elif "python" in prompt.lower():
        code_prompt = "Generate Python code (tkinter or PyQt) to recreate this UI."
    
    yield Text("🛠️ Converting image to code...")
    
    response = await llm.acomplete_with_images(code_prompt, images)
    
    yield Markdown(response)


# Example of handling base64 images
@chatbot
async def base64_example_bot(prompt: str, images: list = None):
    """
    Example showing how to handle base64 encoded images
    """
    if not images:
        yield Text("This bot demonstrates base64 image handling. Send me an image!")
        return
    
    # Check if we received base64 or URL images
    for i, img in enumerate(images):
        if img.base64:
            yield Text(f"📦 Received base64 encoded image {i+1}")
        elif img.url:
            yield Text(f"🔗 Received image URL {i+1}")
    
    # Process with LLM
    llm = LLM(model="gpt-4-vision-preview")
    response = await llm.acomplete_with_images(
        prompt or "What's in this image?",
        images
    )
    
    yield Markdown(response)


async def image_generation(prompt: str):
    """
    A vision-enabled bot that generates images from text prompts.

    This bot demonstrates:
    - Generating images from descriptive text
    - Using multimodal models (GPT-4V, Claude 3, Gemini)
    """
    # Use GPT-4 Vision by default
    llm = LLM(model="gpt-4.1-mini")
    if prompt:
        # Generate image from the text prompt
        response = llm.generate_image(prompt)
        yield Image(response)
    else:
        # No prompt provided - show usage instructions
        yield Markdown("""
            ## 🎨 AI Image Generator

            I can create images from your text prompts using powerful AI models!

            Try prompts like:
            - *"A futuristic cityscape at sunset"*
            - *"A cute robot playing guitar in a forest"*
            - *"An ancient map with fantasy landmarks"*

            👉 Just type your description and I'll generate an image for you!

            **Note:** No need to upload an image — just provide your idea as text.
        """)


if __name__ == "__main__":
    # Run the vision bot by default
    from bubbletea_chat import run_server
    run_server(vision_bot, port=8008)