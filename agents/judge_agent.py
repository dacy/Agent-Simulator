"""
Judge Agent for the Benefit Orchestrator System.
Handles quality assessment of the benefit processing workflow.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import UnboundedChatCompletionContext


def create_judge_agent(model_client):
    """Create the Judge Agent with structured output."""
    
    # Create a model client with structured output for quality assessment
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    structured_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "quality_assessment",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "quality_score": {
                            "type": "integer",
                            "description": "Overall processing quality score (0-7)",
                            "minimum": 0,
                            "maximum": 7
                        },
                        "workflow_compliance": {
                            "type": "string",
                            "description": "Assessment of adherence to workflow rules",
                            "enum": ["COMPLIANT", "MINOR_DEVIATION", "MAJOR_DEVIATION"]
                        },
                        "evaluation_summary": {
                            "type": "string",
                            "description": "Overall assessment of processing quality"
                        },
                        "strengths": {
                            "type": "array",
                            "description": "List of what was done well",
                            "items": {"type": "string"}
                        },
                        "concerns": {
                            "type": "array",
                            "description": "List of issues, gaps, or rule violations identified", 
                            "items": {"type": "string"}
                        },
                        "recommendation": {
                            "type": "string",
                            "description": "Final recommendation for workflow outcome",
                            "enum": ["PROCEED", "USER_REVIEW_REQUIRED"]
                        }
                    },
                    "required": [
                        "quality_score",
                        "workflow_compliance",
                        "evaluation_summary",
                        "strengths",
                        "concerns",
                        "recommendation"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )
    
    system_message = """You are the Judge Agent.
You review the full conversation history and evaluate the quality of the benefit processing workflow.

**EXPECTED WORKFLOW RULES (from Orchestrator Agent):**

1. **Initial Step**: If this is the start of a new request (user provides request ID) → First call `get_request_details` to get the request details, then route to Customer_Verification_agent

2. **After Customer Verification**: Always → Eligibility_Decision_agent

3. **Document Request Handling**: If any agent requests documents (REQUEST_PROCESS_DOC) → Document_Processing_agent

4. **After Eligibility Decision**: If you see Eligibility_Decision_agent has provided a decision (containing "Decision: APPROVED" or "Decision: DECLINED" or "## ELIGIBILITY DECISION") → ALWAYS route to Judge_agent

5. **After Judge Agent**: Always → User_Proxy_agent

6. **After User_Proxy_agent**: If user agrees with decision → Benefit_Execution_agent

7. **After Benefit Execution**: If you see Benefit_Execution_agent has provided execution results (containing "execution_type", "status", or "TERMINATE") → ALWAYS route to TERMINATE

**AGENT NAME MAPPING:**
- Customer Verification → "Customer_Verification_agent"
- Document Processing → "Document_Processing_agent"
- Eligibility Decision → "Eligibility_Decision_agent"
- Judge Agent → "Judge_agent"
- User Input → "User_Proxy_agent"
- Benefit Execution → "Benefit_Execution_agent"

**TERMINATION DETECTION:**
- Look for Benefit_Execution_agent messages containing execution results
- If execution is complete, route to TERMINATE
- Do NOT route back to Customer_Verification_agent after benefit execution
- The workflow ends after benefit execution, not before

**Your Task:**
1. **Review Complete Conversation**: Analyze the full conversation from start to current point
2. **Evaluate Workflow Compliance**: Check if agents followed the exact workflow rules above
3. **Assess Tool Usage**: Verify Orchestrator Agent properly used `get_request_details` when needed
4. **Check Agent Sequence**: Ensure agents were called in the correct order according to workflow rules
5. **Verify Document Handling**: Confirm document requests were properly routed through Document Processing Agent
6. **Assess Decision Quality**: Evaluate the quality of customer verification, eligibility decisions, and benefit execution
7. **Check Termination Logic**: Verify the workflow properly terminated after benefit execution
8. **Identify Rule Violations**: Flag any deviations from the expected workflow sequence

**Scoring Guide:**

**Score 7 (Perfect Execution):**
- All workflow steps completed in correct sequence
- Orchestrator Agent properly retrieved request details when needed
- Document requests properly routed through Document Processing Agent
- All agents provided high-quality outputs
- Workflow terminated correctly after benefit execution

**Score 6 (Good Execution):**
- Minor deviations from workflow rules
- Small issues with tool usage or agent sequencing
- Overall quality maintained with minor concerns

**Score 5-4 (Adequate Execution):**
- Notable deviations from workflow rules
- Issues with agent sequencing or tool usage
- Quality concerns in some agent outputs
- May have skipped or duplicated steps

**Score 3-0 (Poor Execution):**
- Major rule violations or workflow deviations
- Significant issues with agent sequencing
- Poor quality outputs from multiple agents
- Missing critical steps or improper termination

**If score < 6, set recommendation to USER_REVIEW_REQUIRED**"""
    
    return AssistantAgent(
        name="Judge_agent",
        description="Monitors orchestration correctness and suggests human review",
        model_client=structured_model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=[],
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 