import json
from typing import Dict, Any, Optional, List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from config import FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, FIREBASE_CLIENT_EMAIL


class StorageAdapter:
    """Handles data persistence operations for user data and preferences using Firebase Firestore"""

    def __init__(self):
        """Initialize storage adapter with Firebase Firestore configuration"""
        self.db = None
        self.is_connected = self._initialize_firebase()

    def _initialize_firebase(self) -> bool:
        """Initialize Firebase Admin SDK and Firestore client"""
        try:
            # Check if Firebase is already initialized
            if not firebase_admin._apps:
                # Initialize Firebase Admin SDK with service account credentials
                if FIREBASE_PROJECT_ID and FIREBASE_PRIVATE_KEY and FIREBASE_CLIENT_EMAIL:
                    # Create credentials from environment variables
                    cred_dict = {
                        "type": "service_account",
                        "project_id": FIREBASE_PROJECT_ID,
                        "private_key": FIREBASE_PRIVATE_KEY.replace('\\n', '\n'),
                        "client_email": FIREBASE_CLIENT_EMAIL,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    }
                    
                    cred = credentials.Certificate(cred_dict)
                    firebase_admin.initialize_app(cred)
                else:
                    # Try to initialize with default credentials (for local development)
                    firebase_admin.initialize_app()
            
            # Get Firestore client
            self.db = firestore.client()
            return True
            
        except Exception as e:
            self._log_error("initializing Firebase", e)
            return False

    def store_user_preference(self, conversation_uuid: str, preference_key: str, preference_value: Any) -> bool:
        """
        Store a user preference in Firestore

        Args:
            conversation_uuid: The unique conversation identifier
            preference_key: The preference key (e.g., 'timezone', 'weather_location')
            preference_value: The preference value

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            if not self.is_connected or not self.db:
                return False
                
            # Create document reference
            doc_ref = self.db.collection('user_preferences').document(f"{conversation_uuid}_{preference_key}")
            
            # Prepare data
            data = {
                "conversation_uuid": conversation_uuid,
                "preference_key": preference_key,
                "preference_value": str(preference_value),
                "updated_at": datetime.now().isoformat(),
            }
            
            # Set document (upsert)
            doc_ref.set(data)
            return True
            
        except Exception as e:
            self._log_error(f"storing preference {preference_key}", e)
            return False

    def get_user_preference(self, conversation_uuid: str, preference_key: str, default_value: Any = None) -> Any:
        """
        Retrieve a user preference from Firestore

        Args:
            conversation_uuid: The unique conversation identifier
            preference_key: The preference key to retrieve
            default_value: Default value if preference not found

        Returns:
            The preference value or default_value if not found
        """
        try:
            if not self.is_connected or not self.db:
                return default_value
                
            # Get document reference
            doc_ref = self.db.collection('user_preferences').document(f"{conversation_uuid}_{preference_key}")
            
            # Get document
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                return self._parse_preference_value(data.get("preference_value", default_value))
                
            return default_value
            
        except Exception as e:
            self._log_error(f"retrieving preference {preference_key}", e)
            return default_value

    def get_all_user_preferences(self, conversation_uuid: str) -> Dict[str, Any]:
        """
        Retrieve all user preferences for a conversation from Firestore

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            Dictionary of all user preferences
        """
        try:
            if not self.is_connected or not self.db:
                return {}
                
            # Query all preferences for the conversation
            prefs_ref = self.db.collection('user_preferences')
            query = prefs_ref.where(filter=FieldFilter("conversation_uuid", "==", conversation_uuid))
            docs = query.stream()
            
            preferences = {}
            for doc in docs:
                data = doc.to_dict()
                key = data.get("preference_key")
                value = self._parse_preference_value(data.get("preference_value"))
                if key:
                    preferences[key] = value
            
            return preferences
            
        except Exception as e:
            self._log_error("retrieving all preferences", e)
            return {}

    def store_morning_brief(self, conversation_uuid: str, brief_content: str, brief_date: Optional[str] = None) -> bool:
        """
        Store a morning brief in Firestore

        Args:
            conversation_uuid: The unique conversation identifier
            brief_content: The morning brief content
            brief_date: The date of the brief (defaults to today)

        Returns:
            True if stored successfully, False otherwise
        """
        try:
            if not self.is_connected or not self.db:
                return False
                
            if not brief_date:
                brief_date = datetime.now().strftime("%Y-%m-%d")
            
            # Create collection reference
            briefs_ref = self.db.collection('morning_briefs')
            
            # Prepare data
            data = {
                "conversation_uuid": conversation_uuid,
                "brief_content": brief_content,
                "brief_date": brief_date,
                "created_at": datetime.now(),
            }
            
            # Add document
            briefs_ref.add(data)
            return True
            
        except Exception as e:
            self._log_error("storing morning brief", e)
            return False

    def get_recent_morning_briefs(self, conversation_uuid: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve recent morning briefs for a user from Firestore

        Args:
            conversation_uuid: The unique conversation identifier
            limit: Maximum number of briefs to retrieve

        Returns:
            List of recent morning briefs
        """
        try:
            if not self.is_connected or not self.db:
                return []
                
            # Query morning briefs
            briefs_ref = self.db.collection('morning_briefs')
            # Note: Composite index required for where + orderBy on different fields
            # For now, we'll fetch all and sort in memory to avoid index requirement
            query = briefs_ref.where(filter=FieldFilter("conversation_uuid", "==", conversation_uuid))
            
            docs = query.stream()
            
            briefs = []
            for doc in docs:
                data = doc.to_dict()
                # Convert datetime to ISO format string
                if 'created_at' in data and hasattr(data['created_at'], 'isoformat'):
                    data['created_at'] = data['created_at'].isoformat()
                briefs.append(data)
            
            # Sort by created_at in descending order and apply limit
            briefs.sort(key=lambda x: x.get('created_at', ''), reverse=True)
            return briefs[:limit]
            
        except Exception as e:
            self._log_error("retrieving morning briefs", e)
            return []

    def delete_user_data(self, conversation_uuid: str) -> bool:
        """
        Delete all user data for privacy compliance from Firestore

        Args:
            conversation_uuid: The unique conversation identifier

        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if not self.is_connected or not self.db:
                return False
                
            success = True
            
            # Delete user preferences
            prefs_ref = self.db.collection('user_preferences')
            prefs_query = prefs_ref.where(filter=FieldFilter("conversation_uuid", "==", conversation_uuid))
            for doc in prefs_query.stream():
                doc.reference.delete()
            
            # Delete morning briefs
            briefs_ref = self.db.collection('morning_briefs')
            briefs_query = briefs_ref.where(filter=FieldFilter("conversation_uuid", "==", conversation_uuid))
            for doc in briefs_query.stream():
                doc.reference.delete()
            
            return success
            
        except Exception as e:
            self._log_error("deleting user data", e)
            return False

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
        print(f"Error while {action}: {str(error)}")