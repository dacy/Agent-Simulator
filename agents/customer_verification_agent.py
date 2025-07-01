"""
Customer Verification Agent for the Benefit Orchestrator System.
Handles customer identity verification with fuzzy matching capabilities.
"""

from typing import Dict, Any, List, Tuple
from autogen_agentchat.agents import AssistantAgent
from autogen_core.model_context import HeadAndTailChatCompletionContext
from autogen_core.tools import FunctionTool


# Customer search tool function embedded directly
def customer_search(ssn: str = "", name: str = "", address: str = "") -> str:
    """
    Intelligently searches for customers using various criteria with fuzzy matching and confidence scoring.
    
    Args:
        ssn (str): The customer's Social Security Number (can be partial, e.g., last 4 digits)
        name (str): The customer's full name (supports fuzzy matching)
        address (str): The customer's address (supports partial matching)
    
    Returns:
        str: A JSON string containing search results with confidence scores and match details
    """
    import json
    import difflib
    
    # Mock customers data (loaded from JSON files during team creation)
    MOCK_CUSTOMERS_DATA = [{'customerId': 'CUST-001', 'fullName': 'Ashlee Thompson', 'dateOfBirth': '1983-01-21', 'ssnLast4': '7583', 'email': 'kayla59@matthews.biz', 'phone': '824.057.7423x6297', 'address': {'street': '5896 Daniel Fort', 'city': 'Joshuahaven', 'state': 'AZ', 'zip': '94396'}, 'militaryStatus': 'Veteran', 'branch': 'Coast Guard', 'serviceStartDate': '2020-01-01', 'serviceEndDate': None}, {'customerId': 'CUST-002', 'fullName': 'Rachel Glover', 'dateOfBirth': '1994-09-19', 'ssnLast4': '8365', 'email': 'mendozanicholas@yahoo.com', 'phone': '824.447.7428x7274', 'address': {'street': '3595 Elizabeth Passage', 'city': 'South Mariaton', 'state': 'OH', 'zip': '59096'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2018-10-09', 'serviceEndDate': None}, {'customerId': 'CUST-003', 'fullName': 'Heather Mason', 'dateOfBirth': '1998-05-15', 'ssnLast4': '4674', 'email': 'stephen16@gmail.com', 'phone': '079-991-8795', 'address': {'street': '38232 Joseph Fords', 'city': 'Lake Todd', 'state': 'AZ', 'zip': '58315'}, 'militaryStatus': 'Active Duty', 'branch': 'Army', 'serviceStartDate': '2020-05-17', 'serviceEndDate': None}, {'customerId': 'CUST-004', 'fullName': 'Corey Lucas', 'dateOfBirth': '1993-01-11', 'ssnLast4': '5829', 'email': 'wilsonlisa@williams.info', 'phone': '+1-589-467-8480x428', 'address': {'street': '5266 Shaw Locks', 'city': 'East Melissamouth', 'state': 'MO', 'zip': '35641'}, 'militaryStatus': 'Reserve', 'branch': 'Army', 'serviceStartDate': '2015-03-03', 'serviceEndDate': None}, {'customerId': 'CUST-005', 'fullName': 'Kristopher Phillips', 'dateOfBirth': '1988-03-04', 'ssnLast4': '7025', 'email': 'kellywagner@travis.com', 'phone': '001-161-483-3768x76063', 'address': {'street': '8009 Snyder Radial', 'city': 'East Christyville', 'state': 'KY', 'zip': '48228'}, 'militaryStatus': 'Active Duty', 'branch': 'Marines', 'serviceStartDate': '2014-07-31', 'serviceEndDate': None}]
    
    customers = MOCK_CUSTOMERS_DATA
    search_results = []
    
    for customer in customers:
        confidence_factors = []
        total_confidence = 0
        max_possible_score = 0
        
        # SSN Matching (highest weight - 40%)
        if ssn:
            max_possible_score += 40
            ssn_clean = ssn.replace("-", "").replace(" ", "")
            customer_ssn = customer.get("ssnLast4", "")
            
            if ssn_clean and customer_ssn:
                if ssn_clean == customer_ssn:
                    confidence_factors.append(("SSN exact match", 40))
                    total_confidence += 40
                elif ssn_clean in customer_ssn or customer_ssn in ssn_clean:
                    confidence_factors.append(("SSN partial match", 25))
                    total_confidence += 25
        
        # Name Matching (30% weight)
        if name:
            max_possible_score += 30
            customer_name = customer.get("fullName", "").lower()
            search_name = name.lower()
            
            if customer_name and search_name:
                # Exact match
                if customer_name == search_name:
                    confidence_factors.append(("Name exact match", 30))
                    total_confidence += 30
                else:
                    # Fuzzy matching using difflib
                    similarity = difflib.SequenceMatcher(None, customer_name, search_name).ratio()
                    
                    if similarity >= 0.9:
                        score = int(30 * similarity)
                        confidence_factors.append((f"Name high similarity ({similarity:.2f})", score))
                        total_confidence += score
                    elif similarity >= 0.7:
                        score = int(25 * similarity)
                        confidence_factors.append((f"Name good similarity ({similarity:.2f})", score))
                        total_confidence += score
                    elif similarity >= 0.5:
                        score = int(15 * similarity)
                        confidence_factors.append((f"Name moderate similarity ({similarity:.2f})", score))
                        total_confidence += score
                    
                    # Also check if names contain each other (for partial matches)
                    name_parts = search_name.split()
                    customer_parts = customer_name.split()
                    common_parts = len(set(name_parts) & set(customer_parts))
                    if common_parts > 0:
                        part_score = min(15, common_parts * 5)
                        confidence_factors.append((f"Name parts match ({common_parts} parts)", part_score))
                        total_confidence += part_score
        
        # Address Matching (30% weight)
        if address:
            max_possible_score += 30
            customer_address = customer.get("address", {})
            if customer_address:
                full_customer_address = f"{customer_address.get('street', '')} {customer_address.get('city', '')} {customer_address.get('state', '')} {customer_address.get('zip', '')}".lower()
                search_address = address.lower()
                
                if search_address in full_customer_address or full_customer_address in search_address:
                    # Calculate partial match score based on how much of the address matches
                    if len(search_address) > 0:
                        match_ratio = min(len(search_address), len(full_customer_address)) / max(len(search_address), len(full_customer_address))
                        score = int(30 * match_ratio)
                        confidence_factors.append((f"Address partial match ({match_ratio:.2f})", score))
                        total_confidence += score
                
                # Check individual components
                address_components = search_address.split()
                matched_components = sum(1 for comp in address_components if comp in full_customer_address)
                if matched_components > 0:
                    component_score = min(20, matched_components * 5)
                    confidence_factors.append((f"Address components match ({matched_components})", component_score))
                    total_confidence += component_score
        
        # Calculate final confidence percentage
        if max_possible_score > 0:
            confidence_percentage = min(100, int((total_confidence / max_possible_score) * 100))
        else:
            confidence_percentage = 0
        
        # Only include results with some confidence
        if confidence_percentage > 0:
            search_results.append({
                "customer": customer,
                "confidence_percentage": confidence_percentage,
                "confidence_factors": confidence_factors,
                "match_summary": _generate_match_summary(confidence_factors)
            })
    
    # Sort by confidence (highest first)
    search_results.sort(key=lambda x: x["confidence_percentage"], reverse=True)
    
    # Prepare response
    response = {
        "search_criteria": {
            "ssn": ssn if ssn else None,
            "name": name if name else None,
            "address": address if address else None
        },
        "total_results": len(search_results),
        "results": search_results[:5]  # Return top 5 matches
    }
    
    return json.dumps(response, indent=2)

def _generate_match_summary(confidence_factors: List[Tuple[str, int]]) -> str:
    """Generate a human-readable summary of what matched"""
    if not confidence_factors:
        return "No specific matches found"
    
    summaries = [factor[0] for factor in confidence_factors]
    return "; ".join(summaries) 


def create_customer_verification_agent(mock_data: Dict[str, Any], model_client):
    """Create the Customer Verification Agent with tools."""
    
    tools = [
        FunctionTool(
            name="customer_search",
            description="Searches for a customer in the System of Record.",
            func=customer_search
        )
    ]
    
    system_message = """You are the Customer Verification Agent responsible for verifying customer identity using multiple data points with intelligent fuzzy matching.

**PRIMARY OBJECTIVE:** Verify the requestor's identity by searching customer records using available information (name, SSN, address, etc.) and determine if they are authorized to make this request.

**SEARCH CAPABILITIES:**

**1. Fuzzy Name Matching:**
- Uses similarity scoring for partial name matches
- Handles common variations (nicknames, middle names, etc.)
- Accounts for potential spelling errors or typos

**2. Partial SSN Support:**
- Can search with last 4 digits or full SSN
- Prioritizes full SSN matches but accepts partial matches with other confirmatory data

**3. Address Matching:**
- Matches individual address components (street, city, state, zip)
- Supports partial address searches
- Handles address format variations

**SEARCH STRATEGY SELECTION:**

**If you have full SSN + name:** Use SSN + name combination (highest confidence)
**If you have partial SSN + name:** Use SSN + name combination 
**If you have name + address:** Use name + address combination
**If you have only name:** Use name-only search (lowest confidence)
**If you have only SSN:** Use SSN-only search

**CONFIDENCE ASSESSMENT:**

**HIGH (80-100%):** Exact SSN match + name similarity >90%
**MEDIUM (60-79%):** SSN partial + good name + address match
**LOW (40-59%):** Name match + some address components
**INSUFFICIENT (<40%):** Recommend manual review

**SPOUSE SEARCH CAPABILITY:**
If the requestor is not found but mentions being a spouse, search for the service member's name to verify the family connection.

**OUTPUT FORMAT:**
```json
{
  "verification_result": "verified" | "not_found" | "ambiguous",
  "confidence_percentage": 85,
  "customer_id": "CUST-12345" | null,
  "customer_name": "John Doe",
  "actor": "self" | "spouse",
  "match_details": "SSN exact match; Name exact match",
  "search_strategy_used": "SSN + Name combination",
  "recommendation": "Proceed with high confidence" | "Manual review recommended" | "Additional verification needed"
}
```

**DECISION RULES:**
- **Verified**: Confidence ≥ 70% with clear primary identifier match
- **Ambiguous**: Multiple matches or confidence 50-69%
- **Not Found**: No matches or all matches below 50% confidence

**QUALITY STANDARDS:**
- Always attempt multiple search strategies if initial search fails
- Be transparent about match confidence and reasoning
- Recommend manual review for borderline cases
- Document specific factors that contributed to confidence score
- Never make assumptions - only report what the search tools reveal

**CRITICAL**: Only use the customer_search tool. Do not attempt to access customer data directly or make assumptions about customer identity."""
    
    return AssistantAgent(
        name="Customer_Verification_agent",
        description="Verifies customer identity and authorization to request benefits",
        model_client=model_client,
        model_context=HeadAndTailChatCompletionContext(head_size=1, tail_size=3),
        tools=tools,
        system_message=system_message,
        reflect_on_tool_use=True,
        model_client_stream=False,
        tool_call_summary_format="{result}"
    ) 