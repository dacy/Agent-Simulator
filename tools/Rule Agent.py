import json
from typing import List, Dict, Any

def suggest_next_step(conversation_history_json: str) -> str:
    """
    Analyzes the conversation history and suggests the next agent to invoke.
    This tool provides routing logic for the orchestrator.

    Args:
        conversation_history_json: A JSON string representing the list of messages.

    Returns:
        The name of the next agent to be invoked (e.g., "UserProxyAgent", "Benefit_Execution_agent").
    """
    try:
        # It's safer for agents to pass complex data as JSON strings
        conversation_history: List[Dict[str, Any]] = json.loads(conversation_history_json)
        if not conversation_history:
            # This case should ideally not be hit if the orchestrator calls this correctly
            return "Customer_Verification_agent"
    except (json.JSONDecodeError, TypeError):
        # If history is not valid JSON or empty, start from the beginning.
        return "Customer_Verification_agent"

    # The conversation history includes the orchestrator's prompts, so we look at the last agent's actual response
    last_agent_message = None
    for msg in reversed(conversation_history):
        if msg.get("name") and msg.get("name") != "Orchestrator Agent":
            last_agent_message = msg
            break
    
    if not last_agent_message:
        # If no agent has spoken yet, it's the beginning of the workflow.
        # Check if documents are mentioned in the first user message
        initial_user_message = conversation_history[0].get("content", "")
        if "document" in initial_user_message.lower() or "file" in initial_user_message.lower() or "attached" in initial_user_message.lower():
             return "Document_Processing_agent"
        else:
             return "Customer_Verification_agent"

    last_message_content = last_agent_message.get("content", "")
    last_message_name = last_agent_message.get("name", "")

    # Rule 1: After document processing, verify customer
    if last_message_name == "Document_Processing_agent":
        return "Customer_Verification_agent"

    # Rule 2: Handle customer verification failure
    if last_message_name == "Customer_Verification_agent" and '"found": false' in last_message_content:
        return "Eligibility_Decision_agent" # To ask the user for more info

    # Rule 3: After successful verification, decide eligibility
    if last_message_name == "Customer_Verification_agent" and '"found": true' in last_message_content:
        return "Eligibility_Decision_agent"

    # Rule 4: If eligibility agent needs docs, go to user
    if last_message_name == "Eligibility_Decision_agent" and "REQUEST_PROCESS_DOC" in last_message_content:
        return "UserProxyAgent"

    # Rule 5: After a decision is made, execute it
    if last_message_name == "Eligibility_Decision_agent" and '"decision": "approve"' in last_message_content:
        return "Benefit_Execution_agent"

    # Rule 6: After execution, or if declined, we are done
    if last_message_name == "Benefit_Execution_agent" or ('"decision": "decline"' in last_message_content):
        return "TERMINATE"
        
    # Fallback: if confused, ask the Judge agent for a recommendation
    return "Judge_agent" 