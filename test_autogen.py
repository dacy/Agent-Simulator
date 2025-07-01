#!/usr/bin/env python3
"""
Simple test script to verify AutoGen functionality
"""

import json
import os

try:
    print("Testing AutoGen imports...")
    
    # Test basic imports
    from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
    print("✓ Agent imports successful")
    
    from autogen_agentchat.teams import SelectorGroupChat
    print("✓ Team imports successful")
    
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    print("✓ Model client imports successful")
    
    from autogen_agentchat.conditions import TextMentionTermination
    print("✓ Termination conditions imports successful")
    
    from autogen_core.model_context import UnboundedChatCompletionContext
    print("✓ Model context imports successful")
    
    from autogen_core.tools import FunctionTool
    print("✓ Tools imports successful")
    
    print("\n🎉 All AutoGen imports successful!")
    
    # Test basic team creation
    print("\nTesting basic team creation...")
    
    # Create model client
    model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
    print("✓ Model client created")
    
    # Create simple agent
    agent = AssistantAgent(
        name="test_agent",
        description="A test agent",
        model_client=model_client,
        system_message="You are a test agent."
    )
    print("✓ Agent created")
    
    # Create team
    team = SelectorGroupChat(
        participants=[agent],
        model_client=model_client,
        termination_condition=TextMentionTermination(text="TERMINATE")
    )
    print("✓ Team created")
    
    # Test dump_component
    config = team.dump_component()
    print("✓ Config dumped")
    
    # Test JSON export
    config_json = config.model_dump_json(indent=2)
    print("✓ JSON serialization successful")
    
    # Write to file
    with open("test_config.json", 'w', encoding='utf-8') as f:
        f.write(config_json)
    print("✓ JSON file written")
    
    print(f"\n✅ Test completed successfully!")
    print(f"Generated config file size: {len(config_json)} characters")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc() 