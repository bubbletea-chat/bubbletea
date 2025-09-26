import bubbletea_chat as bt
import os
from datetime import datetime
from typing import Any, Dict

from dotenv import load_dotenv

load_dotenv()

# Use absolute imports for Google Cloud deployment compatibility
from core.onboarding_manager import OnboardingManager
from core.scheduler import Scheduler
from core.user_preferences import UserPreferences
from services.news_service import NewsService
from services.weather_service import WeatherService
from storage.storage_adapter import StorageAdapter


async def handler(input_data: Dict[str, Any]) -> bt.Component:
    """
    Main handler for Morning Brief Bot interactions

    Args:
        input_data: Input data containing user message and context

    Returns:
        BubbleTea component with bot response
    """
    try:
        # Extract conversation UUID and user input
        conversation_uuid = input_data.get("conversationUuid", "")
        user_message = input_data.get("userInput", "").strip().lower()

        if not conversation_uuid:
            return bt.Markdown("❌ Unable to identify conversation. Please try again.")

        # Initialize services
        user_prefs = UserPreferences(conversation_uuid)
        onboarding_manager = OnboardingManager(conversation_uuid)
        scheduler = Scheduler()

        # Check if user needs onboarding
        if not onboarding_manager.is_user_onboarded() and user_message not in ["skip", "cancel"]:
            return await handle_onboarding(onboarding_manager, user_message, input_data)

        # Handle different user commands
        if user_message in ["help", "commands"]:
            return get_help_menu()

        elif user_message in ["brief", "morning brief", "today"]:
            return await generate_morning_brief(user_prefs)

        elif user_message in ["settings", "preferences", "config"]:
            return get_settings_menu(user_prefs)

        elif user_message.startswith("set "):
            return await handle_setting_update(user_message, user_prefs)

        elif user_message in ["schedule", "notifications"]:
            return handle_schedule_management(scheduler, conversation_uuid, user_prefs)

        elif user_message in ["history", "past briefs"]:
            return get_brief_history(conversation_uuid)

        elif user_message in ["reset", "restart setup"]:
            return handle_reset(onboarding_manager)

        elif user_message in ["status", "info"]:
            return get_user_status(user_prefs, onboarding_manager)

        else:
            # Default response with suggestions
            return get_default_response()

    except Exception as e:
        return bt.Markdown("❌ An error occurred. Please try again or type 'help' for assistance.")


async def handle_onboarding(
    onboarding_manager: OnboardingManager, user_message: str, input_data: Dict[str, Any]
) -> bt.Component:
    """Handle onboarding flow"""

    # Start onboarding if user hasn't started yet
    if user_message in ["start", "begin", "setup", ""]:
        return onboarding_manager.start_onboarding()

    # Handle step-by-step onboarding based on progress
    status = onboarding_manager.get_onboarding_status()

    if "location" in status["remaining_steps"]:
        if user_message and len(user_message) > 2:
            # Process location input
            response = onboarding_manager.process_location(user_message)
            # Check if we should continue to next step
            if "✅" in str(response):
                return bt.Markdown(str(response) + "\n\n" + str(onboarding_manager.get_timezone_setup()))
            return response
        else:
            return onboarding_manager.get_location_setup()

    elif "timezone" in status["remaining_steps"]:
        if user_message in [
            "utc",
            "america/new_york",
            "america/los_angeles",
            "america/chicago",
            "europe/london",
            "europe/paris",
            "asia/tokyo",
            "asia/shanghai",
            "australia/sydney",
        ]:
            response = onboarding_manager.process_timezone(user_message.replace("_", "/").title())
            return bt.Markdown(str(response) + "\n\n" + str(onboarding_manager.get_news_preferences_setup()))
        else:
            return onboarding_manager.get_timezone_setup()

    # Continue with other onboarding steps...
    return onboarding_manager.complete_onboarding()


async def generate_morning_brief(user_prefs: UserPreferences) -> bt.Component:
    """Generate and return morning brief"""
    try:
        conversation_uuid = user_prefs.conversation_uuid

        # Get user preferences
        location = user_prefs.get_weather_location()
        categories = user_prefs.get_news_categories()
        sections = user_prefs.get_brief_sections()

        brief_parts = []
        brief_parts.append("# 🌅 Good Morning!")
        brief_parts.append(f"Here's your personalized brief for {datetime.now().strftime('%A, %B %d, %Y')}:")

        # Add weather section if enabled and location is set
        if sections.get("weather", True) and location:
            weather_service = WeatherService()
            weather = weather_service.get_weather_forecast(location)
            if weather:
                brief_parts.append(f"\n## 🌤️ Weather for {location}")
                brief_parts.append(weather)
            else:
                brief_parts.append(f"\n## 🌤️ Weather for {location}")
                brief_parts.append("Weather information temporarily unavailable.")

        # Add news section if enabled
        if sections.get("news", True):
            news_service = NewsService()
            news = news_service.get_news_headlines(categories)
            if news:
                brief_parts.append("\n## 📰 News Headlines")
                brief_parts.append(news)
            else:
                brief_parts.append("\n## 📰 News Headlines")
                brief_parts.append("News updates temporarily unavailable.")

        # Add motivational quote if enabled
        if sections.get("motivational_quote", False):
            brief_parts.append("\n## ✨ Daily Inspiration")
            brief_parts.append('_"The way to get started is to quit talking and begin doing."_ - Walt Disney')

        # Store the brief
        storage = StorageAdapter()
        brief_content = "\n".join(brief_parts)
        storage.store_morning_brief(conversation_uuid, brief_content)

        return bt.Markdown(brief_content)

    except Exception as e:
        return bt.Markdown("❌ Unable to generate morning brief. Please check your settings and try again.")


def get_help_menu() -> bt.Component:
    """Return help menu with available commands"""
    return bt.Markdown(
        """# 🤖 Morning Brief Bot - Help

## Available Commands:

### 📋 **Brief Commands**
- `brief` or `today` - Get your personalized morning brief
- `history` - View past morning briefs

### ⚙️ **Settings Commands**
- `settings` - View and modify your preferences
- `schedule` - Manage notification scheduling
- `set location [city]` - Update your location
- `set timezone [timezone]` - Update your timezone

### 🔧 **Setup Commands**
- `reset` - Restart the setup process
- `status` - View your current configuration
- `help` - Show this help menu

### 📝 **Quick Setup**
If you haven't completed setup yet, just start typing your location and I'll guide you through the process!

**Example**: "New York, NY" or "London, UK"

---
*Type any command to get started!*"""
    )


def get_settings_menu(user_prefs: UserPreferences) -> bt.Component:
    """Return current settings and options to modify them"""
    prefs = user_prefs.get_all_preferences()

    location = prefs.get("weather_location", "Not set")
    timezone = prefs.get("timezone", "UTC")
    categories = ", ".join(prefs.get("news_categories", ["general"]))
    brief_time = prefs.get("brief_time", "08:00")
    notifications = "Enabled" if prefs.get("notifications_enabled", True) else "Disabled"

    return bt.Markdown(
        f"""# ⚙️ Your Settings

## Current Configuration:
📍 **Location**: {location}
🕐 **Timezone**: {timezone}
📰 **News Categories**: {categories}
⏰ **Brief Time**: {brief_time}
🔔 **Notifications**: {notifications}

## Quick Updates:
- `set location [city, country]` - Update location
- `set timezone [timezone]` - Update timezone
- `set time [HH:MM]` - Update brief time
- `set notifications on/off` - Toggle notifications

**Example**: `set location San Francisco, CA`

Type `reset` to restart the full setup process."""
    )


async def handle_setting_update(user_message: str, user_prefs: UserPreferences) -> bt.Component:
    """Handle setting updates from user commands"""
    parts = user_message.split(" ", 2)

    if len(parts) < 3:
        return bt.Markdown("❌ Please provide both setting and value. Example: `set location New York, NY`")

    setting = parts[1].lower()
    value = parts[2]

    if setting == "location":
        success = user_prefs.set_weather_location(value)
        if success:
            return bt.Markdown(f"✅ Location updated to **{value}**")
        else:
            return bt.Markdown("❌ Failed to update location. Please try again.")

    elif setting == "timezone":
        success = user_prefs.set_timezone(value)
        if success:
            return bt.Markdown(f"✅ Timezone updated to **{value}**")
        else:
            return bt.Markdown("❌ Failed to update timezone. Please try again.")

    elif setting == "time":
        success = user_prefs.set_brief_time(value)
        if success:
            return bt.Markdown(f"✅ Brief time updated to **{value}**")
        else:
            return bt.Markdown("❌ Failed to update time. Please use HH:MM format.")

    elif setting == "notifications":
        enabled = value.lower() in ["on", "true", "enabled", "yes"]
        success = user_prefs.set_notifications_enabled(enabled)
        status = "enabled" if enabled else "disabled"
        if success:
            return bt.Markdown(f"✅ Notifications **{status}**")
        else:
            return bt.Markdown("❌ Failed to update notification settings.")

    else:
        return bt.Markdown(f"❌ Unknown setting '{setting}'. Available: location, timezone, time, notifications")


def handle_schedule_management(
    scheduler: Scheduler, conversation_uuid: str, user_prefs: UserPreferences
) -> bt.Component:
    """Handle schedule management commands"""
    notifications_enabled = user_prefs.get_notifications_enabled()
    is_scheduled = scheduler.is_scheduled(conversation_uuid)
    brief_time = user_prefs.get_brief_time().strftime("%H:%M")

    status = "Active" if is_scheduled and notifications_enabled else "Inactive"

    return bt.Markdown(
        f"""# 📅 Schedule Management

## Current Status: **{status}**

### Settings:
- **Brief Time**: {brief_time}
- **Notifications**: {'Enabled' if notifications_enabled else 'Disabled'}
- **Scheduled**: {'Yes' if is_scheduled else 'No'}

### Commands:
- `set time [HH:MM]` - Change brief time
- `set notifications on/off` - Enable/disable notifications

**Note**: Schedules automatically update when you change your preferences."""
    )


def get_brief_history(conversation_uuid: str) -> bt.Component:
    """Get user's brief history"""
    storage = StorageAdapter()
    briefs = storage.get_recent_morning_briefs(conversation_uuid, limit=5)

    if not briefs:
        return bt.Markdown("📭 No morning briefs in your history yet. Type `brief` to get your first one!")

    history_text = "# 📚 Your Recent Morning Briefs\n\n"

    for i, brief in enumerate(briefs, 1):
        date = brief.get("brief_date", "Unknown date")
        content_preview = brief.get("brief_content", "")[:100] + "..."
        history_text += f"## {i}. {date}\n{content_preview}\n\n"

    return bt.Markdown(history_text)


def handle_reset(onboarding_manager: OnboardingManager) -> bt.Component:
    """Handle reset/restart setup"""
    success = onboarding_manager.reset_onboarding()

    if success:
        return bt.Markdown(
            """# 🔄 Settings Reset

Your preferences have been reset. Let's set you up again!

Please provide your location to get started (e.g., "New York, NY")"""
        )
    else:
        return bt.Markdown("❌ Failed to reset settings. Please try again.")


def get_user_status(user_prefs: UserPreferences, onboarding_manager: OnboardingManager) -> bt.Component:
    """Get user status and configuration summary"""
    is_onboarded = onboarding_manager.is_user_onboarded()
    prefs = user_prefs.get_all_preferences()

    if not is_onboarded:
        return bt.Markdown("# ⚠️ Setup Incomplete\n\nPlease complete your setup by providing your location.")

    location = prefs.get("weather_location", "Not set")
    timezone = prefs.get("timezone", "UTC")
    categories = ", ".join(prefs.get("news_categories", ["general"]))

    return bt.Markdown(
        f"""# ℹ️ Your Status

## Setup: **Complete** ✅

## Configuration:
- **Location**: {location}
- **Timezone**: {timezone}
- **News Categories**: {categories}
- **Notifications**: {'Enabled' if prefs.get('notifications_enabled', True) else 'Disabled'}

Type `brief` for your morning update or `settings` to make changes."""
    )


def get_default_response() -> bt.Component:
    """Default response when user input doesn't match commands"""
    return bt.Markdown(
        """# 👋 Hello!

I'm your Morning Brief Bot. Here's what I can help you with:

🌅 **Get Brief** - Type `brief` for your personalized morning update
⚙️ **Settings** - Type `settings` to view or update your preferences
📋 **Help** - Type `help` to see all available commands

**Getting Started**: If you haven't set up yet, just tell me your location (e.g., "New York, NY") and I'll guide you through the setup!"""
    )




@bt.chatbot("morning-bot")
async def morning_brief_bot(message: str, user_uuid: str = None, conversation_uuid: str = None) -> bt.Component:
    """Main bot handler"""
    return await handler({"conversationUuid": conversation_uuid, "userInput": message})


@morning_brief_bot.config
def get_config():
    return bt.BotConfig(
        name="morning-brief-bot",
        url=os.getenv("BOT_URL", "http://localhost:5000"),
        is_streaming=False,
        icon_url="https://iafqwfegdftjthhbccyt.supabase.co/storage/v1/object/sign/bubble-tea/good_morning_logo.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV81MDMyMzM5NS1hZDExLTRkYzEtODdkNC0yMjMwM2JkNjBhMzEiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJidWJibGUtdGVhL2dvb2RfbW9ybmluZ19sb2dvLmpwZyIsImlhdCI6MTc1NDA1MjkyMCwiZXhwIjoxNzg1NTg4OTIwfQ.9WU4AmRQ7xY5k05Rkq0dtAJYjOHyJ1d5E8yCW2N31xc",
        emoji="🌅",
        initial_text="🌅 Morning Brief Bot - Type 'start' to setup!",
    )


if __name__ == "__main__":
    bt.run_server(morning_brief_bot, port=8080, host="0.0.0.0")
