from typing import Dict, Any, Optional, List
import bubbletea_chat as bt
from core.user_preferences import UserPreferences
from services.weather_service import WeatherService
from services.news_service import NewsService
from storage.storage_adapter import StorageAdapter


class OnboardingManager:
    """Manages user onboarding flow and preference collection"""

    def __init__(self, conversation_uuid: str):
        """Initialize onboarding manager

        Args:
            conversation_uuid: Unique identifier for the user conversation
        """
        self.conversation_uuid = conversation_uuid
        self.user_prefs = UserPreferences(conversation_uuid)
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.storage = StorageAdapter()

    def is_user_onboarded(self) -> bool:
        """
        Check if user has completed onboarding

        Returns:
            True if user has completed onboarding, False otherwise
        """
        # Check if essential preferences are set
        location = self.user_prefs.get_weather_location()
        timezone = self.user_prefs.get_timezone()

        # User is considered onboarded if they have set their location
        # (timezone has a default value)
        return location is not None

    def start_onboarding(self):
        """
        Start the onboarding flow

        Returns:
            BubbleTea component for onboarding introduction
        """
        return bt.Markdown(
            """# Welcome to Morning Brief Bot! 🌅

I'm here to help you start each day with personalized morning briefs containing:

✅ **Weather updates** for your location
✅ **News headlines** tailored to your interests
✅ **Personalized insights** to kickstart your day

Let's get you set up with a quick configuration process."""
        )

    def get_location_setup(self):
        """
        Get location setup component

        Returns:
            BubbleTea component for location input
        """
        return bt.Text(
            "What's your location? (e.g., 'New York, NY' or 'London, UK')",
            placeholder="Enter your city and country/state...",
            multiline=False,
        )

    def process_location(self, location: str):
        """
        Process user's location input

        Args:
            location: User's location string

        Returns:
            BubbleTea component with confirmation or error
        """
        if not location or len(location.strip()) < 2:
            return bt.Markdown("❌ Please provide a valid location.")

        # Store the location
        success = self.user_prefs.set_weather_location(location.strip())

        if success:
            return bt.Markdown(f"✅ Great! I've set your location to **{location}**.")
        else:
            return bt.Markdown("❌ There was an issue saving your location. Please try again.")

    def get_timezone_setup(self):
        """
        Get timezone setup component

        Returns:
            BubbleTea component for timezone selection
        """
        common_timezones = [
            "UTC",
            "America/New_York",
            "America/Los_Angeles",
            "America/Chicago",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Shanghai",
            "Australia/Sydney",
        ]

        return bt.Pills("What's your timezone?", options=common_timezones, allow_multiple=False)

    def process_timezone(self, timezone: str):
        """
        Process user's timezone selection

        Args:
            timezone: Selected timezone string

        Returns:
            BubbleTea component with confirmation
        """
        success = self.user_prefs.set_timezone(timezone)

        if success:
            return bt.Markdown(f"✅ Timezone set to **{timezone}**.")
        else:
            return bt.Markdown("❌ There was an issue saving your timezone. Please try again.")

    def get_news_preferences_setup(self):
        """
        Get news preferences setup component

        Returns:
            BubbleTea component for news category selection
        """
        news_categories = ["general", "technology", "business", "science", "health", "sports", "entertainment"]

        return bt.Pills(
            "Which news categories interest you? (Select multiple)", options=news_categories, allow_multiple=True
        )

    def process_news_preferences(self, categories: List[str]):
        """
        Process user's news category preferences

        Args:
            categories: List of selected news categories

        Returns:
            BubbleTea component with confirmation
        """
        if not categories:
            categories = ["general", "technology"]  # Default categories

        success = self.user_prefs.set_news_categories(categories)

        if success:
            category_list = ", ".join(categories)
            return bt.Markdown(f"✅ News categories set to: **{category_list}**.")
        else:
            return bt.Markdown("❌ There was an issue saving your news preferences.")

    def get_schedule_setup(self):
        """
        Get schedule setup component

        Returns:
            BubbleTea component for schedule preferences
        """
        time_options = ["06:00", "06:30", "07:00", "07:30", "08:00", "08:30", "09:00", "09:30", "10:00"]

        return bt.Pills(
            "What time would you like to receive your morning brief?", options=time_options, allow_multiple=False
        )

    def process_schedule(self, brief_time: str):
        """
        Process user's schedule preference

        Args:
            brief_time: Selected time string

        Returns:
            BubbleTea component with confirmation
        """
        success = self.user_prefs.set_brief_time(brief_time)

        if success:
            return bt.Markdown(f"✅ Morning brief scheduled for **{brief_time}** daily.")
        else:
            return bt.Markdown("❌ There was an issue saving your schedule preference.")

    def get_brief_sections_setup(self):
        """
        Get brief sections setup component

        Returns:
            BubbleTea component for section selection
        """
        section_options = ["weather", "news", "calendar", "motivational_quote"]

        return bt.Pills(
            "Which sections would you like in your morning brief?", options=section_options, allow_multiple=True
        )

    def process_brief_sections(self, sections: List[str]):
        """
        Process user's brief section preferences

        Args:
            sections: List of selected sections

        Returns:
            BubbleTea component with confirmation
        """
        if not sections:
            sections = ["weather", "news"]  # Default sections

        # Convert list to dict format expected by user preferences
        sections_dict = {section: True for section in sections}
        # Explicitly set unselected sections to False
        all_sections = ["weather", "news", "calendar", "motivational_quote"]
        for section in all_sections:
            if section not in sections:
                sections_dict[section] = False

        success = self.user_prefs.set_brief_sections(sections_dict)

        if success:
            section_list = ", ".join(sections)
            return bt.Markdown(f"✅ Brief sections set to: **{section_list}**.")
        else:
            return bt.Markdown("❌ There was an issue saving your section preferences.")

    def complete_onboarding(self):
        """
        Complete the onboarding process

        Returns:
            BubbleTea component with completion message
        """
        # Enable notifications by default
        self.user_prefs.set_notifications_enabled(True)

        # Get user's preferences for summary
        location = self.user_prefs.get_weather_location()
        timezone = self.user_prefs.get_timezone()
        categories = self.user_prefs.get_news_categories()
        brief_time = self.user_prefs.get_brief_time().strftime("%H:%M")

        return bt.Markdown(
            f"""# 🎉 Setup Complete!

Your Morning Brief Bot is now configured with:

📍 **Location:** {location}
🕐 **Timezone:** {timezone}
📰 **News Categories:** {', '.join(categories)}
⏰ **Brief Time:** {brief_time}

You'll start receiving personalized morning briefs according to your preferences. You can always update your settings by typing "settings" or "preferences".

Type "brief" to get your first morning brief right now, or "help" to see all available commands!"""
        )

    def get_onboarding_status(self) -> Dict[str, Any]:
        """
        Get current onboarding status and progress

        Returns:
            Dictionary containing onboarding progress information
        """
        preferences = self.user_prefs.get_all_preferences()

        status = {
            "is_complete": self.is_user_onboarded(),
            "completed_steps": [],
            "remaining_steps": [],
            "preferences": preferences,
        }

        # Define onboarding steps
        steps = {
            "location": preferences.get("weather_location") is not None,
            "timezone": preferences.get("timezone") != "UTC",
            "news_categories": len(preferences.get("news_categories", [])) > 0,
            "brief_time": preferences.get("brief_time") != "08:00",
            "brief_sections": any(preferences.get("brief_sections", {}).values()),
        }

        for step, completed in steps.items():
            if completed:
                status["completed_steps"].append(step)
            else:
                status["remaining_steps"].append(step)

        return status

    def reset_onboarding(self) -> bool:
        """
        Reset onboarding progress (for testing or re-setup)

        Returns:
            True if reset successfully, False otherwise
        """
        return self.user_prefs.reset_preferences()

    def update_preference_during_onboarding(self, preference_key: str, value: Any):
        """
        Update a specific preference during onboarding

        Args:
            preference_key: The preference to update
            value: The new value

        Returns:
            BubbleTea component with update confirmation
        """
        success = False

        # Route to appropriate setter method
        setter_methods = {
            "location": self.user_prefs.set_weather_location,
            "timezone": self.user_prefs.set_timezone,
            "news_categories": self.user_prefs.set_news_categories,
            "brief_time": self.user_prefs.set_brief_time,
            "brief_sections": self.user_prefs.set_brief_sections,
        }

        if preference_key in setter_methods:
            success = setter_methods[preference_key](value)

        if success:
            return bt.Markdown(f"✅ Updated {preference_key} successfully.")
        else:
            return bt.Markdown(f"❌ Failed to update {preference_key}. Please try again.")
