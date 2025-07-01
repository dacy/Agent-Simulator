# Agent Simulator

This project demonstrates a sophisticated multi-agent workflow for a mock SCRA (Servicemembers Civil Relief Act) benefit processing system. It showcases the power and flexibility of using structured prompts to coordinate specialized agents, serving as an advanced playground for exploring agent orchestration, workflow automation, and decision-making in a semi-realistic military benefit processing scenario using AutoGen Studio.

Military benefit processing workflow using AutoGen agents.

## Quick Start

1. **Generate JSON Configuration**
   ```bash
   python create_benefit_orchestrator.py
   ```

2. **Use with AutoGen Studio**
   - Install: `pip install -U autogenstudio`
   - Run: `autogenstudio ui --port 8081`
   - Open browser to `http://localhost:8081`
   - Toggle off visual builder to access JSON Editor
   - Paste contents of `generated_orchestrator.json`

## Configuration

**Mock Data**: Built into each agent file (embedded in the code)
```python
# Example from orchestrator_agent.py
MOCK_REQUESTS_DATA = [{'requestId': 'REQ-001', 'timestamp': '2025-06-30T21:50:27.064084Z', ...}]
```
**Agent Prompts**: Edit system messages in `agents/*.py` files
**Workflow Rules**: Modify `agents/orchestrator_agent.py`

## Architecture

**SelectorGroupChat Team**: Uses a ChatCompletion model to select the next speaker after each message. The team has simple routing logic due to AutoGen Studio limitations - all complex workflow decisions are handled by the Orchestrator Agent.



## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

