"""
Benefit Execution Agent for the Benefit Orchestrator System.
Handles final execution of approved benefits or decline notifications.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import UnboundedChatCompletionContext


def create_benefit_execution_agent(model_client):
    """Create the Benefit Execution Agent with structured output."""
    
    # Create a model client with structured output for execution results
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    structured_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "execution_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "execution_type": {
                            "type": "string",
                            "description": "Type of execution performed",
                            "enum": ["benefit_activation", "decline_notification"]
                        },
                        "status": {
                            "type": "string",
                            "description": "Whether the execution was successful",
                            "enum": ["success", "failure"]
                        },
                        "customer_message": {
                            "type": "string",
                            "description": "Customer-facing message about the outcome"
                        },
                        "details": {
                            "type": "string",
                            "description": "Technical details about the execution or reason for failure"
                        }
                    },
                    "required": [
                        "execution_type",
                        "status",
                        "customer_message",
                        "details"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )
    
    system_message = """You are the Benefit Execution Agent.
You always carry out the final execution step based on the decision made.

**For APPROVED benefits:**
- Execute the benefit enrollment/activation
- Generate confirmation details
- Notify customer of successful activation

**For DECLINED benefits:**
- Generate decline notification
- Provide clear explanation of decision
- Include any appeal/reapplication information"""
    
    return AssistantAgent(
        name="Benefit_Execution_agent",
        description="Executes benefit after approval",
        model_client=structured_model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=[],
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 