"""
Thread support example for LLM with conversation memory
"""

import bubbletea_chat as bt
from bubbletea_chat import LLM, Text, Markdown


@bt.chatbot(stream=False)
async def thread_bot(message: str, **kwargs):
    """
    Bot that uses OpenAI Assistant API with thread support for conversation memory
    
    Requires: OPENAI_API_KEY environment variable
    """
    components = []
    
    # Get user context
    user_uuid = kwargs.get('user_uuid')
    thread_id = kwargs.get('thread_id')
    
    # Initialize LLM with assistant
    llm = LLM(
        model="gpt-4",
        assistant_id=None,  # Will create a new assistant if not provided
        temperature=0.7
    )
    
    # Create or get thread for this user
    if not thread_id and user_uuid:
        thread_id = llm.create_thread(user_uuid)
        if thread_id:
            components.append(Text(f"Started new conversation thread!"))
    
    if not thread_id:
        # Fallback to stateless if no thread
        components.append(Text("No thread ID available, responding without conversation memory."))
        response = await llm.acomplete(message)
        components.append(Markdown(response))
        return components
    
    # Add user message to thread
    success = llm.add_user_message(thread_id, message)
    if not success:
        components.append(Text("Failed to add message to thread"))
        return components
    
    components.append(Text("Processing with conversation memory..."))
    
    # Get assistant response with full thread context
    response = llm.get_assistant_response(thread_id, message)
    
    if response:
        components.append(Markdown(response))
        components.append(Text(f"Thread ID: {thread_id[:8]}... (conversation preserved)"))
    else:
        components.append(Text("Failed to get response from assistant"))
    
    return components


@bt.chatbot(stream=False)
async def advanced_thread_bot(message: str, **kwargs):
    """
    Advanced bot with custom assistant configuration and thread management
    """
    components = []
    user_uuid = kwargs.get('user_uuid')
    thread_id = kwargs.get('thread_id')
    
    # Initialize with custom assistant configuration
    llm = LLM(
        model="gpt-4",
        llm_provider="openai",
        temperature=0.5
    )
    
    # Initialize assistant with custom instructions
    if not llm.assistant_id:
        llm._initialize_assistant(
            name="BubbleTea Assistant",
            instructions="""You are a helpful AI assistant with perfect memory. 
            Remember all previous messages in our conversation and reference them when relevant.
            Be concise but friendly.""",
            tools=[{"type": "code_interpreter"}]  # Enable code interpreter
        )
    
    # Thread management
    if not thread_id and user_uuid:
        thread_id = llm.create_thread(user_uuid)
        components.append(Markdown("### 🧵 New Conversation Thread Started"))
    elif thread_id:
        components.append(Text("Continuing conversation..."))
    
    if thread_id:
        # Use thread for conversation
        success = llm.add_user_message(thread_id, message)
        if success:
            response = llm.get_assistant_response(thread_id, message)
            if response:
                components.append(Markdown(response))
                components.append(Text(f"💾 Context preserved in thread: {thread_id[:8]}..."))
            else:
                components.append(Text("Error getting response from assistant"))
        else:
            components.append(Text("Error adding message to thread"))
    else:
        # Fallback to regular completion
        components.append(Text("Using stateless mode (no thread ID)"))
        response = await llm.acomplete(message)
        components.append(Text(response))
    
    return components


if __name__ == "__main__":
    bt.run_server(thread_bot, port=8010)