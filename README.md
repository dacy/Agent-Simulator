# Agent Simulator

This project demonstrates a sophisticated multi-agent workflow for a mock SCRA (Servicemembers Civil Relief Act) benefit processing system. It showcases the power and flexibility of using structured prompts to coordinate specialized agents, serving as an advanced playground for exploring agent orchestration, workflow automation, and decision-making in a semi-realistic military benefit processing scenario using AutoGen Studio.

![Demo](Demo.gif)

## Requirements

- Python 3.10+
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Quick Start

1. **Generate JSON Configuration**
   ```bash
   python create_benefit_orchestrator.py
   ```

2. **Use with AutoGen Studio**
   - Install: `pip install -U autogenstudio`
   - In AutoGen Studio, you can set up an environment variable OPENAI_API_KEY (assuming you are using OpenAI models) and AutoGen will automatically use this for any OpenAI model clients you specify for your agents or teams. Alternatively you can specify the api key as part of the team or agent configuration.
   - Run: `autogenstudio ui --port 8081`
   - Open browser to `http://localhost:8081`
   - Toggle off visual builder to access JSON Editor
   - Paste contents of `generated_orchestrator.json`

**Sample Request IDs for Testing:**
- `REQ-001`, `REQ-002`, `REQ-003`, `REQ-004`, `REQ-005`
Test data for these request IDs is embedded directly in the agent code.

## Configuration

**Mock Data**: Built into each agent file (embedded in the code)
```python
# Example from orchestrator_agent.py
MOCK_REQUESTS_DATA = [{'requestId': 'REQ-001', 'timestamp': '2025-06-30T21:50:27.064084Z', ...}]
```
**Agent Prompts**: Edit system messages in `agents/*.py` files
**Workflow Rules**: Modify `agents/orchestrator_agent.py`

## Architecture

The system is built around a modular team of specialized agents, each responsible for a distinct part of the SCRA benefit workflow:

- **Orchestrator Agent**: Central coordinator that interprets workflow state, applies business rules, and routes tasks to the appropriate agent using prompt-based logic.
 - **SelectorGroupChat Team**: Uses a 
ChatCompletion model to select the 
next speaker after each message. The 
team has simple routing logic due to 
AutoGen Studio limitations - all 
complex workflow decisions are 
handled by the Orchestrator Agent.
- **Verification, Document, Eligibility, Judge, Execution Agents**: Each agent handles a specific domain—customer verification, document retrieval/analysis, eligibility decision, quality/judgment, and benefit execution. Agents communicate via structured messages and are coordinated by the Orchestrator.

## Lessons Learned

###  Ambigous Rule Causing Inconsistent Decision

During testing, I discovered a critical challenge in LLM-based system: Unlike traditional programming where errors are immediately apparent, these systems can produce confident, well-structured responses that mask underlying inconsistencies:
- [Eligibility Decision Inconsistency Analysis Report](eligibility_decision_analysis_report.md) 

### Delegate Decsion to LLM?
When designing LLM-based multi-agent systems, a critical question arises: should complex decision logic be delegated to LLM reasoning or implemented as explicit tools? See below page for a very good example of assigning patents to emergency room, and it also proposed a hybrid approach - using tool to handle critical work and LLM for other.

- [Natural Language vs Tools Analysis](natural_language_vs_tools_analysis.md) 

### More Lessons Leanred

**AutoGen Studio Specific:**
- **{history} parameter only works for selector agents/orchestrators**, NOT for individual agent system messages
- **Individual agents must access conversation history** through the messages parameter in their reply functions
- **AutoGen agents with tools can get stuck in repetitive loops** if system messages don't explicitly prohibit duplicate calls
- **Context window size matters** - agents need sufficient context to see their own previous actions

**Structured Output:**
- **Structured output provides maximum reliability** for critical decision-making agents
- **OpenAI's internal JSON schema validation ensures consistent response formats** and prevents malformed outputs


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

