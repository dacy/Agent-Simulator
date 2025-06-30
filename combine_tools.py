import json
import argparse
import os
import importlib.util
from typing import Dict, Any

def read_file_content(file_path: str) -> str:
    """Read file content with UTF-8 encoding."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file_content(file_path: str, content: str) -> None:
    """Write file content with UTF-8 encoding."""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def load_mock_data(mock_data_dir: str = "mock-data") -> Dict[str, Any]:
    """Load all mock data files from the mock-data directory."""
    mock_data = {}
    
    if not os.path.exists(mock_data_dir):
        print(f"Warning: Mock data directory '{mock_data_dir}' not found. Using empty data.")
        return mock_data
    
    # Load customers data
    customers_file = os.path.join(mock_data_dir, "customers.json")
    if os.path.exists(customers_file):
        try:
            with open(customers_file, 'r', encoding='utf-8') as f:
                mock_data['customers'] = json.load(f)
            print(f"  - Loaded {len(mock_data['customers'])} customers from {customers_file}")
        except Exception as e:
            print(f"Warning: Could not load customers data: {e}")
            mock_data['customers'] = []
    
    # Load documents data
    documents_file = os.path.join(mock_data_dir, "documents.json")
    if os.path.exists(documents_file):
        try:
            with open(documents_file, 'r', encoding='utf-8') as f:
                mock_data['documents'] = json.load(f)
            print(f"  - Loaded {len(mock_data['documents'])} documents from {documents_file}")
        except Exception as e:
            print(f"Warning: Could not load documents data: {e}")
            mock_data['documents'] = []
    
    # Load requests data
    requests_file = os.path.join(mock_data_dir, "requests.json")
    if os.path.exists(requests_file):
        try:
            with open(requests_file, 'r', encoding='utf-8') as f:
                mock_data['requests'] = json.load(f)
            print(f"  - Loaded {len(mock_data['requests'])} requests from {requests_file}")
        except Exception as e:
            print(f"Warning: Could not load requests data: {e}")
            mock_data['requests'] = []
    
    return mock_data

def inject_mock_data_into_source(source_code: str, mock_data: Dict[str, Any]) -> str:
    """Replace mock data placeholders in source code with actual data as valid Python code."""
    modified_source = source_code
    
    # Replace placeholders with actual mock data as Python code (not JSON)
    if '{{MOCK_CUSTOMERS_DATA}}' in modified_source:
        customers_python = repr(mock_data.get('customers', []))
        modified_source = modified_source.replace('"{{MOCK_CUSTOMERS_DATA}}"', customers_python)
        print(f"    - Injected {len(mock_data.get('customers', []))} customers into source code")
    
    if '{{MOCK_DOCUMENTS_DATA}}' in modified_source:
        documents_python = repr(mock_data.get('documents', []))
        modified_source = modified_source.replace('"{{MOCK_DOCUMENTS_DATA}}"', documents_python)
        print(f"    - Injected {len(mock_data.get('documents', []))} documents into source code")
    
    if '{{MOCK_REQUESTS_DATA}}' in modified_source:
        requests_python = repr(mock_data.get('requests', []))
        modified_source = modified_source.replace('"{{MOCK_REQUESTS_DATA}}"', requests_python)
        print(f"    - Injected {len(mock_data.get('requests', []))} requests into source code")
    
    return modified_source

def update_agent_format(agent: Dict[str, Any]) -> Dict[str, Any]:
    """Update agent to match the correct AutoGen Studio format."""
    config = agent.get("config", {})
    
    # Add required description at top level if not present
    if "description" not in agent:
        agent["description"] = config.get("description", "An agent that provides assistance with tool use.")
    
    # Add required fields to config if not present
    if "model_client_stream" not in config:
        config["model_client_stream"] = False
    if "reflect_on_tool_use" not in config:
        config["reflect_on_tool_use"] = False
    if "tool_call_summary_format" not in config:
        config["tool_call_summary_format"] = "{result}"
    if "metadata" not in config:
        config["metadata"] = {}
    
    # Update model_client format
    if "model_client" in config:
        model_client = config["model_client"]
        if "component_type" not in model_client:
            model_client["component_type"] = "model"
        if "version" not in model_client:
            model_client["version"] = 1
        if "component_version" not in model_client:
            model_client["component_version"] = 1
        if "description" not in model_client:
            model_client["description"] = "Chat completion client for OpenAI hosted models."
        if "label" not in model_client:
            model_client["label"] = "OpenAIChatCompletionClient"
    
    # Update model_context format
    if "model_context" in config:
        model_context = config["model_context"]
        if "component_type" not in model_context:
            model_context["component_type"] = "chat_completion_context"
        if "version" not in model_context:
            model_context["version"] = 1
        if "component_version" not in model_context:
            model_context["component_version"] = 1
        if "description" not in model_context:
            model_context["description"] = "An unbounded chat completion context that keeps a view of the all the messages."
        if "label" not in model_context:
            model_context["label"] = "UnboundedChatCompletionContext"
    
    # Update tools format
    if "tools" in config:
        for tool in config["tools"]:
            if tool.get("provider") == "autogen_core.tools.FunctionTool":
                if "description" not in tool:
                    tool["description"] = "Create custom tools by wrapping standard Python functions."
    
    return agent

def combine_and_prepare_tools(config_path: str, tools_dir: str, output_path: str):
    """
    Scans for tool files, injects their source code into the appropriate agent's
    tool definition, dynamically creates a function_map for the UserProxyAgent,
    and saves the final, complete configuration.
    """
    print(f"Reading configuration from: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        return
    except json.JSONDecodeError as e:
        print(f"Error: Could not decode JSON from {config_path}: {e}")
        return

    if not os.path.isdir(tools_dir):
        print(f"Error: Tools directory not found at '{tools_dir}'")
        return

    # Load mock data
    print("Loading mock data...")
    mock_data = load_mock_data()

    print(f"Scanning for tools in: {tools_dir}")
    tool_files = [f for f in os.listdir(tools_dir) if f.endswith('.py')]

    # --- Step 1: Inject source code into assistant tool definitions ---
    for tool_file in tool_files:
        tool_file_path = os.path.join(tools_dir, tool_file)
        try:
            with open(tool_file_path, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except IOError as e:
            print(f"Warning: Could not read tool file {tool_file_path}. Skipping. Error: {e}")
            continue

        # Inject mock data into source code
        print(f"  - Processing {tool_file}:")
        source_code = inject_mock_data_into_source(source_code, mock_data)

        for agent in config_data.get('config', {}).get('participants', []):
            for tool in agent.get('config', {}).get('tools', []):
                # We inject the same source into all functions in a file,
                # as they rely on the same imports and context.
                # Match tool file name (without .py) to agent label
                tool_name_clean = tool_file[:-3] if tool_file.endswith('.py') else tool_file
                agent_label = agent.get("label", "")
                
                # Check if agent label starts with tool file name
                if agent_label.startswith(tool_name_clean):
                    tool['config']['source_code'] = source_code
                    print(f"  - Injected source from '{tool_file}' into tool '{tool['config']['name']}' for agent '{agent['label']}'")


    # --- Step 2: UserProxyAgent is for user input only, no function mapping needed ---
    print("UserProxyAgent configured for user input collection (no function mapping required)")

    # --- Step 3: Write the final combined file ---
    print(f"Writing combined configuration to: {output_path}")
    try:
        # Use a custom encoder to handle function objects if we weren't using placeholders
        class CustomEncoder(json.JSONEncoder):
            def default(self, obj):
                if callable(obj):
                    return f"<function {obj.__name__}>"
                return json.JSONEncoder.default(self, obj)

        with open(output_path, 'w', encoding='utf-8') as f:
            # Write clean JSON without function_map hacks
            json_str = json.dumps(config_data, indent=2, cls=CustomEncoder)
            f.write(json_str)

        print("Successfully created combined_orchestrator.json")
    except IOError as e:
        print(f"Error writing to output file {output_path}: {e}")

def combine_tools():
    """Combine tools from separate files into the main orchestrator configuration."""
    
    # Configuration
    config_file = "benefit orchestrator.json"
    tools_dir = "tools"
    output_file = "combined_orchestrator.json"
    
    print(f"Reading configuration from: {config_file}")
    
    # Read base configuration
    config = json.loads(read_file_content(config_file))
    
    # Load mock data
    print("Loading mock data...")
    mock_data = load_mock_data()
    
    print(f"Scanning for tools in: {tools_dir}")
    
    # Process each agent
    for agent in config["config"]["participants"]:
        agent_name = agent["config"]["name"]
        label = agent.get("label", "Unknown Agent")
        
        # Update agent format to match AutoGen Studio requirements
        agent = update_agent_format(agent)
        
        # Look for matching tool file
        tool_file_path = None
        for filename in os.listdir(tools_dir):
            if filename.endswith('.py'):
                clean_name = filename[:-3].replace(' ', '_').replace('-', '_')
                agent_clean = label.replace(' ', '_').replace('-', '_')
                # Check if agent label starts with tool file name (handles cases like "Request_Analysis" vs "Request_Analysis_Agent")
                if agent_clean.lower().startswith(clean_name.lower()):
                    tool_file_path = os.path.join(tools_dir, filename)
                    break
        
        if tool_file_path and os.path.exists(tool_file_path):
            # Read tool source code
            tool_source = read_file_content(tool_file_path)
            
            # Inject mock data into source code
            print(f"  - Processing {os.path.basename(tool_file_path)}:")
            tool_source = inject_mock_data_into_source(tool_source, mock_data)
            
            # Update each tool in this agent
            for tool in agent["config"].get("tools", []):
                if tool.get("provider") == "autogen_core.tools.FunctionTool":
                    tool_name = tool["config"]["name"]
                    
                    # Check if this tool's function exists in the source
                    if f"def {tool_name}(" in tool_source:
                        tool["config"]["source_code"] = tool_source
                        print(f"  - Injected source from '{os.path.basename(tool_file_path)}' into tool '{tool_name}' for agent '{label}'")
            
            # Create function mappings for any functions in the source
            import ast
            try:
                tree = ast.parse(tool_source)
                for node in tree.body:
                    if isinstance(node, ast.FunctionDef):
                        print(f"  - Mapped function '{node.name}'")
            except:
                pass
    
    # Write the combined configuration
    write_file_content(output_file, json.dumps(config, indent=2))
    print(f"Successfully created {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Combine Python tool source files and create a function map for AutoGen Studio."
    )
    parser.add_argument("--config-json", default="benefit orchestrator.json")
    parser.add_argument("--tools-dir", default="tools")
    parser.add_argument("--output-json", default="combined_orchestrator.json")
    args = parser.parse_args()
    combine_and_prepare_tools(args.config_json, args.tools_dir, args.output_json)
    combine_tools() 