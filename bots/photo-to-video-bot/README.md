# Photo to Video Bot

## Description
An advanced multimedia bot that transforms collections of photos into dynamic video presentations. This bot allows users to upload multiple images and automatically generates professional-looking videos with transitions, effects, and optional background music.

## Features
- Multi-photo upload support
- Automatic video generation with transitions
- Customizable video duration and framerate
- Multiple transition effects (fade, slide, zoom)
- Background music integration
- Resolution optimization
- Progress tracking during generation
- Download link for generated videos

## Setup Instructions
1. Clone this repository
2. Navigate to the bot folder: `cd photo_to_video_bot`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy environment variables: `cp .env.example .env`
5. Configure settings in `.env`
6. Create required directories: `mkdir uploads outputs`
7. Run the bot: `python bot.py`

## Commands
- `/start` - Begin video creation process
- `/upload` - Upload photos (up to 10)
- `/generate` - Create video from uploaded photos
- `/settings` - Configure video parameters
- `/preview` - Preview video settings
- `/download` - Get download link for video
- `/clear` - Clear uploaded photos

## Configuration
### Video Generation Options
### Transitions
- **Fade**: Smooth fade between photos
- **Slide**: Sliding transition effect
- **Zoom**: Ken Burns zoom effect
- **Dissolve**: Cross-dissolve transition
- **Wipe**: Directional wipe effect

### Video Customization
- Duration: 10-60 seconds
- FPS: 24, 30, or 60
- Resolution: 720p, 1080p, 4K
- Audio: Optional background music
- Text: Add captions or titles

## Use Cases
- **Photo Slideshows**: Create memorable presentations
- **Event Recaps**: Compile event photos into videos
- **Social Media Content**: Generate shareable video content
- **Portfolio Presentations**: Showcase work professionally
- **Memory Books**: Digital photo albums with motion
- **Marketing Materials**: Product showcase videos

## Technical Details
- **Image Processing**: OpenCV for manipulation
- **Video Generation**: MoviePy for video creation
- **File Handling**: Secure upload/download system
- **Format Support**: JPG, PNG, GIF input
- **Output Format**: MP4 with H.264 codec

### Performance Considerations
- Maximum 10 photos per video
- File size limit: 10MB per photo
- Processing time: ~30 seconds for 10 photos
- Concurrent generation support
- Automatic cleanup of old files

## Deployment Options
- **Local**: Run with sufficient CPU/RAM
- **Docker**: Container with all dependencies
- **Cloud**: AWS/GCP with GPU acceleration
- **Serverless**: Lambda with EFS for storage

## Support
- **BubbleTea Documentation & Issues**: [github.com/bubbletea-chat/bubbletea](https://github.com/bubbletea-chat/bubbletea)