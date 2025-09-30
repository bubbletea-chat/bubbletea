# Movie Guessing Game Bot

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Development](#development)
- [How to Play](#how-to-play)

## Description
An interactive movie guessing game bot built for the BubbleTea Chat platform. Challenge your movie knowledge with AI-generated questions featuring hilariously bad movie plot descriptions!

## Features

- **Interactive Quiz Flow**: Multi-stage game with era, difficulty, and genre selection
- **AI-Generated Questions**: Uses OpenAI GPT-4 to create unique movie quiz questions
- **Bad Plot Descriptions**: Deliberately vague and humorous movie summaries for extra challenge
- **Rich UI Components**: Interactive pills for seamless user experience
- **Score Tracking**: Keep track of your performance across multiple games
- **Session Management**: Maintains game state per user conversation

### How It Works

1. **Start the Game**: Type 'start' to begin
2. **Choose Era**: Select from All, Classics, 2000s, 2010s, or Recent
3. **Pick Difficulty**: Choose All, Easy, Medium, or Hard
4. **Select Genre**: Pick from Action, Comedy, Drama, Sci-Fi, Horror, Romance, or All
5. **Play Quiz**: Answer 5 multiple-choice questions based on badly described movie plots
6. **View Results**: See your final score and play again!

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd movie-game-bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Add your OpenAI API key to `.env`
6. Run the bot: `python bot.py`

## Configuration
### Bot Settings
- **Name**: `movie-guessing-game`
- **Display Name**: `Movie Guessing Game`
- **Port**: `5000` (configurable)
- **Streaming**: Disabled for structured responses

### Environment Variables
Create a `.env` file with:
```bash
OPENAI_API_KEY=your_openai_api_key
BUBBLETEA_API_KEY=your_bubbletea_api_key
```

## Commands
- Send `start` to begin a new game
- Answer questions by selecting from multiple choice options
- View your score at the end of each game

## Use Cases
- **Entertainment**: Fun movie trivia game
- **Education**: Learn about movies through gameplay
- **Social**: Challenge friends with movie knowledge
- **Demo**: Showcase interactive bot capabilities

## Technical Details
### OpenAI Integration
The bot uses GPT-4 to generate movie quiz questions with:
- Badly written movie descriptions (humorous, vague, or misleading)
- Four multiple choice options per question
- Difficulty and genre-appropriate content
- JSON-structured responses for consistent parsing

### Game Flow
- Session-based state management
- Dynamic question generation
- Score tracking across games
- Rich UI with interactive pills

## Deployment Options
- **Local**: Run directly with Python
- **Replit**: Fork and deploy on Replit
- **Docker**: Container deployment supported
- **Cloud**: Deploy to any Python-supporting platform

## Support

- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)

---

**Made with ❤️ by BubbleTea Chat**

*Ready to test your movie knowledge? Start guessing! 🎬*