import json
import os

def read_file_content(file_path: str) -> str:
    """Read file content with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file_content(file_path: str, content: str) -> None:
    """Write file content with UTF-8 encoding."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_config():
    """Fix the combined orchestrator configuration."""
    
    # Read the configuration
    config = json.loads(read_file_content("combined_orchestrator.json"))
    
    # Process each agent
    for agent in config["config"]["participants"]:
        agent_label = agent.get("label", "Unknown Agent")
        
        # Look for matching tool file
        tool_file_path = None
        for filename in os.listdir("tools"):
            if filename.endswith('.py'):
                clean_name = filename[:-3].replace(' ', '_').replace('-', '_')
                agent_clean = agent_label.replace(' ', '_').replace('-', '_')
                if clean_name.lower() == agent_clean.lower():
                    tool_file_path = os.path.join("tools", filename)
                    break
        
        if tool_file_path and os.path.exists(tool_file_path):
            # Read tool source code
            tool_source = read_file_content(tool_file_path)
            
            # Update each tool in this agent
            for tool in agent["config"].get("tools", []):
                if tool.get("provider") == "autogen_core.tools.FunctionTool":
                    # Ensure description is present
                    if "description" not in tool:
                        tool["description"] = "Create custom tools by wrapping standard Python functions."
                    
                    tool_name = tool["config"]["name"]
                    
                    # Check if this tool's function exists in the source
                    if f"def {tool_name}(" in tool_source:
                        tool["config"]["source_code"] = tool_source
                        print(f"  - Updated source code for tool '{tool_name}' in agent '{agent_label}'")
    
    # Write the fixed configuration
    write_file_content("combined_orchestrator.json", json.dumps(config, indent=2))
    print("Successfully fixed combined_orchestrator.json")

if __name__ == "__main__":
    fix_config() 