# 🏛️ NEXUS - AI General Counsel for Business Compliance

A cutting-edge multi-agent AI system built with the **SpoonOS framework** for business compliance deliberation. NEXUS employs three specialized AI agents that debate and provide comprehensive analysis on compliance questions.

## 🎯 Overview

NEXUS uses the SpoonOS Python framework to orchestrate three distinct AI agents:

### The Council Members

1. **Dr. Miranda Blackstone, Esq. (Legal Scholar)** ⚖️
   - Risk-averse lawyer with 20+ years of compliance experience
   - Specializes in GDPR, labor laws, and international regulations
   - Cites specific laws and blocks risky moves

2. **Harold P. Pennywhistle, CPA (Tax Comptroller)** 💰
   - Frugal accountant obsessed with tax optimization
   - Analyzes tax nexus implications and financial exposure
   - Calculates dollar-level impact of every decision

3. **Blake "Rocket" Morrison (Growth Hacker)** 🚀
   - Aggressive founder with "move fast" mentality
   - Prioritizes market capture over compliance
   - Pushes for rapid expansion and disruption

## 🏗️ Architecture

### SpoonOS Integration

The project demonstrates proper SpoonOS usage:

- **BaseAgent**: Each council member extends `BaseAgent` with custom `step()` implementations
- **StateGraph**: Orchestrates the debate workflow with parallel analysis and sequential debate rounds
- **GraphAgent**: Manages state preservation and execution across deliberations
- **Memory**: Maintains conversation context for each agent

### Workflow

1. **Parallel Analysis**: All three agents analyze the query simultaneously
2. **Debate Rounds**: Agents respond to each other's positions (2 rounds)
3. **Synthesis**: Final decision is synthesized from all perspectives
4. **Audit Trail**: SHA-256 hash generated for blockchain storage

## 🚀 Installation

### Prerequisites

- Python 3.10+
- SpoonOS framework
- OpenAI API key (or other LLM provider)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nexus-ai-counsel.git
cd nexus-ai-counsel
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Install SpoonOS (if not already installed):
```bash
pip install spoon-ai
```

## 💻 Usage

### Command Line Interface

Run a deliberation from the command line:

```bash
python nexus_council.py "Should we open an office in Germany with 5 employees?"
```

### Web Dashboard

Launch the interactive web dashboard:

```bash
python web_app.py
```

Then open http://localhost:8000 in your browser.

### API Endpoints

The FastAPI server provides REST endpoints:

```python
# Submit a query for deliberation
POST /api/debate
{
    "query": "Can we hire contractors in California?",
    "include_audit": true
}

# Mint audit trail to blockchain
POST /api/mint-audit
{
    "debate_hash": "0x...",
    "session_id": "uuid"
}

# Verify audit hash
GET /api/verify/{audit_hash}

# Get session details
GET /api/session/{session_id}
```

## 📋 Example Queries

- "Should we open an office in Germany with 5 employees?"
- "Can we hire contractors in California as a Delaware C-Corp?"
- "What are the tax implications of expanding to Texas?"
- "Should we process EU customer data in US servers?"
- "Can we launch our fintech product without licenses?"

## 🔐 Web3 Audit Trail

Every council decision generates an immutable audit trail:

1. **SHA-256 Hash**: Deterministic hash of the complete debate
2. **Blockchain Storage**: Mock implementation (can be connected to real Ethereum)
3. **Verification**: Audit trails can be independently verified

### Audit Report Format

```
NEXUS COMPLIANCE AUDIT REPORT
==============================
Generated: 2024-01-15T10:30:00
Debate Hash: 0x7f3a9b2c...
Blockchain TX: 0x9e8d7c6b...

DECISION SUMMARY
----------------
[Council's final decision]

CONSENSUS: YES/NO
DISSENTING OPINIONS
-------------------
• Legal Scholar: [Dissent if any]
• Tax Comptroller: [Dissent if any]

BLOCKCHAIN VERIFICATION
-----------------------
Contract: 0x742d35Cc...
Block Number: 18976543
Status: Success
```

## 🛠️ Technical Implementation

### SpoonOS Components Used

1. **BaseAgent** - Foundation for all council members
   ```python
   class LegalScholarAgent(BaseAgent):
       async def step(self, run_id=None) -> str:
           # Custom legal analysis logic
   ```

2. **StateGraph** - Workflow orchestration
   ```python
   graph = StateGraph(DebateState)
   graph.add_node("legal_analysis", ...)
   graph.add_edge("legal_analysis", "tax_analysis")
   ```

3. **GraphAgent** - Execution management
   ```python
   agent = GraphAgent("nexus_council", graph, preserve_state=True)
   ```

### State Management

The debate state is managed through TypedDict:

```python
class DebateState(TypedDict):
    user_query: str
    legal_analysis: Optional[str]
    tax_analysis: Optional[str]
    growth_analysis: Optional[str]
    debate_rounds: List[Dict[str, str]]
    final_decision: Optional[str]
    consensus: bool
    dissents: List[str]
    debate_hash: Optional[str]
```

## 🎮 Development

### Running Tests

```bash
pytest tests/
```

### Adding New Agents

1. Create new agent class extending `BaseAgent`
2. Implement `step()` method with analysis logic
3. Add to workflow in `nexus_council.py`

### Customizing Debate Logic

Modify the debate workflow in `_build_debate_graph()`:
- Add more debate rounds
- Change routing logic
- Implement parallel deliberation groups

## 📝 Project Structure

```
nexus-ai-counsel/
├── agents/                 # Council member implementations
│   ├── __init__.py
│   ├── legal_scholar.py    # Legal compliance agent
│   ├── tax_comptroller.py  # Tax analysis agent
│   └── growth_hacker.py    # Growth strategy agent
├── nexus_council.py        # Main orchestration with StateGraph
├── web3_audit.py          # Blockchain audit trail functionality
├── web_app.py             # FastAPI web application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🏆 Features Demonstrated

This project showcases:

- **Multi-Agent Orchestration**: Three agents with distinct personalities
- **SpoonOS StateGraph**: Complex workflow with parallel and sequential execution
- **Debate Simulation**: Agents respond to each other's analysis
- **Consensus Building**: Synthesis of multiple viewpoints
- **Audit Trail**: Blockchain-ready compliance logging
- **Web Dashboard**: Real-time visualization of deliberation
- **REST API**: Programmatic access to council

## 🔧 Configuration

### Environment Variables

```bash
# LLM Configuration
SPOON_LLM_PROVIDER=openai
SPOON_OPENAI_API_KEY=your_key

# Web3 (optional)
ETH_RPC_URL=https://eth-sepolia.public.blastapi.io
PRIVATE_KEY=your_ethereum_private_key

# Application
DEBUG=false
PORT=8000
```

### LLM Providers

Supports multiple LLM providers through SpoonOS:
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Local models via Ollama

## 📄 License

MIT License - Built for hackathon demonstration

## 🙏 Acknowledgments

- Built with [SpoonOS](https://github.com/XSpoonAI/spoon-core) framework
- Inspired by corporate governance best practices
- Designed for real-world compliance scenarios

## 🚨 Disclaimer

This is a hackathon project for demonstration purposes. Always consult qualified legal and tax professionals for actual business compliance decisions.

---

**Built with SpoonOS** - The Python framework for multi-agent AI systems
