"""
User Proxy Agent for the Benefit Orchestrator System.
Handles user interactions and input collection.
"""

from autogen_agentchat.agents import UserProxyAgent


def create_user_proxy_agent():
    """Create the User Proxy Agent."""
    
    return UserProxyAgent(
        name="User_Proxy_agent",
        description="Handles user questions, uploads, and final approval"
    ) 