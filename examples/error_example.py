#!/usr/bin/env python3
"""
Example demonstrating the Error component in BubbleTea
"""

from bubbletea_chat import Text, Error, chatbot

@chatbot
def error_bot(text: str):
    """A bot that demonstrates error handling"""
    
    if "fail" in text.lower():
        # Return an error when user mentions "fail"
        return Error(
            title="Request Failed",
            description="The requested operation could not be completed. Please try again later.",
            code="ERR_001",
        )
    
    if "connection" in text.lower():
        # Return a connection error
        return Error(
            title="Connection Error",
            description="Unable to establish connection to the service. Check your network settings.",
            code="ERR_CONN",
        )
    
    if "unauthorized" in text.lower():
        # Return an authorization error
        return Error(
            title="Unauthorized Access",
            description="You don't have permission to perform this action.",
            code="ERR_403",
        )
    
    # Normal response
    return Text("Hello! Try saying 'fail', 'connection', or 'unauthorized' to see error messages.")

if __name__ == "__main__":
    from bubbletea_chat import run_server
    run_server(port=8012)