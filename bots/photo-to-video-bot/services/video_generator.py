"""
Video generation service using Google's Vertex AI Veo 2 model
"""

import asyncio
import logging
import time
import os
from typing import Optional
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv

from dotenv import load_dotenv

import requests
from supabase import Client, create_client
from .storage import StorageService

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class VideoGeneratorService:
    """Service for generating videos using Vertex AI Veo 2"""

    def __init__(self):
        """Initialize the video generator service"""
        # Get API key from environment variables
        vertex_api_key = os.getenv("VERTEX_API_KEY")
        if not vertex_api_key:
            raise ValueError("VERTEX_API_KEY environment variable is required")

        # Configure Google Gen AI client
        self.client = genai.Client(api_key=vertex_api_key)
        self.vertex_api_key = vertex_api_key
        logger.info("VideoGeneratorService initialized with new Google Gen AI SDK")

    async def generate_video_async(self, text_prompt: Optional[str] = None, image_url: Optional[str] = None) -> str:
        """
        Generate a video using Veo 2 model (async version)

        Args:
            text_prompt: Optional text prompt for video generation
            image_url: Optional image URL for visual prompt

        Returns:
            str: Temporary video file path

        Raises:
            ValueError: If neither text_prompt nor image_url is provided
            Exception: If video generation fails
        """
        # Run the synchronous video generation in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.generate_video, text_prompt, image_url)

    def generate_video(self, text_prompt: Optional[str] = None, image_url: Optional[str] = None) -> str:
        """
        Generate a video using Veo 2 model

        Args:
            text_prompt: Optional text prompt for video generation
            image_url: Optional image URL for visual prompt

        Returns:
            str: Temporary video URL

        Raises:
            ValueError: If neither text_prompt nor image_url is provided
            Exception: If video generation fails
        """
        try:
            if not text_prompt and not image_url:
                raise ValueError("Either text_prompt or image_url must be provided")

            # Validate image URL if provided
            if image_url:
                is_valid, error_msg = self._validate_image_url_sync(image_url)
                if not is_valid:
                    raise ValueError(f"Invalid image URL: {error_msg}")

            # Generate video using Veo 2
            if image_url:
                import tempfile

                response = requests.get(image_url)
                response.raise_for_status()  # Raise an error if download fails

                # Save to temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
                temp_file.write(response.content)
                temp_file.close()
                print("temp file: ", temp_file.name)
                image = types.Image.from_file(location=temp_file.name)

            operation = self.client.models.generate_videos(
                model="veo-2.0-generate-001",
                prompt=text_prompt,
                image=image if image_url else None,
                config=types.GenerateVideosConfig(
                    number_of_videos=1, duration_seconds=5, aspect_ratio="16:9", enhance_prompt=True
                ),
            )
            # Poll operation until complete
            max_wait_time = 300  # 5 minutes timeout
            start_time = time.time()

            while not operation.done:
                if time.time() - start_time > max_wait_time:
                    raise Exception("Video generation timeout")

                time.sleep(5)  # Wait 20 seconds before checking again
                operation = self.client.operations.get(operation)

            # Get the generated video
            if operation.response and operation.response.generated_videos:
                generated_video = operation.response.generated_videos[0]
                video_uri = generated_video.video.uri

                # Add API key to the URI for authentication
                if "?" in video_uri:
                    download_url = f"{video_uri}&key={self.vertex_api_key}"
                else:
                    download_url = f"{video_uri}?key={self.vertex_api_key}"

                logger.info(f"Downloading video from: {download_url}")

                # Download the video using requests
                response = requests.get(download_url, timeout=300)
                response.raise_for_status()
                # return BT.Error for now bt.Text("Video generation failed")
                video_data = response.content
                storage_service = StorageService()

                # Get Supabase credentials from environment variables
                supabase_url = os.getenv("SUPABASE_URL")
                supabase_key = os.getenv("SUPABASE_KEY")

                if not supabase_url or not supabase_key:
                    raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables are required")

                supabase: Client = create_client(supabase_url, supabase_key)
                unique_filename = storage_service._generate_filename()
                response = supabase.storage.from_("bubble-tea").upload(
                    file=video_data,
                    path=unique_filename,
                    file_options={"content-type": "video/mp4", "cache-control": "3600", "upsert": "false"},
                )
                if hasattr(response, "error") and response.error is not None:
                    raise Exception(f"Failed to upload image: {response.error.message}")

                signed_result = supabase.storage.from_("bubble-tea").create_signed_url(
                    unique_filename,
                    60 * 60 * 24 * 365 * 10,  # 10 years
                )
                print("signed_result: ", signed_result)
                if isinstance(signed_result, dict) and "signedURL" in signed_result:
                    video_url = signed_result["signedURL"]
                else:
                    video_url = str(signed_result)

                # logger.info(f"Video generation completed: {video_url}")
                return video_url

        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}", exc_info=True)
            raise

    def _validate_image_url_sync(self, url: str) -> tuple[bool, str]:
        """
        Validate that an image URL is accessible and points to a valid image

        Args:
            url: Image URL to validate

        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        try:
            from urllib.parse import urlparse

            # Basic URL format validation
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"

            if parsed.scheme not in ["http", "https"]:
                return False, "URL must use http or https protocol"

            # Check if URL is accessible
            try:
                response = requests.head(url, timeout=10)

                # Check if request was successful
                if response.status_code not in [200, 201]:
                    return False, f"URL returned status code {response.status_code}"

                # Check content type if available
                content_type = response.headers.get("content-type", "").lower()
                if content_type and not content_type.startswith("image/"):
                    return False, f"URL does not point to an image (content-type: {content_type})"

                return True, "Valid image URL"

            except requests.exceptions.Timeout:
                return False, "URL request timed out"
            except requests.exceptions.RequestException as e:
                return False, f"Failed to access URL: {str(e)}"

        except Exception as e:
            logger.error(f"Error validating image URL {url}: {str(e)}")
            return False, f"Validation error: {str(e)}"
