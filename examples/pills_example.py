"""
Example bot demonstrating the use of Pills components in BubbleTea.
This bot shows various ways to use pills for interactive options.
"""

import bubbletea as bt

@bt.config()
def get_config():
    return bt.BotConfig(
        name="Pills Example Bot",
        url="http://localhost:8004",
        is_streaming=False,
        initial_text="Hello! I can show you different pill interfaces. Try asking me about:\n• Food preferences\n• Travel destinations\n• Programming languages\n• Or just say 'show me pills'"
    )

@bt.chatbot()
def pills_bot(message: str) -> list:
    message_lower = message.lower()
    
    # Food preferences
    if "food" in message_lower or "eat" in message_lower or "cuisine" in message_lower:
        return [
            bt.Text("What type of cuisine do you prefer?"),
            bt.Pill("Italian"),
            bt.Pill("Japanese"),
            bt.Pill("Mexican"),
            bt.Pill("Indian"),
            bt.Pill("Spanish"),
            bt.Pill("American")
        ]
    
    # Travel destinations
    elif "travel" in message_lower or "destination" in message_lower or "vacation" in message_lower:
        return [
            bt.Text("Where would you like to travel?"),
            bt.Pill("Paris"),
            bt.Pill("New York"),
            bt.Pill("Tokyo"),
            bt.Pill("San Francisco"),
            bt.Pill("Rome"),
            bt.Pill("Bali")
        ]
    
    # Programming languages
    elif "programming" in message_lower or "language" in message_lower or "code" in message_lower:
        return [
            bt.Text("Which programming languages are you interested in?"),
            bt.Pill("Python"),
            bt.Pill("Java"),
            bt.Pill("JavaScript"),
            bt.Pill("Rust"),
            bt.Pill("TypeScript"),
            bt.Pill("Ruby"),
            bt.Pill("Go"),
            bt.Pill("Swift")
        ]
    
    # Status pills
    elif "status" in message_lower:
        return [
            bt.Text("Select a status:"),
            bt.Pill("Active"),
            bt.Pill("Pending"),
            bt.Pill("Completed"),
            bt.Pill("Archived"),
            bt.Pill("Draft"),
            bt.Pill("Published")
        ]
    
    # Options pills
    elif "options" in message_lower or "choice" in message_lower:
        return [
            bt.Text("Please select an option:"),
            bt.Pill("Option A"),
            bt.Pill("Option B"),
            bt.Pill("Option C"),
            bt.Pill("Choice 1"),
            bt.Pill("Choice 2"),
            bt.Pill("Choice 3")
        ]
    
    # Priority selection
    elif "priority" in message_lower or "importance" in message_lower:
        return [
            bt.Markdown("## Choose your priority level"),
            bt.Text("Select one or more priorities:"),
            bt.Pill("High Priority"),
            bt.Pill("Medium Priority"),
            bt.Pill("Low Priority"),
            bt.Markdown("*You can select multiple pills by clicking on them*")
        ]
    
    # Default: show all pill types
    else:
        return [
            bt.Text("Here are some example pills:"),
            bt.Markdown("### Task Status:"),
            bt.Pill("Complete"),
            bt.Pill("In Progress"),
            bt.Pill("Paused"),
            bt.Pill("Cancelled"),
            bt.Markdown("### Quick Responses:"),
            bt.Pill("Yes"),
            bt.Pill("No"),
            bt.Pill("Maybe"),
            bt.Pill("Ask Later"),
            bt.Text("\nTry asking me about food, travel, programming languages, or priorities!")
        ]

if __name__ == "__main__":
    bt.run_server(pills_bot, port=8004)