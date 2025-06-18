#!/usr/bin/env python3
"""
Image Generation Bot Examples

This file demonstrates how to create image generation bots using BubbleTea.
It includes several specialized bots that generate images using AI models.

Requirements:
- Set OPENAI_API_KEY for DALL-E image generation
- Or use other providers supported by LiteLLM
"""

import bubbletea_chat as bt
from bubbletea_chat import LLM, Text, Image, Markdown


@bt.chatbot
async def image_generator(prompt: str):
    """
    A simple image generation bot that creates images from text descriptions
    """
    llm = LLM(model="dall-e-3")  # Default image generation model
    
    if prompt:
        yield Text(f"🎨 Creating: {prompt}")
        
        # Generate image from the text prompt
        image_url = await llm.agenerate_image(prompt)
        yield Image(image_url)
        yield Text("✨ Your image is ready!")
    else:
        yield Markdown("""
## 🎨 AI Image Generator

I can create images from your text prompts!

Try prompts like:
- *"A futuristic cityscape at sunset"*
- *"A cute robot playing guitar in a forest"*
- *"An ancient map with fantasy landmarks"*

👉 Just type your description and I'll generate an image for you!
        """)


@bt.chatbot
async def artistic_bot(prompt: str):
    """
    An artistic image generator with style suggestions
    """
    llm = LLM(model="dall-e-3", quality="hd", style="vivid")
    
    if not prompt:
        yield Markdown("""
## 🎭 Artistic Image Creator

I create vivid, artistic images! Try these styles:

**Artistic Styles:**
- *"Oil painting of..."*
- *"Watercolor sketch of..."*
- *"Digital art featuring..."*
- *"Abstract representation of..."*

**Creative Prompts:**
- *"Surreal dreamscape with floating islands"*
- *"Cyberpunk street market at night"*
- *"Fantasy forest with bioluminescent plants"*

What artistic vision shall I bring to life?
        """)
        return
    
    yield Text("🎨 Creating your artistic vision...")
    
    # Add artistic flair to the prompt
    enhanced_prompt = f"Artistic, vivid style: {prompt}"
    
    image_url = await llm.agenerate_image(enhanced_prompt)
    yield Image(image_url)
    yield Markdown(f"**Created:** *{prompt}*")


@bt.chatbot
async def logo_designer(prompt: str):
    """
    A bot specialized in logo and icon design
    """
    llm = LLM(model="dall-e-3", quality="standard")
    
    if not prompt:
        yield Markdown("""
## 💼 Logo & Icon Designer

I design professional logos and icons!

**Logo Types:**
- *"Minimalist logo for tech startup"*
- *"Vintage badge for coffee shop"*
- *"Modern icon for mobile app"*
- *"Abstract symbol for consulting firm"*

**Design Tips:**
- Include company name and industry
- Specify style (modern, classic, playful)
- Mention preferred colors
- Describe any symbols or concepts

What logo should I design for you?
        """)
        return
    
    yield Text("🎨 Designing your logo...")
    
    # Enhance prompt for logo design
    logo_prompt = f"Professional logo design: {prompt}. Clean, scalable, suitable for business use"
    
    image_url = await llm.agenerate_image(logo_prompt)
    yield Image(image_url)
    yield Text("💡 Tip: For best results, use this as inspiration for a professional designer!")


@bt.chatbot
async def scene_creator(prompt: str):
    """
    Creates detailed scenes and environments
    """
    llm = LLM(model="dall-e-3", quality="hd", n=1)
    
    if not prompt:
        yield Markdown("""
## 🌍 Scene & Environment Creator

I create immersive scenes and environments!

**Scene Ideas:**
- *"Cozy reading nook by a rainy window"*
- *"Alien marketplace on distant planet"*
- *"Medieval castle during sunrise"*
- *"Underwater city with coral architecture"*

**Details to Include:**
- Time of day and lighting
- Weather and atmosphere
- Architectural style
- Flora and fauna

Describe the scene you want to explore!
        """)
        return
    
    yield Text("🏗️ Building your scene...")
    
    # Add scene details to prompt
    scene_prompt = f"Detailed scene: {prompt}. Rich atmosphere, immersive environment"
    
    image_url = await llm.agenerate_image(scene_prompt)
    yield Image(image_url)
    yield Markdown(f"**Scene:** *{prompt}*\n\n🌟 Explore every detail of your creation!")


@bt.chatbot
async def character_designer(prompt: str):
    """
    Designs characters for games, stories, or concepts
    """
    llm = LLM(model="dall-e-3", quality="hd")
    
    if not prompt:
        yield Markdown("""
## 👤 Character Designer

I design unique characters for your creative projects!

**Character Types:**
- *"Steampunk inventor with goggles"*
- *"Magical forest guardian"*
- *"Cyberpunk hacker with neon tattoos"*
- *"Ancient warrior with enchanted armor"*

**Helpful Details:**
- Species/race
- Age and personality
- Clothing and accessories
- Special abilities or tools

Who shall I bring to life today?
        """)
        return
    
    yield Text("✏️ Designing your character...")
    
    # Enhance for character design
    character_prompt = f"Character design: {prompt}. Full body or portrait, detailed features, unique personality"
    
    image_url = await llm.agenerate_image(character_prompt)
    yield Image(image_url)
    yield Text("🎭 Your character is ready for their adventure!")


# Run the server with multiple bots
if __name__ == "__main__":
    print("🎨 Image Generation Bots Ready!")
    print("Available at: http://localhost:8000/chat")
    print("\nBots available:")
    print("- Image Generator (default)")
    print("- Artistic Bot")
    print("- Logo Designer")
    print("- Scene Creator")
    print("- Character Designer")
    
    # Run the default image generator
    bt.run_server(image_generator)