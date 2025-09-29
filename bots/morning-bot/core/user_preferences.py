import json
import os
from typing import Dict, List, Optional
from datetime import datetime, time
from dataclasses import dataclass, asdict, field
from enum import Enum
from storage.storage_adapter import StorageAdapter


class OnboardingState(Enum):
    NOT_STARTED = "not_started"
    ASKING_LOCATION = "asking_location"
    ASKING_INTERESTS = "asking_interests"
    ASKING_WAKE_TIME = "asking_wake_time"
    COMPLETED = "completed"


@dataclass
class UserPreferences:
    user_uuid: str
    location: Optional[str] = None
    news_interests: List[str] = field(default_factory=list)
    wake_time: Optional[str] = None  # Format: "HH:MM"
    timezone: Optional[str] = "UTC"
    onboarding_state: str = OnboardingState.NOT_STARTED.value
    conversation_uuid: Optional[str] = None  # For API notifications
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    def is_complete(self) -> bool:
        """Check if all required fields are filled"""
        return all([
            self.location, self.news_interests, self.wake_time,
            self.onboarding_state == OnboardingState.COMPLETED.value
        ])


class UserPreferencesManager:

    def __init__(self, storage_dir: str = "user_data"):
        self.storage_dir = storage_dir
        self.preferences: Dict[str, UserPreferences] = {}
        self.storage = StorageAdapter()
        self._load_all_preferences()

    def _get_user_file_path(self, user_uuid: str) -> str:
        """Get the file path for a specific user's preferences"""
        return f"{self.storage_dir}/{user_uuid}/preferences.json"

    def _load_user_preferences(self, user_uuid: str) -> Optional[UserPreferences]:
        """Load preferences for a specific user"""
        try:
            file_path = self._get_user_file_path(user_uuid)
            data = self.storage.load(file_path)
            if data:
                return UserPreferences.from_dict(data)
            return None
        except Exception as e:
            print(f"Error loading preferences for user {user_uuid}: {e}")
            return None

    def _load_all_preferences(self):
        """Load all user preferences from Supabase"""
        self.preferences = {}
        try:
            # Load all users from database
            if hasattr(self.storage, 'get_all_users'):
                users_data = self.storage.get_all_users()
                for user_data in users_data:
                    user_uuid = user_data['user_uuid']
                    self.preferences[user_uuid] = UserPreferences.from_dict(user_data)
        except Exception as e:
            print(f"Error loading all preferences from Supabase: {e}")

    def _save_user_preferences(self, user_uuid: str):
        """Save preferences for a specific user to their own file"""
        if user_uuid not in self.preferences:
            return

        try:
            file_path = self._get_user_file_path(user_uuid)
            data = self.preferences[user_uuid].to_dict()
            self.storage.save(file_path, data)
        except Exception as e:
            print(f"Error saving preferences for user {user_uuid}: {e}")

    def get_or_create_user(self, user_uuid: str) -> UserPreferences:
        """Get existing user preferences or create new ones"""
        if user_uuid not in self.preferences:
            user_pref = self._load_user_preferences(user_uuid)
            if user_pref:
                self.preferences[user_uuid] = user_pref
            else:
                self.preferences[user_uuid] = UserPreferences(user_uuid=user_uuid)
                self._save_user_preferences(user_uuid)
        return self.preferences[user_uuid]

    def update_user_preferences(self, user_uuid: str,
                                **kwargs) -> UserPreferences:
        """Update user preferences"""
        user_pref = self.get_or_create_user(user_uuid)

        for key, value in kwargs.items():
            if hasattr(user_pref, key):
                setattr(user_pref, key, value)

        user_pref.updated_at = datetime.now().isoformat()
        self._save_user_preferences(user_uuid)
        return user_pref

    def get_users_by_wake_time(self,
                               current_time: time) -> List[UserPreferences]:
        """Get all users who should receive morning updates at the current time"""
        users = []
        current_time_str = current_time.strftime("%H:%M")

        # Get from Supabase
        try:
            db_users = self.storage.get_users_by_wake_time(current_time_str)
            for user_data in db_users:
                user_pref = UserPreferences.from_dict(user_data)
                users.append(user_pref)
        except Exception as e:
            print(f"Error getting users by wake time: {e}")

        return users

    def is_user_onboarded(self, user_uuid: str) -> bool:
        """Check if user has completed onboarding"""
        user_pref = self.get_or_create_user(user_uuid)
        return user_pref.onboarding_state == OnboardingState.COMPLETED.value

    def get_current_onboarding_state(self, user_uuid: str) -> OnboardingState:
        """Get current onboarding state"""
        user_pref = self.get_or_create_user(user_uuid)
        return OnboardingState(user_pref.onboarding_state)

    def advance_onboarding_state(self, user_uuid: str) -> OnboardingState:
        """Move to next onboarding state"""
        user_pref = self.get_or_create_user(user_uuid)

        state_progression = {
            OnboardingState.NOT_STARTED: OnboardingState.ASKING_LOCATION,
            OnboardingState.ASKING_LOCATION: OnboardingState.ASKING_INTERESTS,
            OnboardingState.ASKING_INTERESTS: OnboardingState.ASKING_WAKE_TIME,
            OnboardingState.ASKING_WAKE_TIME: OnboardingState.COMPLETED,
            OnboardingState.COMPLETED: OnboardingState.COMPLETED
        }

        current = OnboardingState(user_pref.onboarding_state)
        next_state = state_progression.get(current,
                                           OnboardingState.NOT_STARTED)

        self.update_user_preferences(user_uuid,
                                     onboarding_state=next_state.value)
        return next_state

    def reset_user_onboarding(self, user_uuid: str):
        """Reset user to start onboarding again"""
        self.update_user_preferences(
            user_uuid,
            location=None,
            news_interests=[],
            wake_time=None,
            onboarding_state=OnboardingState.NOT_STARTED.value)
