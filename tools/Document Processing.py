import json

def get_document(request_id: str, document_id: str) -> str:
    """
    Retrieves a specific document based on request ID and document ID.
    
    Args:
        request_id (str): The ID of the benefit request
        document_id (str): The ID of the specific document to retrieve
        
    Returns:
        str: A JSON string containing the document content or an error message
    """
    # These will be replaced with actual mock data by combine_tools.py
    MOCK_REQUESTS_DATA = "{{MOCK_REQUESTS_DATA}}"
    MOCK_DOCUMENTS_DATA = "{{MOCK_DOCUMENTS_DATA}}"
    
    # Create a lookup from the mock data with case insensitive keys
    request_documents = {}
    request_id_mapping = {}  # Maps lowercase request_id to actual request_id
    
    # Build document lookup by request_id and document_id (case insensitive)
    for request in MOCK_REQUESTS_DATA:
        req_id = request["requestId"]
        req_id_lower = req_id.lower()
        
        # Store the mapping from lowercase to actual case
        request_id_mapping[req_id_lower] = req_id
        
        if req_id_lower not in request_documents:
            request_documents[req_id_lower] = {}
        
        # Also create document_id mapping for case insensitive lookup
        doc_id_mapping = {}
        
        for doc in request.get("documents", []):
            doc_id = doc["documentId"]
            doc_id_lower = doc_id.lower()
            
            # Store mapping from lowercase to actual case
            doc_id_mapping[doc_id_lower] = doc_id
            
            # Create mock document content based on type
            mock_content = create_mock_document_content(doc["documentType"], request, doc)
            request_documents[req_id_lower][doc_id_lower] = {
                "type": doc["documentType"],
                "fileName": doc["fileName"],
                "filePath": doc["filePath"],
                "content": mock_content,
                "actual_document_id": doc_id  # Store actual case for response
            }
    
    # Convert search parameters to lowercase for comparison
    request_id_lower = request_id.lower()
    document_id_lower = document_id.lower()
    
    # Check if request exists (case insensitive)
    if request_id_lower not in request_documents:
        available_requests = [request_id_mapping[req_id] for req_id in request_documents.keys()]
        return json.dumps({
            "error": f"Request ID '{request_id}' not found",
            "available_requests": available_requests
        })
    
    # Check if document exists for this request (case insensitive)
    if document_id_lower not in request_documents[request_id_lower]:
        available_documents = [doc_data["actual_document_id"] for doc_data in request_documents[request_id_lower].values()]
        return json.dumps({
            "error": f"Document ID '{document_id}' not found for request '{request_id}'",
            "available_documents": available_documents
        })
    
    # Return the document content
    document_data = request_documents[request_id_lower][document_id_lower]
    actual_request_id = request_id_mapping[request_id_lower]
    actual_document_id = document_data["actual_document_id"]
    
    return json.dumps({
        "request_id": actual_request_id,
        "document_id": actual_document_id,
        "document_type": document_data["type"],
        "file_name": document_data["fileName"],
        "content": document_data["content"]
    })

def create_mock_document_content(doc_type: str, request: dict, doc: dict) -> dict:
    """Create realistic mock document content based on document type."""
    
    base_content = {
        "document_id": doc["documentId"],
        "file_path": doc["filePath"],
        "processed_date": "2024-12-30"
    }
    
    if doc_type == "Orders Document":
        return {
            **base_content,
            "orders_type": "Permanent Change of Station (PCS)",
            "effective_date": request["requestDetails"]["requestedEffectiveDate"],
            "from_location": "Previous Base",
            "to_location": "New Assignment Location",
            "report_date": request["requestDetails"]["requestedEffectiveDate"]
        }
    
    elif doc_type == "Proof of Military Service":
        return {
            **base_content,
            "service_verification": True,
            "active_duty_status": "Active",
            "branch": "U.S. Army",
            "rank": "Sergeant (E-5)",
            "verification_date": "2024-12-30"
        }
    
    elif doc_type == "Leave and Earnings Statement":
        return {
            **base_content,
            "pay_period": "2024-12-01 to 2024-12-31",
            "base_pay": 3500.00,
            "allowances": 1200.00,
            "deductions": 800.00,
            "net_pay": 3900.00
        }
    
    elif doc_type == "Proof of Residence":
        return {
            **base_content,
            "address_verified": True,
            "lease_start_date": "2024-01-01",
            "monthly_rent": 2500.00,
            "landlord_contact": "Property Management Company"
        }
    
    else:
        return {
            **base_content,
            "content_type": doc_type,
            "status": "verified"
        } 