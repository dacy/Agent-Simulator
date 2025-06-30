import json
import difflib
from typing import Dict, List, Tuple

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
    
    # This will be replaced with actual mock data by combine_tools.py
    MOCK_CUSTOMERS_DATA = "{{MOCK_CUSTOMERS_DATA}}"
    
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