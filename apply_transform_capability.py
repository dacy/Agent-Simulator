"""
AutoGen TransformMessages Capability Application
This script applies the TransformMessages capability to handle conversation history properly.
"""

import json
import copy
from typing import Dict, List

class RequestHistoryContextualizer:
    """
    Custom transformer that provides request details as context rather than conversation flow.
    This solves the issue where agents see history as conversational flow instead of contextual information.
    """
    
    def apply_transform(self, messages: List[Dict]) -> List[Dict]:
        """
        Transform messages to extract request details and provide them as context.
        """
        # Create a copy to avoid modifying original
        transformed_messages = copy.deepcopy(messages)
        
        # Look for request details in the conversation history
        request_details = self._extract_request_details(messages)
        
        if request_details and len(transformed_messages) > 0:
            # Add contextual information to the system message or most recent message
            context_summary = self._format_context_summary(request_details)
            
            # Inject context into the most recent user message
            if transformed_messages and transformed_messages[-1]["role"] == "user":
                original_content = transformed_messages[-1]["content"]
                transformed_messages[-1]["content"] = f"{original_content}\n\n**AVAILABLE CONTEXT:** {context_summary}"
        
        return transformed_messages
    
    def _extract_request_details(self, messages: List[Dict]) -> Dict:
        """Extract request details from conversation history."""
        request_details = {}
        
        for message in messages:
            content = message.get("content", "")
            if isinstance(content, str):
                # Look for JSON patterns that indicate request details
                if '"requestId"' in content and '"fullName"' in content:
                    # Try to extract the JSON
                    try:
                        import re
                        # Simple JSON extraction (this could be made more robust)
                        json_match = re.search(r'\{[^}]*"requestId"[^}]*\}', content)
                        if json_match:
                            try:
                                parsed = json.loads(json_match.group())
                                request_details.update(parsed)
                            except:
                                pass
                    except:
                        pass
                
                # Also look for key-value patterns
                if "Request ID:" in content or "requestId" in content:
                    lines = content.split('\n')
                    for line in lines:
                        if 'requestId' in line or 'Request ID' in line:
                            request_details['extracted_from_text'] = True
                        if 'fullName' in line or 'Full Name' in line:
                            request_details['extracted_from_text'] = True
        
        return request_details
    
    def _format_context_summary(self, request_details: Dict) -> str:
        """Format request details as context summary."""
        if not request_details:
            return "No request details found in conversation history."
        
        summary = "Request details are available in conversation history. "
        if 'requestId' in request_details:
            summary += f"Request ID: {request_details['requestId']}. "
        if 'fullName' in request_details:
            summary += f"Customer: {request_details['fullName']}. "
        if 'benefitType' in request_details:
            summary += f"Benefit: {request_details['benefitType']}. "
        
        summary += "DO NOT call get_request_details again - use existing context."
        return summary
    
    def get_logs(self, pre_transform_messages: List[Dict], post_transform_messages: List[Dict]) -> tuple:
        """Provide logs about the transformation."""
        context_added = len([m for m in post_transform_messages if "AVAILABLE CONTEXT:" in str(m.get("content", ""))]) > 0
        if context_added:
            return "Added request context from conversation history", True
        return "", False


def apply_transform_to_orchestrator():
    """
    Apply the TransformMessages capability to the orchestrator.
    Note: This is a conceptual example. In practice, you would need to integrate
    this with AutoGen's actual TransformMessages capability system.
    """
    
    # Load the current orchestrator
    with open('combined_orchestrator.json', 'r') as f:
        orchestrator = json.load(f)
    
    # Find the Request Analysis Agent
    request_analysis_agent = None
    for agent in orchestrator.get('team', {}).get('participants', []):
        if agent.get('config', {}).get('name') == 'Request_Analysis_agent':
            request_analysis_agent = agent
            break
    
    if not request_analysis_agent:
        print("Request Analysis Agent not found!")
        return
    
    # Add the transform configuration
    # Note: This is conceptual - actual implementation would use AutoGen's transform system
    transform_config = {
        "message_transforms": [
            {
                "provider": "custom.RequestHistoryContextualizer",
                "config": {
                    "extract_request_context": True,
                    "prevent_duplicate_retrieval": True
                }
            }
        ]
    }
    
    # The actual integration would happen through AutoGen's capability system
    print("✅ TransformMessages capability configuration created")
    print("📝 This would be applied through AutoGen's transform_messages.TransformMessages system")
    print("🔧 For actual implementation, integrate with AutoGen's built-in capability system")
    
    return transform_config


if __name__ == "__main__":
    print("🚀 AutoGen TransformMessages Capability Application")
    print("=" * 60)
    
    # Apply the transform capability
    config = apply_transform_to_orchestrator()
    
    print("\n📋 Transform Configuration:")
    print(json.dumps(config, indent=2))
    
    print("\n🔍 Next Steps:")
    print("1. Integrate this with AutoGen's TransformMessages capability")
    print("2. Test the conversation history handling")
    print("3. Monitor for duplicate get_request_details calls")
    
    print("\n✨ Benefits of this approach:")
    print("- Separates context from conversational flow")
    print("- Prevents duplicate request detail retrieval")
    print("- Maintains clean conversation history")
    print("- Uses AutoGen's built-in capabilities") 