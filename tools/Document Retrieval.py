import json

def get_all_documents() -> str:
    """
    Returns a complete list of all available dummy documents for SCRA benefit verification.

    Returns:
        str: A JSON string representing the full list of dummy document records.
    """
    dummy_documents = [
        {
            "name": "lease_agreement.pdf",
            "extracted_content": {
                "type": "Lease Agreement",
                "address": "123 Patriot Way, Freedom City, USA",
                "tenant": "John M. Servicemember",
                "lease_start_date": "2023-01-15",
                "monthly_rent": 2500.00
            }
        },
        {
            "name": "drivers_license.jpg",
            "extracted_content": {
                "type": "Driver's License",
                "name": "John M. Servicemember",
                "dob": "1990-05-20",
                "address": "123 Patriot Way, Freedom City, USA",
                "license_number": "D12345678"
            }
        },
        {
            "name": "military_orders.pdf",
            "extracted_content": {
                "type": "Military Orders",
                "name": "John M. Servicemember",
                "rank": "Sergeant (E-5)",
                "branch": "U.S. Army",
                "orders_type": "Permanent Change of Station (PCS)",
                "report_date": "2022-08-01",
                "station": "Fort Liberty, NC"
            }
        },
        {
            "name": "dmdc_status_report.pdf",
            "extracted_content": {
                "type": "DMDC SCRA Status Report",
                "name": "John M. Servicemember",
                "ssn_last_4": "5678",
                "status_verified": True,
                "active_duty_start_date": "2022-08-01",
                "active_duty_end_date": None,
                "verification_date": "2024-06-30"
            }
        },
        {
            "name": "bank_statement_mar2024.pdf",
            "extracted_content": {
                "type": "Bank Statement",
                "account_holder": "John M. Servicemember",
                "account_number": "xxxx-xxxx-1234",
                "statement_period": "2024-03-01 to 2024-03-31",
                "payments_to_landlord": [
                    {"date": "2024-03-01", "amount": 2500.00}
                ]
            }
        }
    ]
    return json.dumps(dummy_documents) 


def get_document_content(documents_json: str, document_name: str) -> str:
    """
    Searches for a document within a given JSON list and returns its extracted content.

    This tool simulates retrieving structured data from a specific document
    from a list of documents provided to it.

    Args:
        documents_json (str): A JSON string representing a list of document objects.
        document_name (str): The filename of the document to retrieve. 
                             e.g., "lease_agreement.pdf", "military_orders.pdf"

    Returns:
        A JSON string of the extracted document content if found.
             Otherwise, a JSON string with an error message.
    """
    try:
        documents = json.loads(documents_json)
        if not isinstance(documents, list):
            raise TypeError("Input is not a list of documents.")
    except (json.JSONDecodeError, TypeError) as e:
        return json.dumps({"error": f"Invalid format for documents_json: {e}"})

    for doc in documents:
        if isinstance(doc, dict) and doc.get('name', '').lower() == document_name.lower():
            return json.dumps(doc.get('extracted_content', {}))
            
    return json.dumps({"error": f"Document '{document_name}' not found in the provided list."}) 