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

        for agent in config_data.get('config', {}).get('participants', []):
            for tool in agent.get('config', {}).get('tools', []):
                # We inject the same source into all functions in a file,
                # as they rely on the same imports and context.
                if tool_file.startswith(agent.get("label")):
                    tool['config']['source_code'] = source_code
                    print(f"  - Injected source from '{tool_file}' into tool '{tool['config']['name']}' for agent '{agent['label']}'")


    # --- Step 2: Build and inject the function_map into the User Proxy Agent ---
    function_map = {}
    for tool_file in tool_files:
        module_name = os.path.splitext(tool_file)[0]
        spec = importlib.util.spec_from_file_location(module_name, os.path.join(tools_dir, tool_file))
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            for func_name, func_obj in module.__dict__.items():
                if callable(func_obj) and not func_name.startswith("__"):
                    function_map[func_name] = f"<{func_name}>" # Placeholder for studio
                    print(f"  - Mapped function '{func_name}'")

    # Find UserProxyAgent and inject the function map
    for agent in config_data.get('config', {}).get('participants', []):
        if agent.get("label") == "UserProxyAgent":
            if 'config' not in agent:
                agent['config'] = {}
            agent['config']['function_map'] = function_map
            print(f"\nSuccessfully injected function map into UserProxyAgent.")
            break

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
            # We use a trick to replace the placeholder strings with the unquoted function names
            # This is a bit of a hack to make it compatible with Studio's expectations
            json_str = json.dumps(config_data, indent=2, cls=CustomEncoder)
            for func_name in function_map:
                 json_str = json_str.replace(f'"<{func_name}>"', func_name)
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
                if clean_name.lower() == agent_clean.lower():
                    tool_file_path = os.path.join(tools_dir, filename)
                    break
        
        if tool_file_path and os.path.exists(tool_file_path):
            # Read tool source code
            tool_source = read_file_content(tool_file_path)
            
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