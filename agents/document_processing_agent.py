"""
Document Processing Agent for the Benefit Orchestrator System.
Handles document retrieval and processing for benefit requests.
"""

from typing import Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import UnboundedChatCompletionContext
from autogen_core.tools import FunctionTool


# Document processing tool function embedded directly
def get_document(request_id: str, document_id: str) -> str:
    """
    Retrieves a specific document based on request ID and document ID.
    
    Args:
        request_id (str): The ID of the benefit request
        document_id (str): The ID of the specific document to retrieve
        
    Returns:
        str: A JSON string containing the document content or an error message
    """
    import json
    
    # Mock data (loaded from JSON files during team creation)
    MOCK_REQUESTS_DATA = [{'requestId': 'REQ-001', 'timestamp': '2025-06-30T21:50:27.064084Z', 'customerId': '', 'requestor': {'fullName': 'Ashlee Thompson', 'dateOfBirth': '1983-01-21', 'ssnLast4': '7583', 'email': 'kayla59@matthews.biz', 'phone': '824.057.7423x6297', 'address': {'street': '5896 Daniel Fort', 'city': 'Joshuahaven', 'state': 'AZ', 'zip': '94396'}, 'militaryStatus': 'Veteran', 'branch': 'Coast Guard', 'serviceStartDate': '2020-01-01', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Auto Loan Deferment', 'description': 'Range next light half ok there.', 'requestedEffectiveDate': '2025-08-06'}, 'documents': [{'documentId': 'DOC-001', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-001.pdf', 'filePath': '/documents/orders_document_DOC-001.pdf'}, {'documentId': 'DOC-002', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-002.pdf', 'filePath': '/documents/proof_of_military_service_DOC-002.pdf'}]}, {'requestId': 'REQ-002', 'timestamp': '2025-06-30T21:50:27.065405Z', 'customerId': '', 'requestor': {'fullName': 'Rachel Glover', 'dateOfBirth': '1994-09-19', 'ssnLast4': '8365', 'email': 'mendozanicholas@yahoo.com', 'phone': '824.447.7428x7274', 'address': {'street': '3595 Elizabeth Passage', 'city': 'South Mariaton', 'state': 'OH', 'zip': '59096'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2018-10-09', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Foreclosure Protection', 'description': 'Pass weight culture.', 'requestedEffectiveDate': '2025-07-14'}, 'documents': [{'documentId': 'DOC-003', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-003.pdf', 'filePath': '/documents/proof_of_military_service_DOC-003.pdf'}, {'documentId': 'DOC-004', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-004.pdf', 'filePath': '/documents/orders_document_DOC-004.pdf'}]}, {'requestId': 'REQ-003', 'timestamp': '2025-06-30T21:50:27.066422Z', 'customerId': '', 'requestor': {'fullName': 'Heather Mason', 'dateOfBirth': '1998-05-15', 'ssnLast4': '4674', 'email': 'stephen16@gmail.com', 'phone': '079-991-8795', 'address': {'street': '38232 Joseph Fords', 'city': 'Lake Todd', 'state': 'AZ', 'zip': '58315'}, 'militaryStatus': 'Active Duty', 'branch': 'Army', 'serviceStartDate': '2020-05-17', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Overdraft Fee Refund', 'description': 'Safe become north nice Mr quite enough.', 'requestedEffectiveDate': '2025-08-17'}, 'documents': [{'documentId': 'DOC-005', 'documentType': 'Leave and Earnings Statement', 'fileName': 'leave_and_earnings_statement_DOC-005.pdf', 'filePath': '/documents/leave_and_earnings_statement_DOC-005.pdf'}, {'documentId': 'DOC-006', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-006.pdf', 'filePath': '/documents/proof_of_residence_DOC-006.pdf'}]}, {'requestId': 'REQ-004', 'timestamp': '2025-06-30T21:50:27.068256Z', 'customerId': '', 'requestor': {'fullName': 'Corey Lucas', 'dateOfBirth': '1993-01-11', 'ssnLast4': '5829', 'email': 'wilsonlisa@williams.info', 'phone': '+1-589-467-8480x428', 'address': {'street': '5266 Shaw Locks', 'city': 'East Melissamouth', 'state': 'MO', 'zip': '35641'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2015-03-03', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Foreclosure Protection', 'description': 'Light international so today opportunity.', 'requestedEffectiveDate': '2025-08-19'}, 'documents': [{'documentId': 'DOC-007', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-007.pdf', 'filePath': '/documents/proof_of_military_service_DOC-007.pdf'}, {'documentId': 'DOC-008', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-008.pdf', 'filePath': '/documents/proof_of_residence_DOC-008.pdf'}]}, {'requestId': 'REQ-005', 'timestamp': '2025-06-30T21:50:27.070075Z', 'customerId': '', 'requestor': {'fullName': 'Kristopher Phillips', 'dateOfBirth': '1988-03-04', 'ssnLast4': '7025', 'email': 'kellywagner@travis.com', 'phone': '001-161-483-3768x76063', 'address': {'street': '8009 Snyder Radial', 'city': 'East Christyville', 'state': 'KY', 'zip': '48228'}, 'militaryStatus': 'Active Duty', 'branch': 'Marines', 'serviceStartDate': '2014-07-31', 'serviceEndDate': None}, 'requestDetails': {'benefitType': 'Credit Card APR Reduction', 'description': 'Never site national price good design.', 'requestedEffectiveDate': '2025-07-30'}, 'documents': [{'documentId': 'DOC-009', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-009.pdf', 'filePath': '/documents/orders_document_DOC-009.pdf'}, {'documentId': 'DOC-010', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-010.pdf', 'filePath': '/documents/orders_document_DOC-010.pdf'}]}]
    MOCK_DOCUMENTS_DATA = [{'documentId': 'DOC-001', 'requestId': 'REQ-001', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-001.pdf', 'filePath': '/documents/orders_document_DOC-001.pdf'}, {'documentId': 'DOC-002', 'requestId': 'REQ-001', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-002.pdf', 'filePath': '/documents/proof_of_military_service_DOC-002.pdf'}, {'documentId': 'DOC-003', 'requestId': 'REQ-002', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-003.pdf', 'filePath': '/documents/proof_of_military_service_DOC-003.pdf'}, {'documentId': 'DOC-004', 'requestId': 'REQ-002', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-004.pdf', 'filePath': '/documents/orders_document_DOC-004.pdf'}, {'documentId': 'DOC-005', 'requestId': 'REQ-003', 'documentType': 'Leave and Earnings Statement', 'fileName': 'leave_and_earnings_statement_DOC-005.pdf', 'filePath': '/documents/leave_and_earnings_statement_DOC-005.pdf'}, {'documentId': 'DOC-006', 'requestId': 'REQ-003', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-006.pdf', 'filePath': '/documents/proof_of_residence_DOC-006.pdf'}, {'documentId': 'DOC-007', 'requestId': 'REQ-004', 'documentType': 'Proof of Military Service', 'fileName': 'proof_of_military_service_DOC-007.pdf', 'filePath': '/documents/proof_of_military_service_DOC-007.pdf'}, {'documentId': 'DOC-008', 'requestId': 'REQ-004', 'documentType': 'Proof of Residence', 'fileName': 'proof_of_residence_DOC-008.pdf', 'filePath': '/documents/proof_of_residence_DOC-008.pdf'}, {'documentId': 'DOC-009', 'requestId': 'REQ-005', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-009.pdf', 'filePath': '/documents/orders_document_DOC-009.pdf'}, {'documentId': 'DOC-010', 'requestId': 'REQ-005', 'documentType': 'Orders Document', 'fileName': 'orders_document_DOC-010.pdf', 'filePath': '/documents/orders_document_DOC-010.pdf'}]
    
    def _create_mock_document_content(doc_type: str, request: dict, doc: dict) -> dict:
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
            mock_content = _create_mock_document_content(doc["documentType"], request, doc)
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


def create_document_processing_agent(mock_data: Dict[str, Any], model_client):
    """Create the Document Processing Agent with tools."""
    
    tools = [
        FunctionTool(
            name="get_document",
            description="Retrieves a specific document based on request ID and document ID.",
            func=get_document
        )
    ]
    
    system_message = """You are the Document Processing Agent responsible for retrieving and processing documents needed for benefit eligibility decisions.

**PRIMARY OBJECTIVE:** Retrieve requested documents and provide structured summaries for eligibility assessment.

**DOCUMENT PROCESSING WORKFLOW:**

1. **Document Retrieval**: Use get_document tool with provided document IDs
2. **Content Analysis**: Review document content for relevant eligibility information
3. **Information Extraction**: Extract key data points needed for benefit decisions
4. **Structured Summary**: Provide organized summary for decision-making

**DOCUMENT TYPES AND KEY INFORMATION:**

**Military Orders (DD-1)**
- Service member name and rank
- Duty assignment locations
- Effective dates (start/end)
- Type of orders (PCS, deployment, training)
- Special circumstances or restrictions

**Financial Statements**
- Account balances and transaction history
- Income verification
- Debt obligations and payment history
- Financial hardship indicators
- Military pay documentation (LES)

**DD-214 (Discharge Papers)**
- Service dates and duration
- Discharge type (honorable, general, etc.)
- Military occupation and training
- Service-connected disabilities
- Combat service indicators

**Loan/Credit Documents**
- Account numbers and current balances
- Interest rates and terms
- Payment history and current status
- Origination dates relative to military service
- Lender contact information

**Marriage/Family Documents**
- Marriage certificate with dates
- Dependent information
- Family member military status
- Legal name changes

**Address/Residency Proof**
- Current and previous addresses
- Residency verification
- Utility bills and lease agreements
- Military housing assignments

**PROCESSING STANDARDS:**

**For Each Document Processed:**
```
**Document ID:** [Document ID]
**Document Type:** [Type of document]
**Key Information Extracted:**
- [Specific data point 1]
- [Specific data point 2]
- [Additional relevant information]

**Eligibility Relevance:** [How this document supports or challenges eligibility]
**Verification Status:** [Complete/Incomplete/Requires Additional Information]
```

**QUALITY ASSURANCE:**
- Verify document authenticity markers
- Check for completeness of required information
- Note any discrepancies or missing data
- Flag potential fraud indicators
- Cross-reference information across documents

**FINAL SUMMARY FORMAT:**
```
## DOCUMENT PROCESSING SUMMARY

**Documents Processed:** [List of document IDs]

**Eligibility Supporting Evidence:**
- [Key findings that support benefit eligibility]

**Potential Concerns:**
- [Any issues, gaps, or discrepancies identified]

**Missing Information:**
- [Required documents or data not yet provided]

**Recommendation:** [Ready for decision/Need additional documents/Requires manual review]
```

**CRITICAL INSTRUCTIONS:**
- Process ALL requested document IDs
- Extract specific, actionable information
- Note both supporting and contradicting evidence
- Flag incomplete or suspicious documents
- Provide clear, structured summaries for decision-makers
- Do not make eligibility decisions - only process and summarize documents"""
    
    return AssistantAgent(
        name="Document_Processing_agent",
        description="Retrieves and processes documents required for benefit decisions",
        model_client=model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 