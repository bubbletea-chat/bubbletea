import json
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from config import SUPABASE_URL, SUPABASE_KEY


class StorageAdapter:
    """Handles data persistence operations for user data and preferences"""

    def __init__(self):
        """Initialize storage adapter with database configuration"""
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_KEY
        self.is_connected = self._validate_connection()

    def store_user_preference(self, conversation_uuid: str, preference_key: str, preference_value: Any) -> bool:
        """
        Store a user preference in the database

        Args:
            conversation_uuid: The unique conversation identifier
            preference_key: The preference key (e.g., 'timezone', 'weather_location')
            preference_value: The preference value

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            data = {
                "conversation_uuid": conversation_uuid,
                "preference_key": preference_key,
                "preference_value": str(preference_value),
                "updated_at": datetime.now().isoformat(),
            }
            return self._execute_upsert("user_preferences", data)
        except Exception as e:
            self._log_error(f"storing preference {preference_key}", e)
            return False

    def get_user_preference(self, conversation_uuid: str, preference_key: str, default_value: Any = None) -> Any:
        """
        Retrieve a user preference from the database

        Args:
            conversation_uuid: The unique conversation identifier
            preference_key: The preference key to retrieve
            default_value: Default value if preference not found

        Returns:
            The preference value or default_value if not found
        """
        try:
            query_conditions = {"conversation_uuid": conversation_uuid, "preference_key": preference_key}
            result = self._execute_select("user_preferences", query_conditions)

            if result and len(result) > 0:
                return self._parse_preference_value(result[0]["preference_value"])
            return default_value
        except Exception as e:
            self._log_error(f"retrieving preference {preference_key}", e)
            return default_value

    def get_all_user_preferences(self, conversation_uuid: str) -> Dict[str, Any]:
        """
        Retrieve all user preferences for a conversation

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            Dictionary of all user preferences
        """
        try:
            query_conditions = {"conversation_uuid": conversation_uuid}
            results = self._execute_select("user_preferences", query_conditions)

            preferences = {}
            for result in results or []:
                key = result["preference_key"]
                value = self._parse_preference_value(result["preference_value"])
                preferences[key] = value

            return preferences
        except Exception as e:
            self._log_error("retrieving all preferences", e)
            return {}

    def store_morning_brief(self, conversation_uuid: str, brief_content: str, brief_date: Optional[str] = None) -> bool:
        """
        Store a morning brief in the database

        Args:
            conversation_uuid: The unique conversation identifier
            brief_content: The morning brief content
            brief_date: The date of the brief (defaults to today)

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            if not brief_date:
                brief_date = datetime.now().strftime("%Y-%m-%d")

            data = {
                "conversation_uuid": conversation_uuid,
                "brief_content": brief_content,
                "brief_date": brief_date,
                "created_at": datetime.now().isoformat(),
            }
            return self._execute_insert("morning_briefs", data)
        except Exception as e:
            self._log_error("storing morning brief", e)
            return False

    def get_recent_morning_briefs(self, conversation_uuid: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve recent morning briefs for a user

        Args:
            conversation_uuid: The unique conversation identifier
            limit: Maximum number of briefs to retrieve

        Returns:
            List of recent morning briefs
        """
        try:
            query_conditions = {"conversation_uuid": conversation_uuid}
            results = self._execute_select("morning_briefs", query_conditions, limit=limit, order_by="created_at DESC")
            return results or []
        except Exception as e:
            self._log_error("retrieving morning briefs", e)
            return []

    def delete_user_data(self, conversation_uuid: str) -> bool:
        """
        Delete all user data for privacy compliance

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            tables_to_clean = ["user_preferences", "morning_briefs"]
            success = True

            for table in tables_to_clean:
                query_conditions = {"conversation_uuid": conversation_uuid}
                if not self._execute_delete(table, query_conditions):
                    success = False

            return success
        except Exception as e:
            self._log_error("deleting user data", e)
            return False

    def _validate_connection(self) -> bool:
        """Validate database connection"""
        return bool(self.supabase_url and self.supabase_key)

    def _execute_select(
        self, table: str, conditions: Dict[str, Any], limit: Optional[int] = None, order_by: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Execute a SELECT query"""
        if not self.is_connected:
            return None

        # In a real implementation, this would use Supabase client
        # For now, return None to indicate no results
        return None

    def _execute_insert(self, table: str, data: Dict[str, Any]) -> bool:
        """Execute an INSERT query"""
        if not self.is_connected:
            return False

        # In a real implementation, this would use Supabase client
        return True

    def _execute_upsert(self, table: str, data: Dict[str, Any]) -> bool:
        """Execute an UPSERT query"""
        if not self.is_connected:
            return False

        # In a real implementation, this would use Supabase client
        return True

    def _execute_delete(self, table: str, conditions: Dict[str, Any]) -> bool:
        """Execute a DELETE query"""
        if not self.is_connected:
            return False

        # In a real implementation, this would use Supabase client
        return True

    def _parse_preference_value(self, value: str) -> Any:
        """Parse stored preference value"""
        try:
            # Try to parse as JSON first
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # Return as string if not valid JSON
            return value

    def _log_error(self, action: str, error: Exception):
        """Log storage errors"""
        pass
