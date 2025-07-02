#!/usr/bin/env python3
"""
Benefit Orchestrator Team Creation Script

This script creates a complete AutoGen team for processing military benefit requests
using a modular architecture with individual agent files.
"""

import json
import os
from typing import Dict, Any

# AutoGen imports
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_core.model_context import HeadAndTailChatCompletionContext
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Import individual agent creators
from agents.customer_verification_agent import create_customer_verification_agent
from agents.document_processing_agent import create_document_processing_agent
from agents.orchestrator_agent import create_orchestrator_agent
from agents.eligibility_decision_agent import create_eligibility_decision_agent
from agents.benefit_execution_agent import create_benefit_execution_agent
from agents.judge_agent import create_judge_agent
from agents.user_proxy_agent import create_user_proxy_agent



def create_benefit_orchestrator_team():
    """Create the complete benefit orchestrator team."""
    
    print("=== Benefit Orchestrator Team Creation ===\n")
    
    
    print("Creating model client...")
    
    # Set dummy API key for config generation if not already set
    # This allows the structured output model clients to work during JSON export
    if not os.getenv("OPENAI_API_KEY"):
        os.environ["OPENAI_API_KEY"] = "dummy-key-for-config-generation"
    
    # Use dummy API key for config generation - no actual API calls will be made  
    model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini"
    )
    
    print("Creating agents...")
    
    # Create all agents using the modular approach
    customer_verification_agent = create_customer_verification_agent(model_client)
    document_processing_agent = create_document_processing_agent(model_client)
    orchestrator_agent = create_orchestrator_agent(model_client)
    eligibility_decision_agent = create_eligibility_decision_agent(model_client)
    benefit_execution_agent = create_benefit_execution_agent(model_client)
    judge_agent = create_judge_agent(model_client)
    user_proxy_agent = create_user_proxy_agent()
    
    print("Creating termination conditions...")
    
    # Create termination conditions
    max_message_termination = MaxMessageTermination(max_messages=200)
    text_mention_termination = TextMentionTermination(text="TERMINATE")
    
    # Use simple TextMentionTermination to avoid constructor issues
    termination_condition = text_mention_termination
    
    print("Creating team...")
    
    # Create the team
    team = SelectorGroupChat(
        participants=[
            customer_verification_agent,
            document_processing_agent,
            eligibility_decision_agent,
            orchestrator_agent,
            benefit_execution_agent,
            judge_agent,
            user_proxy_agent
        ],
        model_client=model_client,
        model_context=HeadAndTailChatCompletionContext(head_size=1, tail_size=2),
        termination_condition=termination_condition,
        allow_repeated_speaker=False,
        selector_prompt="""STEP 1: Look at the conversation below and find the VERY LAST speaker (scan from bottom up, find the final agent name before a colon).

STEP 2: Apply these rules:
- If the final speaker was NOT 'Orchestrator_agent' → return 'Orchestrator_agent'
- If the final speaker WAS 'Orchestrator_agent' → look for 'next_agent' in their JSON response and return that agent name

<CONVERSATION_HISTORY>
{history}
</CONVERSATION_HISTORY>

Read the above history and find the final speaker. Apply the rules. Return ONLY the agent name:""",
        max_selector_attempts=3
    )
    
    print("Team created successfully!")
    return team


def export_team_config(team, output_file: str = "generated_orchestrator.json"):
    """Export the team configuration to JSON."""
    try:
        print(f"Exporting team configuration to {output_file}...")
        config = team.dump_component()
        
        # Try to serialize the config with custom JSON encoder
        import json
        class ComponentEncoder(json.JSONEncoder):
            def default(self, obj):
                # Try to convert ComponentModel to dict
                if hasattr(obj, '__dict__'):
                    return obj.__dict__
                elif hasattr(obj, 'dump_component'):
                    return obj.dump_component()
                return str(obj)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False, cls=ComponentEncoder)
        
        print(f"✅ Team configuration exported successfully to {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Error exporting team configuration: {e}")
        print("💡 Using alternative serialization approach...")
        
        # Alternative: convert to string representation
        try:
            with open(output_file.replace('.json', '_repr.txt'), 'w', encoding='utf-8') as f:
                f.write(str(config))
            print(f"✅ Team configuration saved as string representation")
            return True
        except Exception as e2:
            print(f"❌ Alternative export also failed: {e2}")
            return False


def main():
    """Main function to create and export the benefit orchestrator team."""
    try:
        # Create the team
        team = create_benefit_orchestrator_team()
        
        # Export to JSON
        success = export_team_config(team)
        
        if success:
            print("\n🎉 Benefit Orchestrator creation completed successfully!")
            print("📄 Configuration saved to: generated_orchestrator.json")
            print("🚀 Ready to use in AutoGen Studio!")
        else:
            print("\n⚠️  Team created but export failed.")
            print("💡 You can still use the team object in Python code.")
            
    except Exception as e:
        print(f"❌ Error creating team: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 