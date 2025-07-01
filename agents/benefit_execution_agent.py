"""
Benefit Execution Agent for the Benefit Orchestrator System.
Handles final execution of approved benefits or decline notifications.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import UnboundedChatCompletionContext


def create_benefit_execution_agent(model_client):
    """Create the Benefit Execution Agent."""
    
    system_message = """You are the Benefit Execution Agent.
You always carry out the final execution step based on the decision made.

**For APPROVED benefits:**
- Execute the benefit enrollment/activation
- Generate confirmation details
- Notify customer of successful activation

**For DECLINED benefits:**
- Generate decline notification
- Provide clear explanation of decision
- Include any appeal/reapplication information

**Return structured response:**
```json
{
  "execution_type": "benefit_activation" | "decline_notification",
  "status": "success" | "failure",
  "customer_message": "...",
  "details": "..."
}
```"""
    
    return AssistantAgent(
        name="Benefit_Execution_agent",
        description="Executes benefit after approval",
        model_client=model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=[],
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 