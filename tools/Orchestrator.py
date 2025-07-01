import json

def get_request_details(request_id: str) -> str:
    """
    Retrieves the complete details of a benefit request using the request ID.
    
    Args:
        request_id (str): The ID of the benefit request to retrieve (e.g., "REQ-001")
        
    Returns:
        str: A JSON string containing the complete request details including requestor info, 
             benefit type, description, effective date, and associated documents
    """
    # This will be replaced with actual mock data by combine_tools.py
    MOCK_REQUESTS_DATA = "{{MOCK_REQUESTS_DATA}}"
    
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

def generate_routing_output(next_agent: str, request_details: dict = None, context_summary: str = "", instructions: str = "") -> str:
    """
    Generates a structured routing output that the orchestrator can reliably parse.
    
    Args:
        next_agent (str): The name of the next agent to route to
        request_details (dict): Optional request details to include
        context_summary (str): Summary of current workflow progress
        instructions (str): Specific instructions for the next agent
        
    Returns:
        str: Formatted routing output with clear agent selection
    """
    output = []
    
    # Very prominent routing section that orchestrator looks for
    output.append("=== ORCHESTRATOR ROUTING ===")
    output.append(f"NEXT_AGENT: {next_agent}")
    output.append("=== END ROUTING ===")
    output.append("")
    
    # Orchestration section
    if request_details:
        output.append("## ORCHESTRATION")
        output.append(f"**Request ID:** {request_details.get('requestId', 'N/A')}")
        output.append(f"**Requestor:** {request_details.get('requestor', {}).get('fullName', 'N/A')}")
        output.append(f"**Benefit Type:** {request_details.get('requestDetails', {}).get('benefitType', 'N/A')}")
        output.append(f"**Military Status:** {request_details.get('requestor', {}).get('militaryStatus', 'N/A')}")
        output.append(f"**Service Branch:** {request_details.get('requestor', {}).get('branch', 'N/A')}")
        output.append("")
    
    # Next agent section (backup for the orchestrator)
    output.append("## NEXT AGENT")
    output.append(f"**Agent:** {next_agent}")
    output.append("")
    
    # Instructions for next agent
    if instructions:
        output.append("## INSTRUCTIONS FOR NEXT AGENT")
        output.append(instructions)
        output.append("")
    
    # Context summary
    if context_summary:
        output.append("## CONTEXT SUMMARY")
        output.append(context_summary)
        output.append("")
    
    return "\n".join(output) 