# Morning Brief Bot

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Configuration](#configuration)
- [Commands](#commands)
- [Data Persistence](#data-persistence)
- [Development](#development)
- [Example Output](#example-output)

## Description
An intelligent morning briefing bot built for the BubbleTea Chat platform. Get personalized daily weather and news summaries delivered at your preferred wake-up time!

## Features

- **Personalized Morning Briefs**: Customized weather and news based on your location and interests
- **Scheduled Delivery**: Automatic delivery at your preferred wake-up time
- **Interactive Onboarding**: Easy setup process with location, interests, and time preferences
- **Real-time Weather**: Current weather conditions and forecasts using OpenAI's web search
- **Curated News**: Relevant news headlines filtered by your selected topics
- **Persistent Storage**: User preferences stored in Firebase Firestore database
- **Rich UI Components**: Interactive pills and formatted messages
- **Flexible Commands**: Multiple ways to interact with the bot

### How It Works

#### Onboarding Flow
1. **Location Setup**: Enter your city and country (e.g., "London, UK")
2. **Interest Selection**: Choose from 9 news categories (Technology, Business, Sports, etc.)
3. **Wake Time**: Set your preferred morning brief delivery time (24-hour format)
4. **Completion**: Receive confirmation and quick action options

#### Daily Briefings
- Automatically generated and delivered at your specified wake-up time
- Includes weather forecast with practical tips
- Contains 3-4 relevant news headlines with descriptions
- Formatted with emojis and easy-to-read structure

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd morning-bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Add your API keys to `.env`
6. Run the bot: `python bot.py`

## Configuration
### Environment Variables
Create a `.env` file with the following variables:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here
BUBBLETEA_API_KEY=your_bubbletea_api_key_here

# Firebase (for persistent storage)
FIREBASE_PROJECT_ID=your_firebase_project_id
FIREBASE_PRIVATE_KEY=your_firebase_private_key
FIREBASE_CLIENT_EMAIL=your_firebase_client_email
```

### Prerequisites
- Python 3.8+
- BubbleTea Chat SDK
- OpenAI API access
- Firebase Firestore database (optional, for persistent storage)

## Commands

| Command | Description |
|---------|-------------|
| `start` or `hi` | Begin setup or restart onboarding |
| `help` | Show available commands |
| `update` | Change your preferences |
| `preview` | Generate a sample morning brief |
| `morning` or `brief` | Get today's morning brief |
| `generate` | Manually trigger a brief generation |
| `status` | View your current settings |


## Use Cases
- **Personal Morning Briefs**: Daily weather and news summaries
- **Location-Based Updates**: Weather and news for your specific area
- **Interest-Based News**: Customized news based on selected topics
- **Scheduled Delivery**: Automatic briefs at your wake-up time
- **On-Demand Briefs**: Generate morning briefs anytime

## Technical Details

### Architecture

**MorningBriefBot**: Main orchestrator handling user interactions and routing commands

**OnboardingManager**: Guides users through the setup process with state management

**UserPreferencesManager**: Manages user data persistence and state transitions

**WeatherService**: Fetches weather data using OpenAI's web search capabilities

**NewsService**: Retrieves relevant news headlines based on user interests

**MorningBriefScheduler**: Background service that generates and delivers daily briefs

**NotificationService**: Handles communication with the BubbleTea API

**StorageAdapter**: Provides abstraction for data persistence (Firebase Firestore implementation)


### AI Integration

The bot leverages **OpenAI GPT-4** with web search capabilities to provide:

### Weather Summaries
- Real-time weather data for any location
- Current conditions and daily forecasts
- Practical weather tips and recommendations
- Concise, emoji-rich formatting

### News Headlines
- Latest breaking news and developments
- Local and regional relevance
- Category-specific filtering (Technology, Business, Sports, etc.)
- Brief, digestible descriptions

### Testing

### Manual Testing
```bash
# Test the complete flow
python bot.py
```

### Test Commands
1. Send `start` - Test onboarding flow
2. Complete setup with valid location, interests, and time
3. Send `preview` - Test brief generation
4. Send `generate` - Test manual triggering
5. Send `status` - Verify preferences saved correctly

### Integration Testing
- Verify OpenAI API connectivity
- Test Firebase Firestore database operations
- Confirm BubbleTea API notifications
- Validate scheduler timing accuracy

## Deployment Options
- **Local**: Run directly with Python
- **Docker**: Container deployment supported
- **Cloud**: Deploy to any Python-supporting platform
- **Serverless**: AWS Lambda, Google Cloud Functions

### Contributing

We welcome contributions to improve the Morning Brief Bot!

### 🚀 Quick Start for Contributors

1. **Fork and Setup**:
```bash
git fork https://github.com/bubbletea-chat/bots-public
cd bots-public
cd openai-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Setup**:
```bash
cp .env.example .env
# Configure with your API keys
```

3. **Create Feature Branch**:
```bash
git checkout -b feature/your-enhancement
```

### 📝 Contribution Guidelines

#### What to Work On
- **New Features**: Additional news categories, weather alerts, reminder systems
- **UI/UX**: Better onboarding flow, more interactive components
- **Performance**: Caching, rate limiting, error resilience
- **Storage**: Alternative storage backends, data export/import
- **AI Enhancements**: Better summarization, sentiment analysis, trending topics

#### Code Standards
- Follow PEP 8 style guidelines
- Add docstrings to all functions and classes
- Use type hints for better code clarity
- Handle exceptions gracefully
- Write descriptive commit messages

#### Testing Your Changes
- Test the complete onboarding flow
- Verify all commands work correctly
- Check error handling for invalid inputs
- Ensure backward compatibility with existing users

### 🎯 Feature Ideas

**Beginner-Friendly**:
- Add more news categories (Local, Health, Science)
- Implement timezone support
- Create user settings export/import
- Add weather alerts for extreme conditions

**Intermediate**:
- Multi-language support for international users
- Voice message support for morning briefs
- Integration with calendar apps for event awareness
- Smart brief timing based on user activity

**Advanced**:
- Machine learning for personalized content ranking
- Real-time brief updates throughout the day
- Integration with smart home devices
- Analytics dashboard for usage patterns

### 📋 Pull Request Process

1. **Before Submitting**:
   - Ensure all tests pass
   - Update documentation for new features
   - Add configuration examples if needed
   - Test with different user scenarios

2. **PR Description**:
   - Clearly describe the problem solved
   - Include screenshots for UI changes
   - List any breaking changes
   - Mention related issues

3. **Review Process**:
   - Code review by maintainers
   - Automated testing validation
   - Documentation review
   - Manual testing in development environment

## Support

Need help or found a bug?

- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)

---

**Stay informed, start your day right! ☀️**

*Built with ❤️ for BubbleTea Chat*