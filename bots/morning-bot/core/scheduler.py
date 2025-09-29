import threading
import time
import os
import json
from datetime import datetime, time as datetime_time
from typing import Dict, Optional
from core.user_preferences import UserPreferencesManager, UserPreferences
from services.weather_service import WeatherService
from services.news_service import NewsService
from services.notification_service import NotificationService
from storage.storage_adapter import StorageAdapter


class MorningBriefScheduler:
    """Scheduler for generating and sending morning briefs"""

    BRIEFS_DIR = "user_data"
    CHECK_INTERVAL = 60  # 30 minutes in seconds

    def __init__(self, preferences_manager: UserPreferencesManager,
                 weather_service: WeatherService, news_service: NewsService):
        """Initialize scheduler with required services"""
        self.preferences_manager = preferences_manager
        self.weather_service = weather_service
        self.news_service = news_service
        self.notification_service = NotificationService()
        self.storage = StorageAdapter()

        self.running = False
        self.thread = None
        self.sent_today: Dict[str, str] = {}  # user_id -> date_sent

    def start(self):
        """Start the scheduler in a background thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_scheduler,
                                           daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the scheduler"""
        self.running = False
        if self.thread:
            self.thread.join()

    def _get_user_brief_path(self, user_uuid: str) -> str:
        """Get the file path for a user's morning brief"""
        return f"{self.BRIEFS_DIR}/{user_uuid}/morning_brief.json"

    def get_user_brief(self, user_uuid: str) -> Optional[str]:
        """Get stored morning brief for a user"""
        try:
            file_path = self._get_user_brief_path(user_uuid)
            brief_data = self.storage.load(file_path)

            if brief_data and self._is_today(brief_data.get('timestamp')):
                return brief_data.get('brief')
        except Exception as e:
            print(f"Error loading brief for user {user_uuid}: {e}")

        return None

    def generate_preview(self, user_uuid: str) -> str:
        """Generate a preview brief for a user"""
        user_pref = self.preferences_manager.get_or_create_user(user_uuid)

        if not user_pref.is_complete():
            return "Complete setup first! Type 'start'."

        return self.generate_morning_brief(user_pref)

    def trigger_manual_brief(self,
                             user_uuid: str,
                             conversation_uuid: str = None) -> str:
        """Manually trigger a morning brief for testing"""
        user_pref = self.preferences_manager.get_or_create_user(user_uuid)
        print("user pref: ", user_pref)

        if not user_pref.is_complete():
            return "Please complete your setup first!"

        # Generate and store the brief
        brief = self.generate_morning_brief(user_pref)
        self._store_brief_for_user(user_uuid, brief)
        self._mark_sent_today(user_uuid)

        # Brief generated

        # Send notification if conversation UUID is provided
        if conversation_uuid:
            return self._send_notification_and_get_result(
                conversation_uuid, brief, user_uuid)
        else:
            # No conversation UUID
            return "Brief generated! Type 'morning' to view."

    def generate_morning_brief(self, user_pref: UserPreferences) -> str:
        """Generate a complete morning brief for a user"""
        greeting = self._get_greeting()
        weather_summary = self._get_weather_summary(user_pref)
        news_summary = self._get_news_summary(user_pref)

        return self._format_morning_brief(greeting, user_pref.location,
                                          weather_summary, news_summary)

    def _run_scheduler(self):
        """Main scheduler loop"""
        # Scheduler started

        while self.running:
            try:
                self._check_and_send_briefs()
                time.sleep(self.CHECK_INTERVAL)
            except Exception as e:
                self._log_scheduler_error(e)
                time.sleep(self.CHECK_INTERVAL)

    def _check_and_send_briefs(self):
        """Check for users who need their morning brief"""
        current_time = datetime.now()
        current_time_obj = datetime_time(current_time.hour,
                                         current_time.minute)

        users = self.preferences_manager.get_users_by_wake_time(
            current_time_obj)

        # Check users

        for user_pref in users:
            if not self._already_sent_today(user_pref.user_uuid):
                self._generate_and_send_brief(user_pref)

    def _generate_and_send_brief(self, user_pref: UserPreferences):
        """Generate and send brief for a user"""
        brief = self.generate_morning_brief(user_pref)
        self._store_brief_for_user(user_pref.user_uuid, brief)
        self._mark_sent_today(user_pref.user_uuid)
        print("uuid: ", user_pref.conversation_uuid)

        # Send notification if conversation UUID is available
        if hasattr(user_pref,
                   'conversation_uuid') and user_pref.conversation_uuid:
            self._send_notification(user_pref.conversation_uuid, brief,
                                    user_pref.user_uuid)

    def _get_greeting(self) -> str:
        """Get time-appropriate greeting"""
        hour = datetime.now().hour

        if hour < 12:
            return "☀️ **Morning!**"
        elif hour < 17:
            return "🌤️ **Afternoon!**"
        else:
            return "🌅 **Evening!**"

    def _get_weather_summary(self, user_pref: UserPreferences) -> str:
        """Get weather summary for user's location"""
        if user_pref.location:
            return self.weather_service.get_weather_summary_openai(
                user_pref.location)
        return "Weather unavailable"

    def _get_news_summary(self, user_pref: UserPreferences) -> str:
        """Get news summary for user's interests"""
        if user_pref.news_interests and user_pref.location:
            return self.news_service.get_news_summary_openai(
                user_pref.news_interests, user_pref.location)
        return "No news"

    def _format_morning_brief(self, greeting: str, location: str, weather: str,
                              news: str) -> str:
        """Format the complete morning brief"""
        return (f"{greeting} 📍 {location}\n\n"
                f"{weather}\n\n"
                f"{news}\n\n"
                "Have a great day! 🌟")

    def _store_brief_for_user(self, user_uuid: str, brief: str):
        """Store the morning brief for retrieval by the bot"""
        try:
            file_path = self._get_user_brief_path(user_uuid)
            brief_data = {
                'user_uuid': user_uuid,
                'brief': brief,
                'timestamp': datetime.now().isoformat()
            }
            self.storage.save(file_path, brief_data)
        except Exception as e:
            print(f"Error storing brief for user {user_uuid}: {e}")

    def _is_today(self, timestamp_str: str) -> bool:
        """Check if timestamp is from today"""
        try:
            brief_date = datetime.fromisoformat(timestamp_str).date()
            return brief_date == datetime.now().date()
        except:
            return False

    def _already_sent_today(self, user_uuid: str) -> bool:
        """Check if brief was already sent today"""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.sent_today.get(user_uuid) == today

    def _mark_sent_today(self, user_uuid: str):
        """Mark that brief was sent today"""
        today = datetime.now().strftime("%Y-%m-%d")
        self.sent_today[user_uuid] = today

    def _send_notification(self, conversation_uuid: str, brief: str,
                           user_uuid: str):
        """Send notification to user"""
        self.notification_service.send_morning_brief(conversation_uuid, brief)

    def _send_notification_and_get_result(self, conversation_uuid: str,
                                          brief: str, user_uuid: str) -> str:
        """Send notification and return result message"""
        if self.notification_service.send_morning_brief(
                conversation_uuid, brief):
            return "Brief sent!"
        else:
            return "Brief saved. Type 'morning' to view."

    def _log_startup(self):
        """Log scheduler startup"""
        pass

    def _log_scheduler_error(self, error: Exception):
        pass
