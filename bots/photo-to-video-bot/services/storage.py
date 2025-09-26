"""
Supabase storage service for video uploads
"""

import logging
import uuid
import os
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class StorageService:
    """Service for uploading videos to Supabase storage"""

    def __init__(self):
        """Initialize the storage service"""
        # Get Supabase credentials from environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

        self.supabase: Client = create_client(supabase_url, supabase_key)
        logger.info("StorageService initialized")

    def _generate_filename(self) -> str:
        """
        Generate unique filename for video

        Returns:
            str: Unique filename with timestamp and UUID
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        return f"generated_video_{timestamp}_{unique_id}.mp4"
