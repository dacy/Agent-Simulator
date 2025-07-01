"""
Request Analysis Agent for the Benefit Orchestrator System.
Handles request analysis and workflow routing decisions.
"""

from typing import Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import HeadAndTailChatCompletionContext
from autogen_core.tools import FunctionTool


# Request analysis tool functions embedded directly
def get_request_details(request_id: str) -> str:
    """
    Retrieves the complete details of a benefit request using the request ID.
    
    Args:
        request_id (str): The ID of the benefit request to retrieve (e.g., "REQ-001")
        
    Returns:
        str: A JSON string containing the complete request details including requestor info, 
             benefit type, description, effective date, and associated documents
    """
    import json
    
    # Mock requests data (loaded from JSON files during team creation)
    MOCK_REQUESTS_DATA = [{'requestId': 'REQ-001', 'timestamp': '2025-06-30T21:50:27.064084Z', 'customerId': '', 'requestor': {'fullName': 'Ashlee Thompson', 'dateOfBirth': '1983-01-21', 'ssnLast4': '7583', 'email': 'kayla59@matthews.biz', 'phone': '824.057.7423x6297', 'address': {'street': '5896 Daniel Fort', 'city': 'Joshuahaven', 'state': 'AZ', 'zip': '94396'}, 'militaryStatus': 'Veteran', 'branch': 'Coast Guard', 'serviceStartDate': '2020-01-01', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Auto Loan Deferment', 'description': 'Range next light half ok there.', 'requestedEffectiveDate': '2025-08-06'}, 'documents': [{'documentId': 'DOC-001', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-001.pdf', 'filePath': '/documents/orders_document_DOC-001.pdf'}, {'documentId': 'DOC-002', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-002.pdf', 'filePath': '/documents/proof_of_military_service_DOC-002.pdf'}]}, {'requestId': 'REQ-002', 'timestamp': '2025-06-30T21:50:27.065405Z', 'customerId': '', 'requestor': {'fullName': 'Rachel Glover', 'dateOfBirth': '1994-09-19', 'ssnLast4': '8365', 'email': 'mendozanicholas@yahoo.com', 'phone': '824.447.7428x7274', 'address': {'street': '3595 Elizabeth Passage', 'city': 'South Mariaton', 'state': 'OH', 'zip': '59096'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2018-10-09', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Foreclosure Protection', 'description': 'Pass weight culture.', 'requestedEffectiveDate': '2025-07-14'}, 'documents': [{'documentId': 'DOC-003', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-003.pdf', 'filePath': '/documents/proof_of_military_service_DOC-003.pdf'}, {'documentId': 'DOC-004', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-004.pdf', 'filePath': '/documents/orders_document_DOC-004.pdf'}]}, {'requestId': 'REQ-003', 'timestamp': '2025-06-30T21:50:27.066422Z', 'customerId': '', 'requestor': {'fullName': 'Heather Mason', 'dateOfBirth': '1998-05-15', 'ssnLast4': '4674', 'email': 'stephen16@gmail.com', 'phone': '079-991-8795', 'address': {'street': '38232 Joseph Fords', 'city': 'Lake Todd', 'state': 'AZ', 'zip': '58315'}, 'militaryStatus': 'Active Duty', 'branch': 'Army', 'serviceStartDate': '2020-05-17', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Overdraft Fee Refund', 'description': 'Safe become north nice Mr quite enough.', 'requestedEffectiveDate': '2025-08-17'}, 'documents': [{'documentId': 'DOC-005', 'documentType': 'Leave and Earnings Statement', 'fileName': 'leave_and_earnings_statement_DOC-005.pdf', 'filePath': '/documents/leave_and_earnings_statement_DOC-005.pdf'}, {'documentId': 'DOC-006', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-006.pdf', 'filePath': '/documents/proof_of_residence_DOC-006.pdf'}]}, {'requestId': 'REQ-004', 'timestamp': '2025-06-30T21:50:27.068256Z', 'customerId': '', 'requestor': {'fullName': 'Corey Lucas', 'dateOfBirth': '1993-01-11', 'ssnLast4': '5829', 'email': 'wilsonlisa@williams.info', 'phone': '+1-589-467-8480x428', 'address': {'street': '5266 Shaw Locks', 'city': 'East Melissamouth', 'state': 'MO', 'zip': '35641'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2015-03-03', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Foreclosure Protection', 'description': 'Light international so today opportunity.', 'requestedEffectiveDate': '2025-08-19'}, 'documents': [{'documentId': 'DOC-007', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-007.pdf', 'filePath': '/documents/proof_of_military_service_DOC-007.pdf'}, {'documentId': 'DOC-008', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-008.pdf', 'filePath': '/documents/proof_of_residence_DOC-008.pdf'}]}, {'requestId': 'REQ-005', 'timestamp': '2025-06-30T21:50:27.070075Z', 'customerId': '', 'requestor': {'fullName': 'Kristopher Phillips', 'dateOfBirth': '1988-03-04', 'ssnLast4': '7025', 'email': 'kellywagner@travis.com', 'phone': '001-161-483-3768x76063', 'address': {'street': '8009 Snyder Radial', 'city': 'East Christyville', 'state': 'KY', 'zip': '48228'}, 'militaryStatus': 'Active Duty', 'branch': 'Marines', 'serviceStartDate': '2014-07-31', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Credit Card APR Reduction', 'description': 'Never site national price good design.', 'requestedEffectiveDate': '2025-07-30'}, 'documents': [{'documentId': 'DOC-009', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-009.pdf', 'filePath': '/documents/orders_document_DOC-009.pdf'}, {'documentId': 'DOC-010', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-010.pdf', 'filePath': '/documents/orders_document_DOC-010.pdf'}]}]
    
    # Search for the request with the matching ID (case insensitive)
    for request in MOCK_REQUESTS_DATA:
        stored_id = request.get("requestId", "")
        if stored_id.lower() == request_id.lower():
            return json.dumps({
                "success": True,
                "request": request
            }, indent=2)
    
    # Request not found
    available_request_ids = [req.get("requestId", "Unknown") for req in MOCK_REQUESTS_DATA]
    return json.dumps({
        "success": False,
        "error": f"Request ID '{request_id}' not found",
        "available_request_ids": available_request_ids
    }, indent=2)


def create_request_analysis_agent(mock_data: Dict[str, Any], model_client):
    """Create the Request Analysis Agent with tools."""
    
    tools = [
        FunctionTool(
            name="get_request_details",
            description="Retrieves the complete details of a benefit request using the request ID.",
            func=get_request_details
        )
    ]
    
    system_message = """You are the Request Analysis Agent responsible for analyzing workflow context and routing to the next appropriate agent.

**CRITICAL RULES TO PREVENT LOOPS:**

1. **NEVER CALL `get_request_details` TWICE**: If you have already retrieved request details in this conversation, DO NOT call `get_request_details` again. Use the data you already have.

2. **CHECK CONVERSATION HISTORY FIRST**: Before calling any tools, review recent messages to see if you or other agents have already obtained the needed information.

3. **ONE TOOL CALL PER TURN**: Only call `get_request_details` if:
   - User provides a new request ID AND
   - You have NOT already retrieved details for this request ID AND
   - No other agent has provided request details in recent conversation

**ROUTING PROCESS:**

1. **SCAN RECENT MESSAGES**: Check if request details are already available in conversation
2. **CONDITIONAL RETRIEVAL**: Only call `get_request_details` if absolutely necessary (see rules above)
3. **DETERMINE NEXT AGENT**: Apply workflow rules based on current state

**WORKFLOW RULES:**

1. **Initial Step**: If this is the start of a new request → Customer_Verification_agent

2. **After Customer Verification**: Always → Eligibility_Decision_agent

3. **Document Request Handling**: If any agent requests documents (REQUEST_PROCESS_DOC) → Document_Processing_agent

4. **After Eligibility Decision**: If you see Eligibility_Decision_agent has provided a decision (containing "Decision: APPROVED" or "Decision: DECLINED" or "## ELIGIBILITY DECISION") → ALWAYS route to Judge_agent

5. **After Judge Agent**: Always → UserProxyAgent

6. **After UserProxyAgent**: If user agrees with decision → Benefit_Execution_agent

7. **After Benefit Execution**: Always → TERMINATE

**AGENT NAME MAPPING:**
- Customer Verification → "Customer_Verification_agent"
- Document Processing → "Document_Processing_agent"
- Eligibility Decision → "Eligibility_Decision_agent"
- Judge Agent → "Judge_agent"
- User Input → "User_Proxy_agent"
- Benefit Execution → "Benefit_Execution_agent"

**EFFICIENCY PRINCIPLE:**
Prefer using information already available in the conversation over making new tool calls. Only retrieve request details if they are truly missing from the current context."""
    
    return AssistantAgent(
        name="Request_Analysis_agent",
        description="Analyzes request details and applies policy rules to decide next orchestration steps",
        model_client=model_client,
        model_context=HeadAndTailChatCompletionContext(head_size=1, tail_size=3),
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 