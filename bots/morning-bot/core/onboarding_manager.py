import re
from typing import List, Optional
from core.user_preferences import UserPreferencesManager, OnboardingState
from bubbletea_chat.components import Pill, Pills, Text, Markdown


class OnboardingManager:
    def __init__(self, preferences_manager: UserPreferencesManager):
        self.preferences_manager = preferences_manager

        # Available news categories
        self.news_categories = [
            "technology", "business", "entertainment", "health",
            "science", "sports", "politics", "world", "finance"
        ]

    def get_onboarding_message(self, user_uuid: str, user_input: Optional[str] = None) -> list:
        """Main onboarding flow handler"""
        current_state = self.preferences_manager.get_current_onboarding_state(user_uuid)

        # Handle user input based on current state
        if user_input and current_state != OnboardingState.NOT_STARTED:
            return self._process_user_input(user_uuid, current_state, user_input)

        # Return appropriate message for current state
        return self._get_state_message(user_uuid, current_state)

    def _get_state_message(self, user_uuid: str, state: OnboardingState) -> list:
        """Get the appropriate message for the current onboarding state"""

        if state == OnboardingState.NOT_STARTED:
            self.preferences_manager.advance_onboarding_state(user_uuid)
            return [
                Markdown(
                    "🌅 **Morning Brief Bot**\n\n"
                    "Daily weather & news at your wake time.\n\n"
                    "**Your city, country?** (e.g., 'London, UK'):"
                )
            ]

        elif state == OnboardingState.ASKING_LOCATION:
            return [Text("City, country? (e.g., 'Paris, France')")]

        elif state == OnboardingState.ASKING_INTERESTS:
            return [
                Text("Pick news topics:"),
                Pills(pills=[Pill(cat.title(), f"interest:{cat}") for cat in self.news_categories]),
                Text("Click topics, then type 'done'")
            ]

        elif state == OnboardingState.ASKING_WAKE_TIME:
            return [
                Text("Wake time? (24-hour format like '07:00'):")
            ]

        elif state == OnboardingState.COMPLETED:
            user_prefs = self.preferences_manager.get_or_create_user(user_uuid)

            return [
                Markdown(
                    "✅ **Setup done!**\n"
                    f"📍 {user_prefs.location}\n"
                    f"📰 {', '.join(user_prefs.news_interests)}\n"
                    f"⏰ {user_prefs.wake_time}"
                ),
                Pills(pills=[
                    Pill("Update", "action:update"),
                    Pill("Preview", "action:preview"),
                    Pill("Help", "action:help")
                ])
            ]

    def _process_user_input(self, user_uuid: str, state: OnboardingState, user_input: str) -> list:
        """Process user input based on current state"""

        if state == OnboardingState.ASKING_LOCATION:
            return self._process_location(user_uuid, user_input)

        elif state == OnboardingState.ASKING_INTERESTS:
            return self._process_interests(user_uuid, user_input)

        elif state == OnboardingState.ASKING_WAKE_TIME:
            return self._process_wake_time(user_uuid, user_input)

        elif state == OnboardingState.COMPLETED:
            return self._handle_completed_state_input(user_uuid, user_input)

        return [Text("Error. Type 'start' to restart.")]

    def _process_location(self, user_uuid: str, location: str) -> list:
        """Process and validate location input"""
        location = location.strip()

        # Basic validation - check if it looks like "City, Country"
        if ',' not in location or len(location) < 5:
            return [
                Text("Format: 'City, Country'")
            ]

        # Save location and advance state
        self.preferences_manager.update_user_preferences(user_uuid, location=location)
        self.preferences_manager.advance_onboarding_state(user_uuid)

        # Return next state message
        return self._get_state_message(user_uuid, OnboardingState.ASKING_INTERESTS)

    def process_pill_selection(self, user_uuid: str, selected_pills: List[str]) -> list:
        """Process pill selections for interests"""
        if not selected_pills:
            return [Text("Pick at least one topic.")]

        # Save interests and advance state
        self.preferences_manager.update_user_preferences(user_uuid, news_interests=selected_pills)
        self.preferences_manager.advance_onboarding_state(user_uuid)

        # Return next state message
        return self._get_state_message(user_uuid, OnboardingState.ASKING_WAKE_TIME)

    def _process_interests(self, user_uuid: str, interests_input: str) -> list:
        """Process and validate interests input"""
        # Check if user typed 'done' after selecting pills
        if interests_input.lower() == 'done':
            # Get stored interests from preferences
            user_prefs = self.preferences_manager.get_or_create_user(user_uuid)
            if user_prefs.news_interests:
                self.preferences_manager.advance_onboarding_state(user_uuid)
                return self._get_state_message(user_uuid, OnboardingState.ASKING_WAKE_TIME)
            else:
                return [Text("Pick at least one topic first.")]

        # If they're typing interests manually (fallback)
        interests = [i.strip().lower() for i in interests_input.split(',')]

        # Validate interests
        valid_interests = []
        invalid_interests = []

        for interest in interests:
            if interest in self.news_categories:
                valid_interests.append(interest)
            else:
                invalid_interests.append(interest)

        if not valid_interests:
            # Show pills again
            return self._get_state_message(user_uuid, OnboardingState.ASKING_INTERESTS)

        # Save interests and advance state
        self.preferences_manager.update_user_preferences(user_uuid, news_interests=valid_interests)
        self.preferences_manager.advance_onboarding_state(user_uuid)

        # Return next state message
        return self._get_state_message(user_uuid, OnboardingState.ASKING_WAKE_TIME)

    def _process_wake_time(self, user_uuid: str, time_input: str) -> list:
        """Process and validate wake time input"""
        time_input = time_input.strip()

        # Validate time format (HH:MM)
        time_pattern = re.compile(r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$')
        match = time_pattern.match(time_input)

        if not match:
            return [Text("Use 24-hour format (e.g., '07:00' or '19:30')")]

        # Normalize time format (ensure 2 digits for hour)
        hour, minute = match.groups()
        normalized_time = f"{hour.zfill(2)}:{minute}"

        # Save wake time and complete onboarding
        self.preferences_manager.update_user_preferences(user_uuid, wake_time=normalized_time)
        self.preferences_manager.advance_onboarding_state(user_uuid)

        # Return completion message
        return self._get_state_message(user_uuid, OnboardingState.COMPLETED)

    def _handle_completed_state_input(self, user_uuid: str, user_input: str) -> list:
        """Handle commands after onboarding is complete"""
        command = user_input.strip().lower()

        if command == 'update' or command == 'restart':
            self.preferences_manager.reset_user_onboarding(user_uuid)
            return self._get_state_message(user_uuid, OnboardingState.NOT_STARTED)

        elif command == 'preview':
            return [Text("Use 'preview' command in main chat.")]

        else:
            return [Text("Type 'help' for commands.")]

    def is_user_onboarded(self, user_uuid: str) -> bool:
        """Check if user has completed onboarding"""
        return self.preferences_manager.is_user_onboarded(user_uuid)
