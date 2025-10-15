# Deploying a Bot

## Table of Contents
- [Ngrok - Local Development Made Easy](#ngrok---local-development-made-easy)
- [Cloud Run - Production Deployment with CI/CD](#cloud-run---production-deployment-with-cicd)
- [CORS Support - Cross-Origin Configuration](#cors-support---cross-origin-configuration)
- [Testing Your Bot](#testing-your-bot)

## Ngrok - Local Development Made Easy

Ngrok is the fastest way to test your bot during development. It creates a secure tunnel from the internet to your local machine, giving you a public URL instantly. Perfect for testing and debugging before deploying to production:

```bash
# Step 1: Install ngrok
brew install ngrok  # macOS
# or download from https://ngrok.com

# Step 2: Start your bot
python your_bot.py

# Step 3: Expose to internet
ngrok http 8000

# Your bot is now accessible at:
# https://abc123.ngrok.io
```

## Cloud Run - Production Deployment with CI/CD

Bots are automatically deployed to Google Cloud Run using GitHub Actions for continuous deployment. When you push changes to the main branch, your bots are built, containerized, and deployed automatically. This provides production-grade hosting with serverless scaling, SSL certificates, and zero DevOps overhead:

### Automatic Deployment Setup

The repository includes GitHub Actions workflows that handle deployment automatically:

**Deployment Process:**
1. Add your bot to the `bots/` folder with `bot.py` and `requirements.txt`
2. Push changes to the main branch
3. GitHub Actions detects changes in `bots/**` directory
4. Automatically builds Docker image using `bots/Dockerfile`
5. Pushes image to Google Artifact Registry
6. Deploys to Cloud Run with all required secrets
7. Sends Slack notification on successful deployment

**Deployment Files:**
- `.github/workflows/deploy-bots.yml` - GitHub Actions workflow for deployment
- `.github/scripts/deploy-and-notify.sh` - Deployment and notification script
- `bots/Dockerfile` - Docker configuration for containerizing bots

### Bot Structure

Each bot in the `bots/` folder should have:
```bash
bots/
  your-bot-name/
    bot.py              # Main bot code
    requirements.txt    # Python dependencies
    config.py          # Optional configuration
    README.md          # Bot documentation
```

### Deployment Features

Cloud Run deployment provides:
- **Automatic Scaling**: Scales from 0 to thousands of instances
- **SSL Certificates**: Automatic HTTPS for all bots
- **Environment Secrets**: All GCP secrets automatically injected
- **Zero Downtime**: Rolling updates with health checks
- **Custom Domains**: Support for custom domain mapping
- **Cost Efficient**: Pay only for actual usage

### Manual Deployment

To manually trigger deployment:
```bash
# Via GitHub Actions UI
# 1. Go to Actions tab in GitHub
# 2. Select "Deploy Bots to Cloud Run"
# 3. Click "Run workflow"
# 4. Select branch and run

# The workflow will:
# - Detect all bots in bots/ folder
# - Build and deploy changed bots
# - Output deployment URLs
```

### Monitoring Deployments

Check deployment status:
- GitHub Actions tab shows build and deployment logs
- Slack notifications (if configured) report deployment success/failure
- Cloud Run console shows service status and logs
- Each bot gets a unique URL: `https://bot-name-[hash].run.app`

## CORS Support - Cross-Origin Configuration

CORS (Cross-Origin Resource Sharing) allows Bubbletea's frontend to communicate with your bot's backend. The SDK handles this automatically, but if you're building a custom implementation, you'll need to configure CORS headers properly:

```python
# FastAPI example
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Your Bot

Before registering with Bubbletea, test your bot locally to ensure it's working correctly. Use these curl commands to verify your endpoints are responding properly. Each test simulates what Bubbletea will send to your bot:

```bash
# Test your bot endpoint
curl -X POST https://your-bot.com/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "message": "Hello"}'

# Test config endpoint
curl https://your-bot.com/config

# Test with images
curl -X POST https://your-bot.com/chat \
  -H "Content-Type: application/json" \
  -d '{"type": "user", "message": "What is this?",
       "images": [{"url": "https://example.com/img.jpg"}]}'
```