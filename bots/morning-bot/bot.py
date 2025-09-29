import bubbletea_chat as bt
from bubbletea_chat.components import Text, Markdown
from core.user_preferences import UserPreferencesManager, OnboardingState
from core.onboarding_manager import OnboardingManager
from services.weather_service import WeatherService
from services.news_service import NewsService
from core.scheduler import MorningBriefScheduler


class MorningBriefBot:
    """Main bot class that handles all user interactions"""

    def __init__(self):
        # Initialize all services
        self.preferences_manager = UserPreferencesManager()
        self.onboarding_manager = OnboardingManager(self.preferences_manager)
        self.weather_service = WeatherService()
        self.news_service = NewsService()
        self.scheduler = MorningBriefScheduler(self.preferences_manager,
                                               self.weather_service,
                                               self.news_service)

        # Start the scheduler
        self.scheduler.start()

        # Define command handlers
        self.command_handlers = {
            'start': self._handle_start_command,
            'hi': self._handle_start_command,
            'help': self._handle_help_command,
            'update': self._handle_update_command,
            'preview': self._handle_preview_command,
            'morning': self._handle_morning_brief_command,
            'brief': self._handle_morning_brief_command,
            'generate': self._handle_generate_command,
            'status': self._handle_status_command
        }

    def handle_message(self,
                       message: str,
                       user_uuid: str = None,
                       conversation_uuid: str = None) -> list:
        """Handle incoming messages"""
        # Use conversation_uuid as primary identifier, fallback to user_uuid
        identifier = conversation_uuid or user_uuid

        # Return error if no identifier provided
        if not identifier:
            return [Text("Error: No user or conversation ID provided.")]

        # Update conversation UUID if provided
        if conversation_uuid:
            self._update_conversation_uuid_if_needed(identifier,
                                                     conversation_uuid)

        # Clean and process message
        message = message.strip()
        message_lower = message.lower()

        # Handle special message types
        if message.startswith("interest:"):
            return self._handle_interest_selection(message, identifier)
        elif message.startswith("action:"):
            return self._handle_action_pill(message, identifier)

        # Handle commands
        if message_lower in self.command_handlers:
            return self.command_handlers[message_lower](identifier,
                                                        conversation_uuid)

        # Handle onboarding if user is still in process
        current_state = self.preferences_manager.get_current_onboarding_state(
            identifier)
        if current_state != OnboardingState.COMPLETED:
            return self.onboarding_manager.get_onboarding_message(
                identifier, message)

        # Default response for unrecognized commands
        return self._get_default_response()

    def _update_conversation_uuid_if_needed(self, identifier: str,
                                            conversation_uuid: str):
        """Update conversation UUID for notifications if changed"""
        if conversation_uuid and identifier:
            user_prefs = self.preferences_manager.get_or_create_user(
                identifier)
            if user_prefs.conversation_uuid != conversation_uuid:
                self.preferences_manager.update_user_preferences(
                    identifier, conversation_uuid=conversation_uuid)

    def _handle_interest_selection(self, message: str,
                                   identifier: str) -> list:
        """Handle interest pill clicks"""
        interest = message.replace("interest:", "")
        current_state = self.preferences_manager.get_current_onboarding_state(
            identifier)

        if current_state == OnboardingState.ASKING_INTERESTS:
            user_prefs = self.preferences_manager.get_or_create_user(
                identifier)
            current_interests = user_prefs.news_interests or []

            # Toggle interest
            if interest in current_interests:
                current_interests.remove(interest)
            else:
                current_interests.append(interest)

            # Update preferences
            self.preferences_manager.update_user_preferences(
                identifier, news_interests=current_interests)

            return [Text(f"Topics: {', '.join(current_interests)}")]
        return []

    def _handle_action_pill(self, message: str, identifier: str) -> list:
        """Handle action pill clicks"""
        action = message.replace("action:", "")

        action_handlers = {
            "update": lambda: self._handle_update_command(identifier, None),
            "preview": lambda: self._handle_preview_command(identifier, None),
            "help": lambda: self._handle_help_command(identifier, None)
        }

        handler = action_handlers.get(action)
        return handler() if handler else []

    def _handle_start_command(self,
                              identifier: str,
                              conversation_uuid: str = None) -> list:
        """Handle start/setup commands"""
        if conversation_uuid:
            self._update_conversation_uuid_if_needed(identifier,
                                                     conversation_uuid)
        return self.onboarding_manager.get_onboarding_message(identifier)

    def _handle_help_command(self,
                             identifier: str,
                             conversation_uuid: str = None) -> list:
        """Handle help command"""
        return [
            Markdown("**Commands:**\n"
                     "• `start` - Setup\n"
                     "• `update` - Change settings\n"
                     "• `preview` - Sample brief\n"
                     "• `morning` - Today's brief\n"
                     "• `generate` - Test brief\n"
                     "• `status` - Your settings")
        ]

    def _handle_update_command(self,
                               identifier: str,
                               conversation_uuid: str = None) -> list:
        """Handle update/reset commands"""
        self.preferences_manager.reset_user_onboarding(identifier)
        return self.onboarding_manager.get_onboarding_message(identifier)

    def _handle_preview_command(self,
                                identifier: str,
                                conversation_uuid: str = None) -> list:
        """Handle preview command"""
        preview = self.scheduler.generate_preview(identifier)
        return [Markdown(preview)]

    def _handle_morning_brief_command(self,
                                      identifier: str,
                                      conversation_uuid: str = None) -> list:
        """Handle morning brief request"""
        brief = self.scheduler.get_user_brief(identifier)
        if brief:
            return [Markdown(brief)]
        return [Text("No brief yet. Type 'generate' to create one.")]

    def _handle_generate_command(self, identifier: str,
                                 conversation_uuid: str) -> list:
        """Handle manual brief generation"""
        result = self.scheduler.trigger_manual_brief(identifier,
                                                     conversation_uuid)
        return [Text(result)]

    def _handle_status_command(self,
                               identifier: str,
                               conversation_uuid: str = None) -> list:
        """Handle status/preferences command"""
        user_prefs = self.preferences_manager.get_or_create_user(identifier)
        return [
            Markdown("**Your Settings:**\n"
                     f"📍 {user_prefs.location}\n"
                     f"📰 {', '.join(user_prefs.news_interests)}\n"
                     f"⏰ {user_prefs.wake_time}")
        ]

    def _get_default_response(self) -> list:
        """Get default response for unrecognized commands"""
        return [Text("Type 'help' for commands.")]


# Create global bot instance
bot_instance = MorningBriefBot()


@bt.chatbot('morning-bot')
def morning_brief_bot(message: str,
                      user_uuid: str = None,
                      conversation_uuid: str = None) -> list:
    """Main bot handler"""
    return bot_instance.handle_message(message, user_uuid, conversation_uuid)


@morning_brief_bot.config
def get_config():
    return bt.BotConfig(
        name="morning-brief-bot",
        url="http://localhost:5000",
        is_streaming=False,
        icon_url=
        "https://iafqwfegdftjthhbccyt.supabase.co/storage/v1/object/sign/bubble-tea/good_morning_logo.jpg?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV81MDMyMzM5NS1hZDExLTRkYzEtODdkNC0yMjMwM2JkNjBhMzEiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJidWJibGUtdGVhL2dvb2RfbW9ybmluZ19sb2dvLmpwZyIsImlhdCI6MTc1NDA1MjkyMCwiZXhwIjoxNzg1NTg4OTIwfQ.9WU4AmRQ7xY5k05Rkq0dtAJYjOHyJ1d5E8yCW2N31xc",
        emoji="🌅",
        initial_text="🌅 Morning Brief Bot - Type 'start' to setup!")


if __name__ == "__main__":
    bt.run_server(morning_brief_bot, port=8080, host="0.0.0.0")
