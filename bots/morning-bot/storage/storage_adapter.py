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
                
            # Create/update single document for all preferences
            doc_ref = self.db.collection('user_preferences').document(conversation_uuid)
            
            # Convert value to JSON string if it's a complex type
            if isinstance(preference_value, (list, dict)):
                stored_value = json.dumps(preference_value)
            else:
                stored_value = str(preference_value)
            
            # Use merge to update only the specific field without overwriting others
            doc_ref.set({
                preference_key: stored_value,
                "conversation_uuid": conversation_uuid,
                "updated_at": datetime.now().isoformat(),
            }, merge=True)
            
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
                
            # Get single document containing all preferences
            doc_ref = self.db.collection('user_preferences').document(conversation_uuid)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                if preference_key in data:
                    return self._parse_preference_value(data.get(preference_key, default_value))
                
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
                
            # Get single document containing all preferences
            doc_ref = self.db.collection('user_preferences').document(conversation_uuid)
            doc = doc_ref.get()
            
            if doc.exists:
                data = doc.to_dict()
                preferences = {}
                
                # Parse each preference value, excluding metadata fields
                for key, value in data.items():
                    if key not in ['conversation_uuid', 'updated_at']:
                        preferences[key] = self._parse_preference_value(value)
                
                return preferences
            
            return {}
            
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
            
            # Delete single user preferences document
            prefs_ref = self.db.collection('user_preferences').document(conversation_uuid)
            prefs_ref.delete()
            
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

    def load(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Load data from Firestore based on key pattern
        Compatible with the abstract StorageAdapter interface
        
        Args:
            key: The storage key (file path pattern)
            
        Returns:
            Dictionary with the loaded data or None
        """
        try:
            if not self.is_connected or not self.db:
                return None
                
            # Parse the key to determine what to load
            if "preferences.json" in key:
                # Extract user_uuid from path like "user_data/{user_uuid}/preferences.json"
                user_uuid = key.split('/')[1] if '/' in key else key
                
                # Get all preferences for this user
                preferences = self.get_all_user_preferences(user_uuid)
                
                if preferences:
                    # Return in expected format
                    return {
                        'user_uuid': user_uuid,
                        'location': preferences.get('location'),
                        'news_interests': preferences.get('news_interests', []),
                        'wake_time': preferences.get('wake_time'),
                        'timezone': preferences.get('timezone', 'UTC'),
                        'onboarding_state': preferences.get('onboarding_state', 'not_started'),
                        'conversation_uuid': preferences.get('conversation_uuid'),
                        'created_at': preferences.get('created_at'),
                        'updated_at': preferences.get('updated_at')
                    }
                    
            elif "morning_brief.json" in key:
                # Extract user_uuid from path
                user_uuid = key.split('/')[1] if '/' in key else key
                
                # Get the most recent brief
                briefs = self.get_recent_morning_briefs(user_uuid, limit=1)
                
                if briefs:
                    data = briefs[0]
                    return {
                        'user_uuid': user_uuid,
                        'brief': data.get('brief_content'),
                        'timestamp': data.get('created_at')
                    }
                    
            return None
            
        except Exception as e:
            self._log_error(f"loading from key {key}", e)
            return None
    
    def save(self, key: str, data: Dict[str, Any]) -> bool:
        """
        Save data to Firestore based on key pattern
        Compatible with the abstract StorageAdapter interface
        
        Args:
            key: The storage key (file path pattern)
            data: The data to save
            
        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if not self.is_connected or not self.db:
                return False
                
            if "preferences.json" in key:
                # Saving user preferences
                user_uuid = data.get('user_uuid')
                if not user_uuid:
                    return False
                    
                # Store each preference
                for pref_key, pref_value in data.items():
                    if pref_key != 'user_uuid':
                        self.store_user_preference(user_uuid, pref_key, pref_value)
                        
                return True
                
            elif "morning_brief.json" in key:
                # Saving morning brief
                user_uuid = data.get('user_uuid')
                brief = data.get('brief')
                
                if user_uuid and brief:
                    return self.store_morning_brief(user_uuid, brief)
                    
            return False
            
        except Exception as e:
            self._log_error(f"saving to key {key}", e)
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if data exists in Firestore
        Compatible with the abstract StorageAdapter interface
        
        Args:
            key: The storage key to check
            
        Returns:
            True if exists, False otherwise
        """
        try:
            if not self.is_connected or not self.db:
                return False
                
            if "preferences.json" in key:
                user_uuid = key.split('/')[1] if '/' in key else key
                preferences = self.get_all_user_preferences(user_uuid)
                return len(preferences) > 0
                
            elif "morning_brief.json" in key:
                user_uuid = key.split('/')[1] if '/' in key else key
                briefs = self.get_recent_morning_briefs(user_uuid, limit=1)
                
                # Check if brief exists for today
                if briefs:
                    today = datetime.now().strftime("%Y-%m-%d")
                    for brief in briefs:
                        if brief.get('brief_date') == today:
                            return True
                            
            return False
            
        except Exception as e:
            self._log_error(f"checking existence of key {key}", e)
            return False
    
    def get_users_by_wake_time(self, wake_time: str) -> List[Dict[str, Any]]:
        """
        Get all users with a specific wake time
        
        Args:
            wake_time: The wake time to filter by (e.g., "08:00")
            
        Returns:
            List of user data dictionaries
        """
        try:
            if not self.is_connected or not self.db:
                return []
                
            # Query all user preference documents
            prefs_ref = self.db.collection('user_preferences')
            # Query documents that have the wake_time field matching the specified time
            wake_time_query = prefs_ref.where(
                filter=FieldFilter("wake_time", "==", wake_time)
            )
            
            wake_time_docs = wake_time_query.stream()
            
            users = []
            for doc in wake_time_docs:
                data = doc.to_dict()
                conversation_uuid = doc.id  # Document ID is the conversation UUID
                
                # Parse stored preference values
                preferences = {}
                for key, value in data.items():
                    if key not in ['conversation_uuid', 'updated_at']:
                        preferences[key] = self._parse_preference_value(value)
                
                # Only include users who have completed onboarding
                if preferences.get('onboarding_state') == 'completed':
                    users.append({
                        'user_uuid': conversation_uuid,
                        'conversation_uuid': conversation_uuid,
                        'location': preferences.get('location'),
                        'news_interests': preferences.get('news_interests', []),
                        'wake_time': wake_time,
                        'timezone': preferences.get('timezone', 'UTC'),
                        'onboarding_state': preferences.get('onboarding_state')
                    })
                        
            return users
            
        except Exception as e:
            self._log_error(f"fetching users by wake time {wake_time}", e)
            return []
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users from the database
        
        Returns:
            List of all user data dictionaries
        """
        try:
            if not self.is_connected or not self.db:
                return []
                
            # Get all user preference documents
            prefs_ref = self.db.collection('user_preferences')
            all_docs = prefs_ref.stream()
            
            users = []
            for doc in all_docs:
                data = doc.to_dict()
                conversation_uuid = doc.id  # Document ID is the conversation UUID
                
                # Parse stored preference values
                preferences = {}
                for key, value in data.items():
                    if key not in ['conversation_uuid', 'updated_at']:
                        preferences[key] = self._parse_preference_value(value)
                
                if preferences:  # Only add if user has preferences
                    users.append({
                        'user_uuid': conversation_uuid,
                        'conversation_uuid': conversation_uuid,
                        'location': preferences.get('location'),
                        'news_interests': preferences.get('news_interests', []),
                        'wake_time': preferences.get('wake_time'),
                        'timezone': preferences.get('timezone', 'UTC'),
                        'onboarding_state': preferences.get('onboarding_state', 'not_started')
                    })
                    
            return users
            
        except Exception as e:
            self._log_error("fetching all users", e)
            return []

    def _log_error(self, action: str, error: Exception):
        """Log storage errors"""
        print(f"Error while {action}: {str(error)}")