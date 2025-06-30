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