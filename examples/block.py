"""
Block component example for BubbleTea
"""

import bubbletea_chat as bt
from bubbletea_chat import Block, Text, Markdown, Image


@bt.chatbot(stream=False)
def block_bot(message: str):
    """Bot demonstrating Block component for grouped content"""
    components = []
    
    if "help" in message.lower():
        # Create a help block with multiple components
        help_block = [
                Markdown("## 📚 Help Documentation"),
                Text("Here are the available commands:"),
                Markdown("""
- `status` - Check system status
- `profile` - View user profile
- `settings` - Configure settings
- `help` - Show this help message
                """),
                Text("For more information, visit our docs!"),
            ],
        components.append(help_block)
        
    elif "status" in message.lower():
        # Create a status block
        status_block = Block(
            components=[
                Markdown("## System Status"),
                Text("✅ All systems operational"),
                Markdown("""
| Service | Status | Uptime |
|---------|--------|--------|
| API | 🟢 Online | 99.9% |
| Database | 🟢 Online | 99.8% |
| Cache | 🟢 Online | 100% |
                """),
                Text("Last checked: Just now"),
            ],
            title="System Status",
            style="info"
        )
        components.append(status_block)
        
    elif "profile" in message.lower():
        # Create a profile block with image
        profile_block = [
                Image("https://picsum.photos/200/200", alt="Profile picture"),
                Markdown("## User Profile"),
                Text("Name: John Doe"),
                Text("Email: john@example.com"),
                Text("Member since: 2024"),
                Markdown("**Status:** Premium member"),
            ]
        components.append(profile_block)
        
    else:
        # Default response with multiple blocks
        components.append(
            components=[
                Text("Welcome to Block Bot!"),
                Text("I demonstrate how to use Block components to group related content."),
            ],
        )
        
        components.append(
            components=[
                Markdown("### Try these commands:"),
                Text("• Type 'help' for documentation"),
                Text("• Type 'status' for system status"),
                Text("• Type 'profile' for user profile"),
                Block(120)
            ],
        )
    
    return components


if __name__ == "__main__":
    bt.run_server(block_bot, port=8009)