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
                "report_date": request["requestDetails"]["requestedEffectiveDate"],
                "service_member_name": request["requestor"]["fullName"],
                "rank": "Sergeant (E-5)",
                "branch": request["requestor"]["branch"],
                "orders_number": "ORD-2025-001",
                "deployment_type": "PCS",
                "duration_days": 180,
                "authorized_by": "Department of Defense"
            }
        
        elif doc_type == "Proof of Military Service":
            return {
                **base_content,
                "service_verification": True,
                "active_duty_status": request["requestor"]["militaryStatus"],
                "branch": request["requestor"]["branch"],
                "rank": "Sergeant (E-5)",
                "verification_date": "2024-12-30",
                "service_start_date": request["requestor"]["serviceStartDate"],
                "service_end_date": request["requestor"]["serviceEndDate"],
                "service_duration_months": 48,
                "discharge_type": "Honorable" if request["requestor"]["militaryStatus"] == "Veteran" else None,
                "military_occupation": "Infantry",
                "combat_service": False,
                "service_connected_disabilities": []
            }
        
        elif doc_type == "Leave and Earnings Statement":
            return {
                **base_content,
                "pay_period": "2024-12-01 to 2024-12-31",
                "base_pay": 3500.00,
                "allowances": 1200.00,
                "deductions": 800.00,
                "net_pay": 3900.00,
                "service_member_name": request["requestor"]["fullName"],
                "rank": "Sergeant (E-5)",
                "branch": request["requestor"]["branch"],
                "deployment_allowance": 250.00,
                "hazard_pay": 0.00,
                "combat_pay": 0.00,
                "total_compensation": 4150.00
            }
        
        elif doc_type == "Proof of Residence":
            return {
                **base_content,
                "address_verified": True,
                "lease_start_date": "2024-01-01",
                "monthly_rent": 2500.00,
                "landlord_contact": "Property Management Company",
                "current_address": request["requestor"]["address"],
                "residency_duration_months": 12,
                "utility_bills_included": True,
                "military_housing": False,
                "pcs_affected": True
            }
        
        elif doc_type == "Loan Statement":
            return {
                **base_content,
                "loan_type": "Auto Loan",
                "account_number": "AUTO-12345",
                "original_balance": 25000.00,
                "current_balance": 18000.00,
                "monthly_payment": 450.00,
                "interest_rate": 4.5,
                "loan_origination_date": "2023-01-15",
                "lender_name": "Military Auto Loans Inc.",
                "payment_history": "Current",
                "deferment_eligible": True,
                "pre_service_account": False
            }
        
        elif doc_type == "Financial Hardship Documentation":
            return {
                **base_content,
                "hardship_type": "Service-related financial burden",
                "monthly_income": 3900.00,
                "monthly_expenses": 4200.00,
                "deficit_amount": 300.00,
                "hardship_duration_months": 6,
                "service_connection": True,
                "documentation_provided": ["Bank statements", "Expense records"],
                "verification_status": "Verified"
            }
        
        elif doc_type == "Mortgage Documents":
            return {
                **base_content,
                "mortgage_type": "Conventional",
                "account_number": "MORT-67890",
                "original_loan_amount": 300000.00,
                "current_balance": 280000.00,
                "monthly_payment": 1800.00,
                "interest_rate": 3.75,
                "loan_origination_date": "2022-06-01",
                "lender_name": "Veterans United",
                "property_address": request["requestor"]["address"],
                "pre_service_mortgage": True,
                "scra_eligible": True
            }
        
        elif doc_type == "Bank Statements":
            return {
                **base_content,
                "bank_name": "USAA Bank",
                "account_type": "Checking",
                "account_number": "****1234",
                "statement_period": "2024-12-01 to 2024-12-31",
                "opening_balance": 2500.00,
                "closing_balance": 1800.00,
                "overdraft_fees": 35.00,
                "fee_dates": ["2024-12-15", "2024-12-22"],
                "deployment_related_fees": True,
                "fee_occurrence_days": 7
            }
        
        elif doc_type == "Credit Statements":
            return {
                **base_content,
                "credit_card_type": "Visa",
                "account_number": "****5678",
                "current_balance": 5000.00,
                "credit_limit": 10000.00,
                "current_apr": 18.99,
                "account_opening_date": "2021-03-15",
                "issuer_name": "Chase Bank",
                "pre_service_account": True,
                "scra_eligible": True,
                "payment_history": "Good"
            }
        
        elif doc_type == "Account History":
            return {
                **base_content,
                "account_type": "Credit Card",
                "account_number": "****5678",
                "opening_date": "2021-03-15",
                "pre_service_balance": 2000.00,
                "pre_service_apr": 18.99,
                "current_balance": 5000.00,
                "current_apr": 18.99,
                "payment_history": "Good",
                "scra_application_date": "2024-12-30"
            }
        
        else:
            return {
                **base_content,
                "content_type": doc_type,
                "status": "verified",
                "document_verified": True,
                "processing_notes": f"Standard processing completed for {doc_type}"
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


def create_document_processing_agent(model_client):
    """Create the Document Processing Agent with tools and structured output."""
    
    tools = [
        FunctionTool(
            name="get_document",
            description="Retrieves a specific document based on request ID and document ID.",
            func=get_document
        )
    ]
    
    # Create a model client with structured output for document processing results
    from autogen_ext.models.openai import OpenAIChatCompletionClient
    structured_model_client = OpenAIChatCompletionClient(
        model="gpt-4o-mini",
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "document_processing_response",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "documents_processed": {
                            "type": "array",
                            "description": "List of processed documents with their content and analysis",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "document_id": {
                                        "type": "string",
                                        "description": "The document ID that was processed"
                                    },
                                    "document_type": {
                                        "type": "string",
                                        "description": "Type of document (e.g., Orders Document, Proof of Military Service, Loan Statement, etc.)"
                                    },
                                    "content": {
                                        "type": "object",
                                        "description": "The actual document content retrieved from the system with detailed fields based on document type",
                                        "properties": {
                                            "document_id": {"type": "string"},
                                            "file_path": {"type": "string"},
                                            "processed_date": {"type": "string"}
                                        },
                                        "required": ["document_id", "file_path", "processed_date"],
                                        "additionalProperties": False
                                    },
                                    "key_information": {
                                        "type": "array",
                                        "description": "Key information extracted from the document for eligibility assessment",
                                        "items": {"type": "string"}
                                    },
                                    "eligibility_relevance": {
                                        "type": "string",
                                        "description": "How this document supports or challenges eligibility"
                                    },
                                    "verification_status": {
                                        "type": "string",
                                        "description": "Document verification status",
                                        "enum": ["complete", "incomplete", "requires_additional_info"]
                                    }
                                },
                                "required": ["document_id", "document_type", "content", "key_information", "eligibility_relevance", "verification_status"],
                                "additionalProperties": False
                            }
                        },
                        "summary": {
                            "type": "object",
                            "description": "Overall summary of document processing results",
                            "properties": {
                                "total_documents": {
                                    "type": "integer",
                                    "description": "Total number of documents processed"
                                },
                                "supporting_evidence": {
                                    "type": "array",
                                    "description": "Key findings that support benefit eligibility",
                                    "items": {"type": "string"}
                                },
                                "potential_concerns": {
                                    "type": "array",
                                    "description": "Any issues, gaps, or discrepancies identified",
                                    "items": {"type": "string"}
                                },
                                "missing_information": {
                                    "type": "array",
                                    "description": "Required documents or data not yet provided",
                                    "items": {"type": "string"}
                                },
                                "recommendation": {
                                    "type": "string",
                                    "description": "Overall recommendation based on document processing",
                                    "enum": ["ready_for_decision", "need_additional_documents", "requires_manual_review"]
                                }
                            },
                            "required": ["total_documents", "supporting_evidence", "potential_concerns", "missing_information", "recommendation"],
                            "additionalProperties": False
                        }
                    },
                    "required": ["documents_processed", "summary"],
                    "additionalProperties": False
                }
            }
        }
    )
    
    system_message = """You are the Document Processing Agent responsible for retrieving and processing documents needed for benefit eligibility decisions.

**PRIMARY OBJECTIVE:** Retrieve requested documents by ID and provide structured output with document content for eligibility assessment.

**DOCUMENT PROCESSING WORKFLOW:**

1. **Document Retrieval**: Use get_document tool with provided document IDs (ONLY search by document ID)
2. **Content Analysis**: Review document content for relevant eligibility information
3. **Information Extraction**: Extract key data points needed for benefit decisions
4. **Structured Output**: Provide JSON response with document content and analysis

**DOCUMENT TYPES AND KEY INFORMATION:**

**Orders Document**
- Orders type (PCS, deployment, training)
- Effective dates and report dates
- From/to locations
- Service member name, rank, and branch
- Orders number and authorization
- Duration in days
- Deployment type classification

**Proof of Military Service**
- Service verification status
- Active duty status and branch
- Rank and military occupation
- Service start/end dates and duration
- Discharge type (for veterans)
- Combat service indicators
- Service-connected disabilities

**Leave and Earnings Statement (LES)**
- Pay period and compensation details
- Base pay, allowances, and deductions
- Net pay and total compensation
- Deployment allowances and special pay
- Service member identification

**Proof of Residence**
- Address verification status
- Lease details and monthly rent
- Residency duration
- Military housing status
- PCS impact assessment

**Loan Statement**
- Loan type and account details
- Original and current balances
- Monthly payment and interest rate
- Loan origination date
- Lender information
- Deferment eligibility
- Pre-service account status

**Financial Hardship Documentation**
- Hardship type and duration
- Monthly income vs expenses
- Deficit amount calculation
- Service connection verification
- Documentation provided
- Verification status

**Mortgage Documents**
- Mortgage type and account details
- Original loan amount and current balance
- Monthly payment and interest rate
- Property address
- Pre-service mortgage status
- SCRA eligibility

**Bank Statements**
- Bank name and account type
- Statement period and balances
- Overdraft fees and dates
- Deployment-related fee assessment
- Fee occurrence tracking

**Credit Statements**
- Credit card type and account details
- Current balance and credit limit
- APR and account opening date
- Issuer information
- Pre-service account status
- SCRA eligibility
- Payment history

**Account History**
- Account type and opening date
- Pre-service vs current balances
- APR changes and payment history
- SCRA application tracking

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
- **ONLY search by document ID** - use the get_document tool with provided document IDs
- Process ALL requested document IDs
- **Use the document content from the tool response** - the tool already provides the content
- Extract specific, actionable information from the document content
- Note both supporting and contradicting evidence
- Flag incomplete or suspicious documents
- **Provide structured JSON output** with analysis and summary
- Do not make eligibility decisions - only process and summarize documents
- **The tool provides content, you provide analysis**"""
    
    return AssistantAgent(
        name="Document_Processing_agent",
        description="Retrieves and processes documents required for benefit decisions",
        model_client=structured_model_client,
        model_context=UnboundedChatCompletionContext(),
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 