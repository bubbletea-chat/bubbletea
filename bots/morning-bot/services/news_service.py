from typing import List, Optional
from openai import OpenAI
from config import OPENAI_API_KEY


class NewsService:
    """Service for generating news summaries using OpenAI with web search capability"""

    SYSTEM_PROMPT = """Generate 3-4 current news headlines with brief descriptions for {categories} in {location}.

Focus on:
- Latest developments and breaking news
- Local and regional relevance to {location}
- Topics: {categories}

Format: Use emojis and be very concise (1-line descriptions).
Provide only the news headlines and descriptions, no additional commentary."""

    def __init__(self, search_context_size: str = "medium"):
        """Initialize the news service with OpenAI client and web search capability"""
        self.search_context_size = search_context_size  # "low", "medium", "high"
        self.openai_client = self._create_openai_client()

    def _create_openai_client(self) -> Optional[OpenAI]:
        """Create OpenAI client if API key is available"""
        if OPENAI_API_KEY:
            return OpenAI(api_key=OPENAI_API_KEY)
        return None

    def get_news_summary(self, categories: List[str], location: str) -> str:
        """
        Get news summary for specified categories using web search

        Args:
            categories: List of news categories to include
            location: User's location for context

        Returns:
            News summary string
        """
        if not self.openai_client:
            return self._get_api_key_error_message()

        if not categories:
            return self._get_no_categories_message()

        try:
            return self._generate_news_summary_with_web_search(categories, location)
        except Exception as e:
            return self._get_error_message(categories, e)

    def _generate_news_summary_with_web_search(self, categories: List[str], location: str) -> str:
        """Generate news summary using OpenAI's web search capability"""
        categories_str = ", ".join(categories)

        # Use the new Responses API with web search
        response = self.openai_client.responses.create(
            model="gpt-4.1",  # Use gpt-4.1 for web search capability
            tools=[
                {
                    "type": "web_search_preview",
                    "search_context_size": self.search_context_size,
                }
            ],
            input=self.SYSTEM_PROMPT.format(categories=categories_str, location=location),
        )

        return response.output_text

    def _get_api_key_error_message(self) -> str:
        """Get error message for missing API key"""
        return "News unavailable. Set OPENAI_API_KEY."

    def _get_no_categories_message(self) -> str:
        """Get message when no categories are selected"""
        return "No news topics selected."

    def _get_error_message(self, categories: List[str], error: Exception) -> str:
        """Get error message for news generation failure"""
        return "News unavailable."

    # Maintain backward compatibility
    def get_news_summary_openai(self, categories: List[str], location: str) -> str:
        """Legacy method name for backward compatibility"""
        return self.get_news_summary(categories, location)
