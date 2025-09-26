from typing import Dict, Any, Optional, List
from datetime import datetime, time
import json
from storage.storage_adapter import StorageAdapter


class UserPreferences:
    """Manages user preferences and settings for personalized morning briefs"""

    def __init__(self, conversation_uuid: str):
        """Initialize user preferences manager

        Args:
            conversation_uuid: Unique identifier for the user conversation
        """
        self.conversation_uuid = conversation_uuid
        self.storage = StorageAdapter()
        self._cache = {}

    def set_timezone(self, timezone: str) -> bool:
        """
        Set user's timezone preference

        Args:
            timezone: Timezone string (e.g., 'America/New_York', 'UTC')

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "timezone", timezone)
        if success:
            self._cache["timezone"] = timezone
        return success

    def get_timezone(self) -> str:
        """
        Get user's timezone preference

        Returns:
            Timezone string, defaults to 'UTC' if not set
        """
        if "timezone" in self._cache:
            return self._cache["timezone"]

        timezone = self.storage.get_user_preference(self.conversation_uuid, "timezone", "UTC")
        self._cache["timezone"] = timezone
        return timezone

    def set_weather_location(self, location: str) -> bool:
        """
        Set user's preferred weather location

        Args:
            location: Location string (e.g., 'New York, NY', 'London, UK')

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "weather_location", location)
        if success:
            self._cache["weather_location"] = location
        return success

    def get_weather_location(self) -> Optional[str]:
        """
        Get user's preferred weather location

        Returns:
            Location string or None if not set
        """
        if "weather_location" in self._cache:
            return self._cache["weather_location"]

        location = self.storage.get_user_preference(self.conversation_uuid, "weather_location", None)
        if location:
            self._cache["weather_location"] = location
        return location

    def set_news_categories(self, categories: List[str]) -> bool:
        """
        Set user's preferred news categories

        Args:
            categories: List of news categories (e.g., ['technology', 'business'])

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "news_categories", json.dumps(categories))
        if success:
            self._cache["news_categories"] = categories
        return success

    def get_news_categories(self) -> List[str]:
        """
        Get user's preferred news categories

        Returns:
            List of news categories, defaults to general categories
        """
        if "news_categories" in self._cache:
            return self._cache["news_categories"]

        categories_json = self.storage.get_user_preference(
            self.conversation_uuid, "news_categories", json.dumps(["general", "technology", "business"])
        )

        try:
            categories = json.loads(categories_json) if isinstance(categories_json, str) else categories_json
        except (json.JSONDecodeError, TypeError):
            categories = ["general", "technology", "business"]

        self._cache["news_categories"] = categories
        return categories

    def set_brief_time(self, brief_time: str) -> bool:
        """
        Set user's preferred time for morning briefs

        Args:
            brief_time: Time string in HH:MM format (e.g., '08:00')

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "brief_time", brief_time)
        if success:
            self._cache["brief_time"] = brief_time
        return success

    def get_brief_time(self) -> time:
        """
        Get user's preferred time for morning briefs

        Returns:
            Time object, defaults to 8:00 AM if not set
        """
        if "brief_time" in self._cache:
            time_str = self._cache["brief_time"]
        else:
            time_str = self.storage.get_user_preference(self.conversation_uuid, "brief_time", "08:00")
            self._cache["brief_time"] = time_str

        try:
            hour, minute = map(int, time_str.split(":"))
            return time(hour, minute)
        except (ValueError, AttributeError):
            return time(8, 0)  # Default to 8:00 AM

    def set_notifications_enabled(self, enabled: bool) -> bool:
        """
        Enable or disable morning brief notifications

        Args:
            enabled: Whether notifications should be enabled

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "notifications_enabled", str(enabled))
        if success:
            self._cache["notifications_enabled"] = enabled
        return success

    def get_notifications_enabled(self) -> bool:
        """
        Check if morning brief notifications are enabled

        Returns:
            True if enabled, defaults to True
        """
        if "notifications_enabled" in self._cache:
            return self._cache["notifications_enabled"]

        enabled_str = self.storage.get_user_preference(self.conversation_uuid, "notifications_enabled", "True")
        enabled = enabled_str.lower() in ("true", "1", "yes", "on")
        self._cache["notifications_enabled"] = enabled
        return enabled

    def set_brief_sections(self, sections: Dict[str, bool]) -> bool:
        """
        Set which sections to include in morning briefs

        Args:
            sections: Dict mapping section names to enabled status
                     (e.g., {'weather': True, 'news': True, 'calendar': False})

        Returns:
            True if set successfully, False otherwise
        """
        success = self.storage.store_user_preference(self.conversation_uuid, "brief_sections", json.dumps(sections))
        if success:
            self._cache["brief_sections"] = sections
        return success

    def get_brief_sections(self) -> Dict[str, bool]:
        """
        Get which sections to include in morning briefs

        Returns:
            Dict mapping section names to enabled status
        """
        if "brief_sections" in self._cache:
            return self._cache["brief_sections"]

        sections_json = self.storage.get_user_preference(
            self.conversation_uuid, "brief_sections", json.dumps({"weather": True, "news": True, "calendar": False})
        )

        try:
            sections = json.loads(sections_json) if isinstance(sections_json, str) else sections_json
        except (json.JSONDecodeError, TypeError):
            sections = {"weather": True, "news": True, "calendar": False}

        self._cache["brief_sections"] = sections
        return sections

    def get_all_preferences(self) -> Dict[str, Any]:
        """
        Get all user preferences as a dictionary

        Returns:
            Dictionary containing all user preferences
        """
        # Load all preferences into cache if not already loaded
        preference_keys = [
            "timezone",
            "weather_location",
            "news_categories",
            "brief_time",
            "notifications_enabled",
            "brief_sections",
        ]

        for key in preference_keys:
            if key not in self._cache:
                # Trigger getter to load and cache the preference
                getattr(self, f"get_{key}")()

        return self._cache.copy()

    def reset_preferences(self) -> bool:
        """
        Reset all user preferences to defaults

        Returns:
            True if reset successfully, False otherwise
        """
        try:
            # Clear cache
            self._cache.clear()

            # Delete stored preferences (they will fall back to defaults)
            success = self.storage.delete_user_data(self.conversation_uuid)
            return success
        except Exception as e:
            return False

    def update_preferences(self, preferences: Dict[str, Any]) -> Dict[str, bool]:
        """
        Update multiple preferences at once

        Args:
            preferences: Dictionary of preference key-value pairs

        Returns:
            Dictionary mapping preference keys to success status
        """
        results = {}

        for key, value in preferences.items():
            setter_method = f"set_{key}"
            if hasattr(self, setter_method):
                results[key] = getattr(self, setter_method)(value)
            else:
                # Direct storage for unknown preferences
                results[key] = self.storage.store_user_preference(self.conversation_uuid, key, value)
                if results[key]:
                    self._cache[key] = value

        return results
