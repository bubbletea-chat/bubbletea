# ChatGPT Thread Bot

## What you'll get

### Description
A sophisticated AI chatbot powered by OpenAI's GPT at provides intelligent conversation with threaded messaging support. Perfect for customer support, brainstorming sessions, and interactive AI assistance with conversation history management.

### Live bot
🔗 **Try it now:** [ChatGPT Thread Bot on BubbleTea](https://bubbletea.chat/bot/chatgpt-wrapper)

### Example conversations
- [View sample conversation 1](https://bubbletea.chat/shared/wrhjUAYmHryp3XFZFauSYyCjypq4n8v3egC9RmvxtD8)
- [View sample conversation 2](https://bubbletea.chat/shared/wrhjUAYmHryp3XFZFauSYyCjypq4n8v3egC9RmvxtD8)

### Features
- **Natural Language Conversations** - Powered by GPT-4 for intelligent responses
- **Threaded Messaging** - Maintains conversation context across multiple messages
- **Async Processing** - Non-blocking message handling for better performance
- **Context Retention** - Remembers previous messages within a thread
- **Multi-turn Dialog** - Ideal for extended conversations and problem-solving
- **Timeout Protection** - 120-second timeout for long-running requests
- **Rich Markdown Support** - Formatted responses with markdown rendering
- **Session Management** - Per-user conversation threads for personalized experiences

## How to build it

### Code review

1. **Main Components:**
   - `process_message_async()` - Handles async message processing with the OpenAI API
   - `gpt_assistant()` - Main chatbot handler decorated with @bt.chatbot
   - `get_config()` - Bot configuration including metadata and display settings

2. **Key Technologies:**
   - BubbleTea Chat SDK for bot framework
   - OpenAI API for GPT-4 integration
   - Async/await for non-blocking operations
   - Thread management for conversation continuity
   - httpx for async HTTP requests

3. **Architecture Flow:**
   - User sends message → Bot receives via webhook
   - Creates/retrieves thread ID for conversation context
   - Async task processes message with OpenAI API
   - Response formatted as Markdown component
   - Sent back to BubbleTea platform via API

4. **Environment Variables:**
   ```
   BUBBLETEA_API_KEY=your_bubbletea_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

### Deployment

1. **Prerequisites:**
   - Python 3.8+
   - Google Cloud Platform account
   - BubbleTea API key
   - OpenAI API key

2. **Installation:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Local Testing:**
   ```bash
   # Set environment variables
   export OPENAI_API_KEY="your_key"
   export BUBBLETEA_API_KEY="your_key"

   # Run the bot
   python bot.py
   ```

4. **Deploy to Google Cloud Run:**

   Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["python", "bot.py"]
   ```

   Deploy:
   ```bash
   # Build container
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/openai-bot

   # Deploy to Cloud Run
   gcloud run deploy openai-bot \
     --image gcr.io/YOUR_PROJECT/openai-bot \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --port 8080 \
     --set-env-vars BUBBLETEA_API_KEY=$BUBBLETEA_API_KEY,OPENAI_API_KEY=$OPENAI_API_KEY
   ```

5. **Configuration:**
   - Set environment variables in Cloud Run
   - Update bot URL in BubbleTea dashboard with Cloud Run URL
   - Configure CORS if needed

## Deployed

✅ **Status:** Successfully deployed on Google Cloud Run

🌐 **Platform:** Google Cloud Platform (GCP)

📍 **Region:** Configurable (default: us-central1)

🔗 **Live URL:** Available on [BubbleTea Chat](https://bubbletea.chat/bot/chatgpt-wrapper)

🚀 **Port:** 8080 (Cloud Run default)

## Support
For BubbleTea SDK documentation: [docs.bubbletea.chat](https://bubbletea.chat/docs)
For platform issues: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)