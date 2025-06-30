import json

def customer_search(ssn: str, name: str, address: str) -> str:
    """Searches for customers in a dummy list of customers using their SSN, name, or address and returns all matches.

    Args:
        ssn (str): The customer's Social Security Number.
        name (str): The customer's full name.
        address (str): The customer's address.

    Returns:
        str: A JSON string representing a list of matched customer objects. Returns an empty list '[]' if no matches are found."""
    dummy_customers = [
        {"ssn": "123-45-678", "name": "John Smith", "address": "123 Fake St, Anytown, USA"},
        {"ssn": "987-65-432", "name": "Alice Wonderland", "address": "456 Rabbit Hole, Fantasyland"},
        {"ssn": "111-22-333", "name": "Bob Builder", "address": "789 Construction Zone"}
    ]

    matched_customers = []
    for customer in dummy_customers:
        if customer["ssn"] == ssn or customer["name"].lower() == name.lower() or customer["address"].lower() == address.lower():
            matched_customers.append(customer)

    return json.dumps(matched_customers) 