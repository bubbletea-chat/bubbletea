import requests
from typing import Optional, Dict, Any
from config import BUBBLETEA_API_KEY, BUBBLETEA_API_URL, BUBBLETEA_BOT_NAME
import bubbletea_chat as bt


class NotificationService:
    """Service to send notifications via the BubbleTea API"""

    def __init__(self):
        """Initialize notification service with API configuration"""
        self.api_base_url = BUBBLETEA_API_URL
        self.api_key = BUBBLETEA_API_KEY
        self.bot_name = BUBBLETEA_BOT_NAME

    def send_notification(
        self, conversation_uuid: str, message: str, is_user: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Send a notification message to a user via the API

        Args:
            conversation_uuid: The conversation UUID
            message: The message content
            is_user: Whether this is a user message (False for bot messages)

        Returns:
            Response data from the API or None if failed
        """
        if not self._can_send_notification():
            return None

        try:
            return self._send_api_request(conversation_uuid, message, is_user)
        except Exception as e:
            self._log_error("sending notification", e)
            return None

    def send_morning_brief(self, conversation_uuid: str, brief_content: str) -> bool:
        """
        Send a morning brief notification to a user

        Args:
            conversation_uuid: The conversation UUID
            brief_content: The morning brief content

        Returns:
            True if sent successfully, False otherwise
        """
        notification_message = self._format_morning_brief(brief_content)
        result = self.send_notification(conversation_uuid, notification_message, is_user=False)
        return result is not None

    def send_reminder(self, conversation_uuid: str, reminder_text: str) -> bool:
        """
        Send a reminder notification to a user

        Args:
            conversation_uuid: The conversation UUID
            reminder_text: The reminder text

        Returns:
            True if sent successfully, False otherwise
        """
        result = self.send_notification(conversation_uuid, reminder_text, is_user=False)
        return result is not None

    def _can_send_notification(self) -> bool:
        """Check if notifications can be sent"""
        return bool(self.api_key)

    def _send_api_request(self, conversation_uuid: str, message: str, is_user: bool) -> Optional[Dict[str, Any]]:
        """Send the actual API request"""
        url = self._build_api_url(conversation_uuid)
        headers = self._build_headers()
        payload = self._build_payload(message, is_user)

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            self._log_success(conversation_uuid)
            return response.json()
        else:
            self._log_failure(response)
            return None

    def _build_api_url(self, conversation_uuid: str) -> str:
        """Build the API URL for sending messages"""
        return f"{self.api_base_url}/v1/developer/conversation/{conversation_uuid}/message"

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers"""
        return {"x-api-key": self.api_key, "Content-Type": "application/json", "accept": "application/json"}

    def _build_payload(self, message: str, is_user: bool) -> Dict[str, Any]:
        """Build request payload"""
        message = bt.Markdown(message)
        content = message.model_dump()
        return {"sender": "agent", "content": content}

    def _format_morning_brief(self, brief_content: str) -> str:
        """Format morning brief with notification header"""
        return f"🌅 **Morning Brief**\n\n{brief_content}"

    def _log_error(self, action: str, error: Exception):
        """Log error during notification process"""
        pass

    def _log_success(self, conversation_uuid: str):
        """Log successful notification"""
        pass

    def _log_failure(self, response):
        """Log failed notification"""
        pass
