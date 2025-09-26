from typing import Optional
from openai import OpenAI
from config import OPENAI_API_KEY


class WeatherService:
    """Service for generating weather summaries using OpenAI with web search capability"""

    SYSTEM_PROMPT = """Get today's current weather summary for {location}.

Include:
- Current temperature and conditions
- Today's forecast
- One practical tip for the weather
- Use emojis and be concise (2-3 sentences)

Provide only the weather summary, no additional commentary."""

    def __init__(self, search_context_size: str = "medium"):
        """Initialize the weather service with OpenAI client and web search capability"""
        self.search_context_size = search_context_size  # "low", "medium", "high"
        self.openai_client = self._create_openai_client()

    def _create_openai_client(self) -> Optional[OpenAI]:
        """Create OpenAI client if API key is available"""
        if OPENAI_API_KEY:
            return OpenAI(api_key=OPENAI_API_KEY)
        return None

    def get_weather_summary(self, location: str) -> str:
        """
        Get weather summary for a location using web search

        Args:
            location: The location to get weather for

        Returns:
            Weather summary string
        """
        if not self.openai_client:
            return self._get_api_key_error_message()

        try:
            return self._generate_weather_summary_with_web_search(location)
        except Exception as e:
            return self._get_error_message(location, e)

    def _generate_weather_summary_with_web_search(self, location: str) -> str:
        """Generate weather summary using OpenAI's web search capability"""
        # Use the new Responses API with web search
        response = self.openai_client.responses.create(
            model="gpt-4.1",  # Use gpt-4.1 for web search capability
            tools=[
                {
                    "type": "web_search_preview",
                    "search_context_size": self.search_context_size,
                }
            ],
            input=self.SYSTEM_PROMPT.format(location=location),
        )

        return response.output_text

    def _get_api_key_error_message(self) -> str:
        """Get error message for missing API key"""
        return "Weather unavailable. Set OPENAI_API_KEY."

    def _get_error_message(self, location: str, error: Exception) -> str:
        """Get error message for weather generation failure"""
        return f"Weather unavailable for {location}."

    # Maintain backward compatibility
    def get_weather_summary_openai(self, location: str) -> str:
        """Legacy method name for backward compatibility"""
        return self.get_weather_summary(location)
