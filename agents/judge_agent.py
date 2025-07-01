"""
Judge Agent for the Benefit Orchestrator System.
Handles quality assessment of the benefit processing workflow.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import UnboundedChatCompletionContext


def create_judge_agent(model_client):
    """Create the Judge Agent."""
    
    system_message = """You are the Judge Agent.
You review the full conversation history and evaluate the quality of the benefit processing workflow.

**EXPECTED WORKFLOW RULES (from Request Analysis Agent):**
1. **Initial Step**: Customer_Verification_agent
2. **After Customer Verification**: Always → Eligibility_Decision_agent
3. **Document Request Handling (applies globally)**:
   - If any agent requests documents (REQUEST_PROCESS_DOC) → Document_Processing_agent
   - After Document Processing completes → return to the agent that originally requested documents
4. **After Eligibility Decision**: Always → Judge_agent
5. **After Judge Agent**: Always → UserProxyAgent
6. **After UserProxyAgent (User Response)**:
   - If user agrees with decision → Benefit_Execution_agent
   - If user disagrees, collect user's updated decision → Benefit_Execution_agent (using the user's decision)
7. **After Benefit Execution**: Always → TERMINATE

**Your Task:**
1. Review the complete conversation from start to current point
2. Evaluate workflow compliance with the above rules
3. Assess customer verification, document processing, eligibility decision quality
4. Check if all required steps were properly completed
5. Verify agents followed proper sequence and procedures

**Return structured feedback:**
```json
{
  "quality_score": 0-7,
  "workflow_compliance": "COMPLIANT" | "MINOR_DEVIATION" | "MAJOR_DEVIATION",
  "evaluation_summary": "Overall assessment of processing quality",
  "strengths": ["What was done well"],
  "concerns": ["Any issues, gaps, or rule violations identified"],
  "recommendation": "PROCEED" | "USER_REVIEW_REQUIRED"
}
```

**Scoring Guide:**
- 7: Perfect execution, all steps complete, full compliance
- 6: Good execution, minor issues or deviations
- 5-4: Adequate but notable concerns or rule deviations
- 3-0: Significant issues or major rule violations requiring review

**If score < 6, set recommendation to USER_REVIEW_REQUIRED**"""
    
    return AssistantAgent(
        name="Judge_agent",
        description="Monitors orchestration correctness and suggests human review",
        model_client=model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=[],
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 