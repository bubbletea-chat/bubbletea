# BubbleTea Components Showcase Bot

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Development](#development)
- [Components Showcased](#components-showcased)

## Description
An interactive demonstration bot that showcases all available UI components in the BubbleTea Chat platform. This bot serves as a live reference for developers to understand and test various UI components including Text, Markdown, Cards, Pills, Images, Videos, and more.

## Features
- Live demonstration of all BubbleTea UI components
- Interactive examples showing component usage
- Developer-friendly reference implementation
- Visual showcase of formatting options
- Component behavior demonstrations

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd bt_components_showcase_bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Add your API keys to `.env`
6. Run the bot: `python bot.py`

## Configuration
### Components Demonstrated
- **Text**: Basic text messages with formatting
- **Markdown**: Rich text with headers, lists, and code blocks
- **Pills**: Interactive button choices
- **Cards**: Structured content display
- **Images**: Image rendering and display
- **Videos**: Video content embedding
- **Audio**: Audio file playback
- **Links**: Clickable hyperlinks
- **Tables**: Data in tabular format
- **Code Blocks**: Syntax-highlighted code

### Environment Variables
Create a `.env` file with:
```bash
BUBBLETEA_API_KEY=your_bubbletea_api_key
```

## Commands
- `/start` - Begin the component showcase
- `/text` - Text component examples
- `/markdown` - Markdown formatting examples
- `/cards` - Card component demonstrations
- `/pills` - Interactive pill buttons
- `/media` - Image, video, and audio examples
- `/all` - Show all components

## Use Cases
- Component reference for developers
- UI/UX testing and validation
- Learning BubbleTea platform capabilities
- Prototyping bot interfaces
- Component behavior verification

## Technical Details
- **Framework**: BubbleTea Chat SDK
- **Components**: Full UI component library
- **Architecture**: Single-file demonstration bot
- **State Management**: Session-based navigation

## Deployment Options
- **Local**: Run directly with Python
- **Replit**: Fork and run on Replit
- **Docker**: Container deployment supported
- **Cloud**: Deploy to any Python-supporting platform


## Support
For questions about components or the BubbleTea platform:
- **Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)