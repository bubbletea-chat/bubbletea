# Root Dockerfile for all bots
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Install system dependencies needed for compilation
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

ARG BOT_DIR
WORKDIR /app

# Copy that bot’s code into the image
COPY ${BOT_DIR}/ /app/

# Install dependencies
RUN python -m pip install --upgrade pip && \
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

EXPOSE 8080
CMD ["python", "bot.py"]
