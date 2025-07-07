"""
Comprehensive example bot demonstrating ALL BubbleTea features and components
"""

import bubbletea_chat as bt
import json
import asyncio
from datetime import datetime

# Define bot configuration with complete App Store metadata
@bt.config()
def get_config():
    return bt.BotConfig(
        # Required fields
        name="demo-bot",  # Handle for URL (no spaces)
        url="http://localhost:8000",
        is_streaming=True,
        
        # Complete App Store-like metadata
        display_name="Demo Master",  # What users see (max 20 chars)
        subtitle="Showcase all BubbleTea features",  # Max 30 chars
        icon_emoji="�",  # Can use emoji instead of icon_url
        # icon_url="https://example.com/demo-bot-icon-1024x1024.png",  # Alternative to emoji
        preview_video_url="https://example.com/demo-bot-preview.mp4",
        description="""
# Demo Master Bot

A comprehensive demonstration of all BubbleTea features:

## 🎯 Components Showcase
- **Text & Markdown** - Rich text formatting
- **Images & Cards** - Visual content display
- **Pills & Buttons** - Interactive elements
- **Tables & Lists** - Structured data
- **Forms & Inputs** - User data collection
- **Charts & Graphs** - Data visualization
- **Audio & Video** - Media content
- **Maps & Locations** - Geographic data
- **Calendars & Events** - Time-based content

## 🛠️ Advanced Features
- **File Uploads** - Document processing
- **Real-time Updates** - Live data streaming
- **User Authentication** - Secure access
- **Memory & Context** - Conversation history
- **API Integrations** - External services
- **Custom Actions** - Interactive workflows

Try commands like: `showcase`, `components`, `upload`, `chart`, `map`, `calendar`
        """,
        visibility="public",  # or "private" for internal bots
        entrypoint="showcase",  # Launch context
        
        # Complete configuration options
        initial_text="� Welcome to Demo Master! Type 'showcase' to see all features, or ask me anything!",
        max_message_length=2000,
        rate_limit_per_minute=60,
        enable_file_upload=True,
        enable_audio_input=True,
        enable_location_sharing=True,
        
        # For private bots
        # authorized_emails=["team@example.com", "demo@example.com"],
        # required_permissions=["read", "write", "upload"]
    )

# Define the comprehensive chatbot
@bt.chatbot(name="demo-bot", stream=True)
async def demo_bot(message: str, **kwargs):
    """A comprehensive demonstration bot showcasing all BubbleTea features"""
    
    # Access user context
    user_email = kwargs.get('user_email')
    user_uuid = kwargs.get('user_uuid')
    conversation_id = kwargs.get('conversation_id')
    
    # Handle file uploads
    files = kwargs.get('files', [])
    if files:
        yield bt.Text(f"📁 Received {len(files)} file(s):")
        for file in files:
            yield bt.Text(f"• {file.get('name', 'Unknown')} ({file.get('size', 0)} bytes)")
    
    # Handle location data
    location = kwargs.get('location')
    if location:
        yield bt.Text(f"📍 Location received: {location.get('lat', 0)}, {location.get('lng', 0)}")
    
    # Command routing
    command = message.lower().strip()
    
    if command == "showcase" or command == "demo":
        async for item in showcase_all_features():
            yield item
    elif command == "components":
        async for item in showcase_components():
            yield item
    elif command == "charts" or command == "chart":
        async for item in showcase_charts():
            yield item
    elif command == "forms" or command == "form":
        async for item in showcase_forms():
            yield item
    elif command == "media":
        async for item in showcase_media():
            yield item
    elif command == "maps" or command == "map":
        async for item in showcase_maps():
            yield item
    elif command == "calendar":
        async for item in showcase_calendar():
            yield item
    elif command == "tables" or command == "table":
        async for item in showcase_tables():
            yield item
    elif command == "interactive":
        async for item in showcase_interactive():
            yield item
    elif command == "streaming":
        async for item in showcase_streaming():
            yield item
    elif "help" in command:
        async for item in show_help():
            yield item
    else:
        async for item in handle_general_query(message):
            yield item

async def showcase_all_features():
    """Showcase all available features"""
    yield bt.Markdown("# 🚀 Complete BubbleTea Features Showcase")
    yield bt.Text("Here's everything you can do with BubbleTea:")
    
    # Navigation pills
    yield bt.Pills(pills=[
        bt.Pill(text="📝 Components", action="components"),
        bt.Pill(text="📊 Charts", action="charts"),
        bt.Pill(text="📋 Forms", action="forms"),
        bt.Pill(text="🎵 Media", action="media"),
        bt.Pill(text="🗺️ Maps", action="maps"),
        bt.Pill(text="📅 Calendar", action="calendar"),
        bt.Pill(text="📊 Tables", action="tables"),
        bt.Pill(text="🎮 Interactive", action="interactive"),
    ])
    
    # Feature overview cards
    yield bt.Card(
        title="📝 Text & Markdown",
        text="Rich text formatting with full Markdown support",
        markdown=bt.Markdown("*Supports* **bold**, `code`, and [links](https://example.com)")
    )
    
    yield bt.Card(
        title="🖼️ Images & Media",
        text="Display images, videos, and audio content",
        image=bt.Image(
            url="https://picsum.photos/400/200",
            alt="Demo image"
        )
    )
    
    yield bt.Card(
        title="📊 Data Visualization",
        text="Charts, graphs, and interactive visualizations",
        markdown=bt.Markdown("Support for bar charts, line graphs, pie charts, and more!")
    )

async def showcase_components():
    """Showcase basic components"""
    yield bt.Markdown("## 📝 Basic Components")
    
    # Text variations
    yield bt.Text("🔤 Plain text component")
    yield bt.Markdown("**📝 Markdown** with *formatting* and `code`")
    yield bt.Text("💬 Multi-line text\nwith line breaks\nand emojis! 🎉")
    
    # Pills (buttons)
    yield bt.Text("🏷️ Interactive Pills:")
    yield bt.Pills(pills=[
        bt.Pill(text="Primary", variant="primary"),
        bt.Pill(text="Secondary", variant="secondary"),
        bt.Pill(text="Success", variant="success"),
        bt.Pill(text="Warning", variant="warning"),
        bt.Pill(text="Danger", variant="danger"),
    ])
    
    # Images
    yield bt.Text("🖼️ Image Display:")
    yield bt.Image(
        url="https://picsum.photos/seed/demo/600/300",
        alt="Demo landscape image",
        caption="Random landscape image"
    )
    
    # Cards
    yield bt.Text("🃏 Card Components:")
    yield bt.Card(
        title="Feature Card",
        text="Cards can contain multiple types of content",
        image=bt.Image(url="https://picsum.photos/seed/card/300/200", alt="Card image"),
        markdown=bt.Markdown("With **markdown** support too!")
    )

async def showcase_charts():
    """Showcase chart components"""
    yield bt.Markdown("## 📊 Data Visualization")
    
    # Bar Chart
    yield bt.Text("📊 Bar Chart Example:")
    yield bt.Chart(
        type="bar",
        data={
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
            "datasets": [{
                "label": "Sales ($)",
                "data": [12000, 19000, 8000, 15000, 20000, 18000],
                "backgroundColor": "rgba(54, 162, 235, 0.5)",
                "borderColor": "rgba(54, 162, 235, 1)",
                "borderWidth": 1
            }]
        },
        options={
            "responsive": True,
            "scales": {
                "y": {"beginAtZero": True}
            }
        }
    )
    
    # Line Chart
    yield bt.Text("📈 Line Chart Example:")
    yield bt.Chart(
        type="line",
        data={
            "labels": ["Q1", "Q2", "Q3", "Q4"],
            "datasets": [{
                "label": "Growth %",
                "data": [5, 12, 8, 15],
                "borderColor": "rgba(255, 99, 132, 1)",
                "backgroundColor": "rgba(255, 99, 132, 0.1)",
                "fill": True
            }]
        }
    )
    
    # Pie Chart
    yield bt.Text("🥧 Pie Chart Example:")
    yield bt.Chart(
        type="pie",
        data={
            "labels": ["Desktop", "Mobile", "Tablet"],
            "datasets": [{
                "data": [60, 35, 5],
                "backgroundColor": [
                    "rgba(255, 99, 132, 0.8)",
                    "rgba(54, 162, 235, 0.8)",
                    "rgba(255, 205, 86, 0.8)"
                ]
            }]
        }
    )

async def showcase_forms():
    """Showcase form components"""
    yield bt.Markdown("## 📋 Forms & Input")
    
    # Text Input
    yield bt.Input(
        type="text",
        placeholder="Enter your name...",
        label="Full Name",
        required=True
    )
    
    # Email Input
    yield bt.Input(
        type="email",
        placeholder="user@example.com",
        label="Email Address",
        required=True
    )
    
    # Number Input
    yield bt.Input(
        type="number",
        placeholder="25",
        label="Age",
        min_value=1,
        max_value=120
    )
    
    # Select Dropdown
    yield bt.Select(
        label="Favorite Color",
        options=[
            {"value": "red", "label": "Red"},
            {"value": "blue", "label": "Blue"},
            {"value": "green", "label": "Green"},
            {"value": "yellow", "label": "Yellow"}
        ],
        placeholder="Choose a color..."
    )
    
    # Checkbox
    yield bt.Checkbox(
        label="I agree to the terms and conditions",
        required=True
    )
    
    # Radio buttons
    yield bt.Radio(
        label="Subscription Plan",
        options=[
            {"value": "basic", "label": "Basic ($9/month)"},
            {"value": "pro", "label": "Pro ($19/month)"},
            {"value": "enterprise", "label": "Enterprise ($49/month)"}
        ],
        required=True
    )
    
    # Textarea
    yield bt.Textarea(
        placeholder="Tell us about yourself...",
        label="Bio",
        rows=4
    )
    
    # Date Input
    yield bt.Input(
        type="date",
        label="Date of Birth"
    )
    
    # Submit Button
    yield bt.Button(
        text="Submit Form",
        variant="primary",
        action="submit_form"
    )

async def showcase_media():
    """Showcase media components"""
    yield bt.Markdown("## 🎵 Media Components")
    
    # Audio
    yield bt.Text("🎵 Audio Player:")
    yield bt.Audio(
        url="https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
        title="Sample Audio",
        controls=True,
        autoplay=False
    )
    
    # Video
    yield bt.Text("🎬 Video Player:")
    yield bt.Video(
        url="https://sample-videos.com/zip/10/mp4/SampleVideo_1280x720_1mb.mp4",
        title="Sample Video",
        controls=True,
        autoplay=False,
        width=400,
        height=300
    )
    
    # File Upload
    yield bt.Text("📁 File Upload:")
    yield bt.FileUpload(
        accept=".pdf,.doc,.docx,.txt,.jpg,.png",
        multiple=True,
        max_size_mb=10,
        label="Upload Documents"
    )

async def showcase_maps():
    """Showcase map components"""
    yield bt.Markdown("## 🗺️ Maps & Location")
    
    # Basic Map
    yield bt.Text("🗺️ Interactive Map:")
    yield bt.Map(
        center={"lat": 40.7128, "lng": -74.0060},  # New York City
        zoom=12,
        markers=[
            {
                "lat": 40.7128,
                "lng": -74.0060,
                "title": "New York City",
                "description": "The Big Apple"
            },
            {
                "lat": 40.7589,
                "lng": -73.9851,
                "title": "Times Square",
                "description": "The Crossroads of the World"
            }
        ]
    )
    
    # Location Request
    yield bt.Text("📍 Request User Location:")
    yield bt.LocationRequest(
        message="Share your location to find nearby restaurants",
        button_text="Share Location"
    )

async def showcase_calendar():
    """Showcase calendar components"""
    yield bt.Markdown("## 📅 Calendar & Events")
    
    # Calendar
    yield bt.Text("📅 Interactive Calendar:")
    yield bt.Calendar(
        events=[
            {
                "title": "Team Meeting",
                "date": "2025-07-15",
                "time": "10:00 AM",
                "description": "Weekly team sync"
            },
            {
                "title": "Project Deadline",
                "date": "2025-07-20",
                "time": "11:59 PM",
                "description": "Final submission"
            },
            {
                "title": "Client Presentation",
                "date": "2025-07-25",
                "time": "2:00 PM",
                "description": "Q3 results presentation"
            }
        ],
        view="month",
        selectable=True
    )
    
    # Date Picker
    yield bt.Text("📆 Date Selection:")
    yield bt.DatePicker(
        label="Select Event Date",
        min_date="2025-07-10",
        max_date="2025-12-31"
    )

async def showcase_tables():
    """Showcase table components"""
    yield bt.Markdown("## 📊 Tables & Lists")
    
    # Basic Table
    yield bt.Text("📋 Data Table:")
    yield bt.Table(
        columns=[
            {"key": "name", "label": "Name", "sortable": True},
            {"key": "age", "label": "Age", "sortable": True},
            {"key": "city", "label": "City", "sortable": True},
            {"key": "salary", "label": "Salary", "sortable": True}
        ],
        data=[
            {"name": "Alice Johnson", "age": 28, "city": "New York", "salary": "$75,000"},
            {"name": "Bob Smith", "age": 34, "city": "San Francisco", "salary": "$95,000"},
            {"name": "Carol Davis", "age": 26, "city": "Chicago", "salary": "$68,000"},
            {"name": "David Wilson", "age": 31, "city": "Boston", "salary": "$82,000"}
        ],
        searchable=True,
        paginated=True,
        page_size=10
    )
    
    # List
    yield bt.Text("📝 Formatted List:")
    yield bt.List(
        items=[
            {"text": "Complete project proposal", "checked": True},
            {"text": "Review code changes", "checked": False},
            {"text": "Update documentation", "checked": False},
            {"text": "Schedule team meeting", "checked": True}
        ],
        ordered=False,
        checkable=True
    )

async def showcase_interactive():
    """Showcase interactive components"""
    yield bt.Markdown("## 🎮 Interactive Components")
    
    # Progress Bar
    yield bt.Text("⏳ Progress Indicator:")
    yield bt.Progress(
        value=65,
        max_value=100,
        label="Upload Progress",
        show_percentage=True
    )
    
    # Rating
    yield bt.Text("⭐ Rating Component:")
    yield bt.Rating(
        value=4.5,
        max_rating=5,
        label="Rate this experience",
        interactive=True
    )
    
    # Slider
    yield bt.Text("🎚️ Slider Input:")
    yield bt.Slider(
        min_value=0,
        max_value=100,
        value=50,
        step=5,
        label="Volume Level"
    )
    
    # Toggle Switch
    yield bt.Text("🔄 Toggle Switch:")
    yield bt.Toggle(
        label="Enable notifications",
        checked=True
    )
    
    # Action Buttons
    yield bt.Text("🎯 Action Buttons:")
    yield bt.ButtonGroup(
        buttons=[
            bt.Button(text="👍 Like", action="like", variant="success"),
            bt.Button(text="💬 Comment", action="comment", variant="primary"),
            bt.Button(text="📤 Share", action="share", variant="secondary"),
            bt.Button(text="🔖 Save", action="save", variant="outline")
        ]
    )

async def showcase_streaming():
    """Showcase streaming content"""
    yield bt.Markdown("## 🌊 Streaming Content")
    yield bt.Text("Watch this content stream in real-time:")
    
    # Simulate streaming data
    for i in range(5):
        await asyncio.sleep(0.5)  # Simulate processing time
        yield bt.Text(f"📊 Processing step {i+1}/5... {'▓' * (i+1)}{'░' * (4-i)}")
    
    yield bt.Text("✅ Streaming complete!")
    
    # Live updating chart
    yield bt.Text("📈 Live Chart Update:")
    for i in range(3):
        await asyncio.sleep(1)
        yield bt.Chart(
            type="line",
            data={
                "labels": [f"T{j}" for j in range(i+3)],
                "datasets": [{
                    "label": f"Real-time Data (Update {i+1})",
                    "data": [j*2 + i*3 for j in range(i+3)],
                    "borderColor": f"rgba({50+i*50}, 162, 235, 1)",
                    "backgroundColor": f"rgba({50+i*50}, 162, 235, 0.1)"
                }]
            }
        )

async def show_help():
    """Show help information"""
    yield bt.Markdown("## 🆘 Help & Commands")
    yield bt.Text("Available commands:")
    
    yield bt.Pills(pills=[
        bt.Pill(text="showcase - Show all features"),
        bt.Pill(text="components - Basic components"),
        bt.Pill(text="charts - Data visualization"),
        bt.Pill(text="forms - Input forms"),
        bt.Pill(text="media - Audio/video"),
        bt.Pill(text="maps - Location features"),
        bt.Pill(text="calendar - Date/time"),
        bt.Pill(text="tables - Data tables"),
        bt.Pill(text="interactive - Interactive UI"),
        bt.Pill(text="streaming - Real-time updates"),
    ])

async def handle_general_query(message: str):
    """Handle general queries"""
    yield bt.Text(f"💬 You said: {message}")
    yield bt.Markdown("I'm a demo bot showcasing all BubbleTea features!")
    yield bt.Text("Try these commands:")
    yield bt.Pills(pills=[
        bt.Pill(text="showcase", action="showcase"),
        bt.Pill(text="components", action="components"),
        bt.Pill(text="charts", action="charts"),
        bt.Pill(text="help", action="help"),
    ])
    
    # Echo with rich formatting
    yield bt.Card(
        title="Your Message",
        text=message,
        markdown=bt.Markdown(f"**Received at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    )
    
    yield bt.Done()

if __name__ == "__main__":
    # Run the comprehensive demo server
    bt.run_server(demo_bot, port=8030)