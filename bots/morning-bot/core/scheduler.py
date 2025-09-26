import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from core.user_preferences import UserPreferences
from services.notification_service import NotificationService
from storage.storage_adapter import StorageAdapter


class Scheduler:
    """Handles scheduling and execution of morning brief notifications"""

    def __init__(self):
        """Initialize the scheduler"""
        self.notification_service = NotificationService()
        self.storage = StorageAdapter()
        self._scheduled_tasks: Dict[str, threading.Thread] = {}
        self._running = True
        self._lock = threading.Lock()

    def schedule_morning_brief(self, conversation_uuid: str) -> bool:
        """
        Schedule morning brief for a user based on their preferences

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            True if scheduled successfully, False otherwise
        """
        try:
            user_prefs = UserPreferences(conversation_uuid)

            # Check if notifications are enabled
            if not user_prefs.get_notifications_enabled():
                return False

            # Get user's preferred time
            brief_time = user_prefs.get_brief_time()

            # Calculate next execution time
            next_execution = self._calculate_next_execution_time(brief_time)

            # Cancel existing task if any
            self.cancel_morning_brief(conversation_uuid)

            # Schedule new task
            task_thread = threading.Thread(
                target=self._scheduled_morning_brief_task, args=(conversation_uuid, next_execution), daemon=True
            )

            with self._lock:
                self._scheduled_tasks[conversation_uuid] = task_thread

            task_thread.start()
            return True

        except Exception as e:
            self._log_error(f"scheduling morning brief for {conversation_uuid}", e)
            return False

    def cancel_morning_brief(self, conversation_uuid: str) -> bool:
        """
        Cancel scheduled morning brief for a user

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            True if cancelled successfully, False otherwise
        """
        try:
            with self._lock:
                if conversation_uuid in self._scheduled_tasks:
                    # Note: We can't actually cancel a running thread in Python
                    # This removes it from our tracking, but the thread will complete naturally
                    del self._scheduled_tasks[conversation_uuid]
                    return True
            return False
        except Exception as e:
            self._log_error(f"cancelling morning brief for {conversation_uuid}", e)
            return False

    def schedule_recurring_brief(self, conversation_uuid: str, brief_generator: Callable[[str], str]) -> bool:
        """
        Schedule recurring daily morning briefs

        Args:
            conversation_uuid: The unique conversation identifier
            brief_generator: Function that generates brief content

        Returns:
            True if scheduled successfully, False otherwise
        """
        try:
            task_thread = threading.Thread(
                target=self._recurring_brief_task, args=(conversation_uuid, brief_generator), daemon=True
            )

            with self._lock:
                self._scheduled_tasks[f"{conversation_uuid}_recurring"] = task_thread

            task_thread.start()
            return True

        except Exception as e:
            self._log_error(f"scheduling recurring brief for {conversation_uuid}", e)
            return False

    def schedule_reminder(self, conversation_uuid: str, reminder_time: datetime, reminder_text: str) -> bool:
        """
        Schedule a one-time reminder

        Args:
            conversation_uuid: The unique conversation identifier
            reminder_time: When to send the reminder
            reminder_text: The reminder message

        Returns:
            True if scheduled successfully, False otherwise
        """
        try:
            if reminder_time <= datetime.now():
                return False

            task_id = f"{conversation_uuid}_reminder_{int(reminder_time.timestamp())}"
            task_thread = threading.Thread(
                target=self._scheduled_reminder_task,
                args=(conversation_uuid, reminder_time, reminder_text),
                daemon=True,
            )

            with self._lock:
                self._scheduled_tasks[task_id] = task_thread

            task_thread.start()
            return True

        except Exception as e:
            self._log_error(f"scheduling reminder for {conversation_uuid}", e)
            return False

    def get_active_schedules(self) -> List[str]:
        """
        Get list of active scheduled tasks

        Returns:
            List of conversation UUIDs with active schedules
        """
        with self._lock:
            return list(self._scheduled_tasks.keys())

    def cancel_all_schedules(self):
        """Cancel all scheduled tasks"""
        with self._lock:
            self._running = False
            self._scheduled_tasks.clear()

    def is_scheduled(self, conversation_uuid: str) -> bool:
        """
        Check if user has an active schedule

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            True if user has active schedules, False otherwise
        """
        with self._lock:
            return any(conversation_uuid in task_id for task_id in self._scheduled_tasks.keys())

    def _calculate_next_execution_time(self, brief_time: time) -> datetime:
        """
        Calculate the next execution time for a brief

        Args:
            brief_time: The preferred time for the brief

        Returns:
            Next execution datetime
        """
        now = datetime.now()
        today_execution = now.replace(hour=brief_time.hour, minute=brief_time.minute, second=0, microsecond=0)

        if today_execution <= now:
            # Schedule for tomorrow if today's time has passed
            return today_execution + timedelta(days=1)
        else:
            # Schedule for today if the time hasn't passed yet
            return today_execution

    def _scheduled_morning_brief_task(self, conversation_uuid: str, execution_time: datetime):
        """
        Execute a scheduled morning brief task

        Args:
            conversation_uuid: The unique conversation identifier
            execution_time: When to execute the task
        """
        # Wait until execution time
        while self._running and datetime.now() < execution_time:
            time.sleep(60)  # Check every minute

        if not self._running:
            return

        try:
            # Generate and send morning brief
            brief_content = self._generate_morning_brief(conversation_uuid)
            if brief_content:
                self.notification_service.send_morning_brief(conversation_uuid, brief_content)

                # Store the brief
                self.storage.store_morning_brief(conversation_uuid, brief_content)

        except Exception as e:
            self._log_error(f"executing morning brief task for {conversation_uuid}", e)
        finally:
            # Clean up from active tasks
            with self._lock:
                if conversation_uuid in self._scheduled_tasks:
                    del self._scheduled_tasks[conversation_uuid]

    def _recurring_brief_task(self, conversation_uuid: str, brief_generator: Callable[[str], str]):
        """
        Execute recurring morning brief task

        Args:
            conversation_uuid: The unique conversation identifier
            brief_generator: Function to generate brief content
        """
        while self._running:
            try:
                user_prefs = UserPreferences(conversation_uuid)

                # Check if notifications are still enabled
                if not user_prefs.get_notifications_enabled():
                    break

                # Get current time and preferred brief time
                brief_time = user_prefs.get_brief_time()
                next_execution = self._calculate_next_execution_time(brief_time)

                # Wait until execution time
                while self._running and datetime.now() < next_execution:
                    time.sleep(60)  # Check every minute

                if not self._running:
                    break

                # Generate and send brief
                brief_content = brief_generator(conversation_uuid)
                if brief_content:
                    self.notification_service.send_morning_brief(conversation_uuid, brief_content)
                    self.storage.store_morning_brief(conversation_uuid, brief_content)

                # Wait a bit to avoid duplicate sends
                time.sleep(120)

            except Exception as e:
                self._log_error(f"recurring brief task for {conversation_uuid}", e)
                break

        # Clean up from active tasks
        with self._lock:
            task_id = f"{conversation_uuid}_recurring"
            if task_id in self._scheduled_tasks:
                del self._scheduled_tasks[task_id]

    def _scheduled_reminder_task(self, conversation_uuid: str, reminder_time: datetime, reminder_text: str):
        """
        Execute a scheduled reminder task

        Args:
            conversation_uuid: The unique conversation identifier
            reminder_time: When to send the reminder
            reminder_text: The reminder message
        """
        # Wait until reminder time
        while self._running and datetime.now() < reminder_time:
            time.sleep(60)  # Check every minute

        if not self._running:
            return

        try:
            # Send reminder
            self.notification_service.send_reminder(conversation_uuid, reminder_text)

        except Exception as e:
            self._log_error(f"executing reminder task for {conversation_uuid}", e)
        finally:
            # Clean up from active tasks
            task_id = f"{conversation_uuid}_reminder_{int(reminder_time.timestamp())}"
            with self._lock:
                if task_id in self._scheduled_tasks:
                    del self._scheduled_tasks[task_id]

    def _generate_morning_brief(self, conversation_uuid: str) -> Optional[str]:
        """
        Generate morning brief content for a user

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            Brief content string or None if generation failed
        """
        try:
            user_prefs = UserPreferences(conversation_uuid)

            # Get user preferences
            location = user_prefs.get_weather_location()
            categories = user_prefs.get_news_categories()
            sections = user_prefs.get_brief_sections()

            brief_parts = []
            brief_parts.append("# 🌅 Good Morning!")
            brief_parts.append(f"Here's your personalized brief for {datetime.now().strftime('%A, %B %d, %Y')}:")

            # Add weather section if enabled and location is set
            if sections.get("weather", True) and location:
                from ..services.weather_service import WeatherService

                weather_service = WeatherService()
                weather = weather_service.get_weather_forecast(location)
                if weather:
                    brief_parts.append(f"\n## 🌤️ Weather for {location}")
                    brief_parts.append(weather)

            # Add news section if enabled
            if sections.get("news", True):
                from ..services.news_service import NewsService

                news_service = NewsService()
                news = news_service.get_news_headlines(categories)
                if news:
                    brief_parts.append("\n## 📰 News Headlines")
                    brief_parts.append(news)

            # Add motivational quote if enabled
            if sections.get("motivational_quote", False):
                brief_parts.append("\n## ✨ Daily Inspiration")
                brief_parts.append('_"The way to get started is to quit talking and begin doing."_ - Walt Disney')

            return "\n".join(brief_parts)

        except Exception as e:
            self._log_error(f"generating morning brief for {conversation_uuid}", e)
            return None

    def _log_error(self, action: str, error: Exception):
        """Log scheduler errors"""
        pass
