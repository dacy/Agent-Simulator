# Agent Simulator - Military Benefit Processing Workflow

A sophisticated multi-agent system for processing military and veteran benefit requests using AutoGen Studio. This system demonstrates intelligent workflow orchestration with natural language understanding, structured decision-making, and flexible user interaction.

## 🎯 Overview

The Agent Simulator processes military benefit requests through a comprehensive workflow that includes customer verification, document processing, eligibility assessment, quality control, user approval, and benefit execution. The system uses OpenAI's structured output capabilities for reliable decision-making and supports dynamic user input handling.

## 🏗️ Architecture

### Core Components

- **Request Analysis Agent**: Workflow orchestrator with intelligent routing and natural language understanding
- **Customer Verification Agent**: Identity verification with fuzzy matching and confidence scoring
- **Document Processing Agent**: Document retrieval and content analysis
- **Eligibility Decision Agent**: Military benefit eligibility assessment with comprehensive rules
- **Judge Agent**: Quality control and workflow compliance assessment
- **User Proxy Agent**: Dynamic user interaction and input collection
- **Benefit Execution Agent**: Final benefit activation or decline notification

### Key Features

✅ **Intelligent Workflow Orchestration**: Natural language understanding for flexible user interaction  
✅ **Structured Output**: OpenAI JSON schemas for reliable decision-making  
✅ **Fuzzy Matching**: Advanced customer verification with confidence scoring  
✅ **Quality Control**: Automated workflow compliance assessment  
✅ **Dynamic User Input**: Flexible handling of various user instructions and requests  
✅ **Mock Data System**: Comprehensive test data for development and testing  
✅ **AutoGen Studio Ready**: Complete JSON configuration for immediate deployment  

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenAI API key
- AutoGen Studio 0.4.2+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd "Agent Simulator"
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install autogen-agentchat autogen-core autogen-ext
   ```

4. **Configure OpenAI API key**
   ```bash
   set OPENAI_API_KEY=your_api_key_here  # Windows
   # or
   export OPENAI_API_KEY=your_api_key_here  # Linux/Mac
   ```

5. **Generate orchestrator configuration**
   ```bash
   python create_benefit_orchestrator.py
   ```

### Usage

1. **Import to AutoGen Studio**
   - Open AutoGen Studio
   - Import the generated `generated_orchestrator.json` file
   - The complete team configuration will be loaded

2. **Start a conversation**
   - Provide a request ID (e.g., "REQ-001")
   - The system will automatically process the request through the workflow

## 📋 Workflow Process

### 1. Request Analysis
- **Input**: Request ID from user
- **Action**: Retrieves request details and routes to customer verification
- **Output**: Complete request information

### 2. Customer Verification
- **Input**: Requestor information
- **Action**: Fuzzy matching against customer database
- **Output**: Verification result with confidence score

### 3. Document Processing
- **Input**: Document requests from other agents
- **Action**: Retrieves and analyzes document content
- **Output**: Document information and analysis

### 4. Eligibility Decision
- **Input**: Customer verification and document data
- **Action**: Applies military benefit eligibility rules
- **Output**: APPROVED/DECLINED decision with justification

### 5. Quality Assessment
- **Input**: Eligibility decision and workflow data
- **Action**: Evaluates decision quality and compliance
- **Output**: Quality score and recommendation

### 6. User Approval
- **Input**: Decision and quality assessment
- **Action**: Presents decision to user for approval
- **Output**: User agreement or additional instructions

### 7. Benefit Execution
- **Input**: Final approved decision
- **Action**: Executes benefit activation or sends decline notification
- **Output**: Execution confirmation

## 🎛️ Supported Benefits

- **Auto Loan Deferment**: Active duty with PCS/deployment orders
- **Foreclosure Protection (SCRA)**: Active duty mortgage protection
- **Overdraft Fee Refund**: Active duty fee refunds during deployment
- **Credit Card APR Reduction**: SCRA APR reduction to 6%

## 🔧 Configuration

### Agent Configuration Files

- `agents/request_analysis_agent.py` - Workflow orchestration
- `agents/customer_verification_agent.py` - Identity verification
- `agents/document_processing_agent.py` - Document handling
- `agents/eligibility_decision_agent.py` - Eligibility assessment
- `agents/judge_agent.py` - Quality control
- `agents/user_proxy_agent.py` - User interaction
- `agents/benefit_execution_agent.py` - Benefit execution

### Mock Data

- `mock-data/customers.json` - Customer database
- `mock-data/documents.json` - Document repository
- `mock-data/requests.json` - Benefit requests

## 🧪 Testing

### Sample Request IDs

- `REQ-001` - Auto Loan Deferment (Veteran)
- `REQ-002` - Foreclosure Protection (Reserve)
- `REQ-003` - Overdraft Fee Refund (Active Duty)
- `REQ-004` - Foreclosure Protection (Reserve)
- `REQ-005` - Credit Card APR Reduction (Active Duty)

### Test Scenarios

1. **Standard Approval Flow**: Use any REQ-* ID for normal processing
2. **User Disagreement**: Disagree with decision to test correction flow
3. **Document Requests**: Agents will request missing documents automatically
4. **Customer Recheck**: Ask to "recheck customer" to test verification flow

## 🔍 Advanced Features

### Intelligent User Input Handling

The system supports various types of user input:

- **Agreement**: "Yes", "I agree", "Proceed", etc.
- **Disagreement**: "No", "I disagree", "Change this", etc.
- **Instructions**: "Recheck customer", "Review documents", "Add information"
- **Questions**: "Why was this declined?", "What documents are needed?"
- **Corrections**: "The customer is actually active duty", "Add missing document"

### Structured Output Benefits

- **Reliable JSON**: OpenAI guarantees valid response format
- **Schema Validation**: Strict validation prevents malformed responses
- **Consistent Format**: Standardized output across all agents
- **Error Prevention**: Clear validation rules and constraints

### Quality Control System

- **Workflow Compliance**: Ensures all required steps are completed
- **Decision Quality**: Evaluates decision reasoning and documentation
- **Risk Assessment**: Identifies potential issues or inconsistencies
- **Recommendation Engine**: Provides guidance for next steps

## 🛠️ Development

### Adding New Benefits

1. Update eligibility rules in `eligibility_decision_agent.py`
2. Add benefit-specific document requirements
3. Update mock data with new benefit types
4. Test with new request scenarios

### Extending Agent Capabilities

1. Modify agent system messages for new functionality
2. Add new tools to agent configurations
3. Update workflow rules in request analysis agent
4. Regenerate orchestrator configuration

### Customizing Workflow

1. Edit workflow rules in `request_analysis_agent.py`
2. Modify routing logic and conditions
3. Add new agents or modify existing ones
4. Update termination conditions

## 📊 Performance

- **Response Time**: Typically 2-5 seconds per agent interaction
- **Accuracy**: High confidence scoring for customer verification
- **Reliability**: Structured output prevents JSON parsing errors
- **Scalability**: Modular design supports easy expansion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly with mock data
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues or questions:

1. Check the workflow rules in `request_analysis_agent.py`
2. Verify OpenAI API key configuration
3. Ensure all dependencies are installed
4. Test with sample request IDs

## 🔄 Version History

- **v1.0.0**: Initial release with complete benefit processing workflow
- **v1.1.0**: Added structured output and intelligent user input handling
- **v1.2.0**: Enhanced quality control and workflow compliance
- **v1.3.0**: Improved agentic flow and natural language understanding

---

**Ready to deploy?** Import `generated_orchestrator.json` into AutoGen Studio and start processing benefit requests! 