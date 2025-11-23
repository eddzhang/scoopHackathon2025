# NEXUS v3 - Multi-Round Adversarial Debate System

An AI-powered decision-making platform that simulates adversarial debates between Legal Counsel and Business Strategist agents to help startups navigate complex regulatory and business decisions. Built on SpoonOS with Anthropic Claude and blockchain-verified audit trails on NEO L1.

> **Demo-ready for hackathons** - Professional UI, real-time streaming, and immutable compliance records.

## 🎯 What It Does

Startups face tough decisions where legal compliance and business growth are in tension:
- Should we launch in the EU without full GDPR compliance?
- Can we classify contractors as independent workers?
- Should we accept crypto payments before getting licenses?
- Can we use customer data for AI training without explicit consent?

NEXUS runs a **3-round adversarial debate** between AI agents, then delivers a **Strategic Synthesis** with:
- ✅ Risk assessment (LOW/MEDIUM/HIGH)
- 💰 Cost of delay analysis
- 📊 Confidence score (65-85%)
- 🎯 Actionable decision roadmap
- 🔗 Blockchain-verified audit trail on NEO L1

**Why This Matters**: When regulators ask "how did you make this decision?", you have an immutable, timestamped record of your due diligence process.

## ✨ Features

- 🤖 **Three AI Agents**: Legal Counsel (risk-focused), Business Strategist (growth-focused), Strategic Synthesizer (decision-maker)
- ⚔️ **3-Round Debate System**: Opening arguments → Direct rebuttals → Final positions → Synthesis
- 📊 **Real-Time Decision Summary**: Live risk score, cost of delay, and confidence metrics
- 🔗 **Blockchain Audit Trail**: Every decision is cryptographically recorded on NEO L1 for compliance verification
- 🎯 **Context-Aware Agents**: Each round builds on previous arguments for genuine back-and-forth debate
- 💼 **Business-Ready**: Formatted outputs with actionable timelines and risk mitigation strategies
- ⚡ **Real-Time Streaming**: WebSocket-based live debate updates
- 🎨 **Professional UI**: Clean, modern interface with typing indicators and round tracking

## 🏗️ Architecture

### Agent System

**1. Legal Counsel** ⚖️ (Risk-Focused Advisor)
   - Identifies regulatory risks (GDPR, FinCEN, FTC, SEC, etc.)
   - Quantifies potential penalties realistically
   - Cites legal precedents and enforcement examples
   - **Verdict Options**: ⚖️ PROCEED WITH CAUTION | ❌ HIGH RISK - RECONSIDER | ✅ MANAGEABLE RISK

**2. Business Strategist** 📊 (Growth-Focused Advisor)
   - Analyzes market opportunity and competitive timing
   - Quantifies revenue potential and cost of delay
   - Cites competitor precedents (companies that moved fast)
   - Proposes risk mitigation strategies
   - **Verdict Options**: 🚀 SHIP NOW | 📊 PHASE ROLLOUT | ⏸️ NEEDS REFINEMENT

**3. Strategic Synthesizer** 🎯 (CEO-Level Decision Maker)
   - Reviews BOTH legal and business arguments
   - Weighs tradeoffs explicitly
   - Proposes phased approach balancing compliance with speed
   - Delivers structured decision:
     - 📊 **Risk Assessment**: HIGH/MEDIUM/LOW with reasoning
     - 💰 **Cost of Delay**: Quantified opportunity cost
     - 🎯 **Action Plan**: Numbered steps with timeline
     - 🤝 **Confidence Level**: 65-85%
     - ⚡ **Decision Speed**: Execute within X timeframe

### Debate Flow

```
User Query → Round 1: Opening Arguments (Legal + Business)
           → Round 2: Direct Rebuttals (agents respond to each other's specific points)
           → Round 3: Final Positions (agents review full debate history)
           → Synthesis: Strategic Synthesizer delivers verdict
           → Blockchain: Decision recorded on NEO L1 with SHA-256 hash
```

### Key Innovation: Context-Aware Rebuttals

Unlike simple multi-agent systems, NEXUS agents **actually respond to each other**:
- Round 2: Each agent receives opponent's Round 1 argument and must address specific points
- Round 3: Each agent sees full debate history and proposes concrete mitigation strategies
- Result: Genuine adversarial debate, not parallel monologues

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- pip or conda
- Anthropic API key ([get one here](https://console.anthropic.com/))

### Installation

1. **Clone the repository**:
```bash
git clone https://github.com/yourusername/scoopHackathon2025.git
cd scoopHackathon2025
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Required packages:
```txt
spoon-ai>=0.1.0
fastapi>=0.104.0
uvicorn>=0.24.0
websockets>=12.0
python-dotenv>=1.0.0
anthropicsdk>=0.8.0
```

3. **Set up environment variables**:
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Required
ANTHROPIC_API_KEY=sk-ant-api03-...

# Optional
USE_LLM=true
DEBUG=false
PORT=8001
```

4. **Start the server**:
```bash
python web_app_v3.py
```

5. **Open your browser**:
```
http://localhost:8001
```

## 💻 How to Use

### 1. Enter Your Business Decision

Be specific about context and constraints:
```
"Should we launch our MVP in the EU without full GDPR compliance? 
We have a 3-month window before competitors launch, representing $5M ARR potential. 
Our engineering team believes they can achieve 80% compliance now and iterate to 100% within 6 weeks."
```

### 2. Start the Debate

Click **"Start Multi-Round Debate"** and watch in real-time:
- 🟢 **Round 1**: Both agents present opening arguments (30-60 seconds each)
- 🔴 **Round 2**: Agents directly rebut each other's specific points
- 🟡 **Round 3**: Final positions considering all arguments
- 🎯 **Synthesis**: Strategic Synthesizer delivers verdict

### 3. Review the Decision Summary

The right sidebar updates dynamically:
- **Risk Score**: Color-coded (🔴 HIGH / 🟠 MEDIUM / 🟢 LOW)
- **Cost of Delay**: Quantified opportunity cost
- **Confidence Level**: How certain the recommendation is
- **Blockchain Hash**: Click to verify on NEO block explorer

### 4. Export or Share

The complete debate transcript and decision summary can be exported for:
- Board presentations
- Regulatory compliance documentation
- Internal decision logs

## 📝 Example Queries

### Data Privacy & AI
```
Should we use customer support chat logs to train our AI model without explicit consent?

Context:
- 3-month head start opportunity worth $500K
- Privacy policy has "service improvement" clause
- Doesn't specifically mention AI training
- Competitors like Intercom and Zendesk do this
```

**Expected Debate**:
- Legal: Cites GDPR Article 6, warns of €20M fines
- Business: Points to competitor precedents, proposes opt-out mechanism
- Synthesis: Recommends phased approach with consent update

### Cryptocurrency Payments
```
Should we start accepting cryptocurrency payments before getting money transmitter licenses?

Context:
- Each state license costs $50K and takes 9 months
- Could capture $2M ARR crypto-native market
- Coinbase operated this way for years
```

**Expected Debate**:
- Legal: Warns of FinCEN enforcement, cites BitMEX case
- Business: Argues first-mover advantage, proposes starting with non-MSB states
- Synthesis: Recommends soft launch in crypto-friendly states while pursuing licenses

### Employment Classification
```
Can we classify our 10 California engineers as independent contractors instead of employees?

Context:
- Would save $700K per year in benefits and equity
- Engineers work full-time, use our equipment
- Several tech giants leverage contractor models
```

**Expected Debate**:
- Legal: Cites AB5 test, warns of Uber/Lyft penalties
- Business: Proposes hybrid model with clear SOW boundaries
- Synthesis: Recommends employee classification with performance bonuses

### International Expansion
```
Should we launch our MVP in the EU without full GDPR compliance?

Context:
- 3-month window before competitors launch
- $5M ARR potential
- Engineering believes 80% compliance achievable now, 100% in 6 weeks
```

**Expected Debate**:
- Legal: Questions "80% compliance" validity, cites Article 25
- Business: Proposes UK soft launch (lighter enforcement) while completing EU compliance
- Synthesis: Recommends phased rollout starting with UK, full EU launch after 100% compliance

## 🔗 Web3 Integration - Blockchain Audit Trail

Every decision made through NEXUS is cryptographically recorded on the **NEO L1 blockchain**.

### Why Blockchain?

- 📜 **Compliance Proof**: If regulators ask "how did you decide?", you have immutable evidence
- 🔒 **Cannot Be Altered**: The decision reasoning is permanently timestamped
- 🔍 **Audit Trail**: Full debate history is hashed and stored on-chain
- ⚖️ **Legal Protection**: Demonstrates due diligence process for liability defense

### How It Works

1. **After Strategic Synthesizer completes**, the system creates an audit payload:
```json
{
  "timestamp": "2025-11-23T11:42:00Z",
  "query": "Should we launch MVP in EU without full GDPR...",
  "debate": {
    "round1": { "legal": "...", "business": "..." },
    "round2": { "legal_rebuttal": "...", "business_rebuttal": "..." },
    "round3": { "legal_final": "...", "business_final": "..." }
  },
  "synthesis": "Strategic Synthesizer verdict...",
  "decision": {
    "riskScore": "MEDIUM",
    "costOfDelay": "$500K/quarter",
    "confidence": "75%",
    "recommendation": "PROCEED WITH CAUTION"
  }
}
```

2. **Payload is hashed** using SHA-256

3. **Hash is submitted** to NEO L1 blockchain

4. **Transaction hash displayed** and clickable (links to NEO block explorer)

### Value Proposition

This creates an **immutable record** that the decision was made based on documented reasoning, which is valuable for:
- Regulatory audits (SEC, FTC, GDPR authorities)
- Board oversight and governance
- Insurance claims ("we did our due diligence")
- Internal compliance reviews

**Note**: Currently uses simulated blockchain submission. Can be connected to real NEO L1 with minimal changes to `blockchain_audit.py`.

## 🛠️ Tech Stack

### Core Technologies

- **Agent Orchestration**: [SpoonOS](https://spoonos.ai) - Python framework for multi-agent systems
- **LLM Provider**: [Anthropic Claude 3.5 Haiku](https://www.anthropic.com) - Fast, cost-effective model
- **Backend**: FastAPI + Python 3.10
- **Frontend**: HTML/CSS/JavaScript (Vanilla JS)
- **Real-Time**: WebSockets for live debate streaming
- **Blockchain**: NEO L1 for audit trail storage
- **Styling**: Custom CSS with modern design patterns

### Key Libraries

```python
spoon-ai          # Multi-agent orchestration
anthropicsdk      # Claude API integration  
fastapi           # Web framework
uvicorn           # ASGI server
websockets        # Real-time communication
python-dotenv     # Environment management
pydantic          # Data validation
```

### SpoonOS Components Used

**1. BaseAgent** - Foundation for debate agents
```python
class LLMDebateAgent(BaseAgent):
    async def step(self, run_id=None) -> str:
        # Generate LLM response
        response = await self.llm.llm_manager.chat(
            messages=llm_messages,
            provider="anthropic",
            model="claude-3-haiku-20240307",
            max_tokens=1000
        )
        return response.content
```

**2. ChatBot** - LLM integration
```python
llm = ChatBot(
    name="debate_agent",
    system_prompt=persona,
    llm_manager=LLMManager()
)
```

**3. Memory** - Conversation context
```python
self.memory = Memory()
await self.add_message("user", query)
await self.add_message("assistant", response)
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|--------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key | Yes | - |
| `USE_LLM` | Enable LLM-powered agents | No | `true` |
| `DEBUG` | Enable debug logging | No | `false` |
| `PORT` | Server port | No | `8001` |

### Rate Limits

Anthropic Claude Haiku rate limits (Tier 1):
- **50 requests per minute** (RPM)
- **50,000 tokens per minute** (TPM)

The system includes:
- 1-second delays between API calls
- Exponential backoff retry logic (2s, 4s, 6s)
- Automatic rate limit handling

### Agent Customization

To modify agent behavior, edit system prompts in `debate_orchestrator_llm.py`:

```python
# Legal Counsel persona
persona = """You are a pragmatic legal advisor focused on regulatory compliance..."""

# Business Strategist persona  
persona = """You are a business strategist focused on market opportunity..."""

# Strategic Synthesizer persona
persona = """You are a CEO-level decision maker who synthesizes..."""
```

### Performance Tuning

**Faster responses** (lower quality):
```python
model="claude-3-haiku-20240307",  # Already using fastest model
max_tokens=500  # Reduce from 1000
```

**Higher quality** (slower):
```python
model="claude-3-5-sonnet-20241022",  # Upgrade to Sonnet
max_tokens=2000  # Allow longer responses
```

## 📁 Project Structure

```
scoopHackathon2025/
├── agents/                      # Agent implementations
│   ├── paranoid_lawyer.py       # Original mock legal agent
│   └── growth_hacker.py         # Original mock growth agent
├── templates/                   # HTML templates
│   └── debate_v3.html           # Main debate UI
├── static/                      # Static assets
│   └── debate.js                # Frontend JavaScript
├── debate_orchestrator_llm.py   # LLM-powered debate system
│   ├── LLMDebateAgent           # Base agent class
│   ├── ParanoidLawyerLLM        # Legal Counsel agent
│   ├── GreedyFinanceLLM         # Business Strategist agent
│   ├── MediatorLLM              # Strategic Synthesizer agent
│   └── DebateOrchestratorLLM    # Main orchestration
├── blockchain_audit.py          # NEO L1 blockchain integration
├── web_app_v3.py                # FastAPI application with WebSockets
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (create from .env.example)
└── README.md                    # This file
```

## 🏆 Key Features Demonstrated

### For Hackathon Judges

This project showcases:

1. **Advanced Multi-Agent System**
   - Three specialized AI agents with distinct roles
   - Context-aware rebuttals (agents actually respond to each other)
   - 3-round debate structure with escalating complexity

2. **Real-Time Streaming Architecture**
   - WebSocket-based live updates
   - Typing indicators during API calls
   - Dynamic UI updates as debate progresses

3. **Production-Ready LLM Integration**
   - SpoonOS framework for agent orchestration
   - Anthropic Claude 3.5 Haiku for speed
   - Rate limit handling with exponential backoff
   - Retry logic for reliability

4. **Blockchain Integration**
   - SHA-256 hashing of debate transcripts
   - NEO L1 blockchain submission (simulated)
   - Clickable transaction hashes
   - Immutable compliance records

5. **Professional UX**
   - Clean, modern interface
   - Real-time decision summary updates
   - Color-coded risk indicators
   - Mobile-responsive design

6. **Business Value**
   - Solves real startup compliance dilemmas
   - Provides actionable recommendations
   - Creates audit trail for regulators
   - Demonstrates due diligence process

## 👥 Contributing

Contributions are welcome! Areas for improvement:

- [ ] Add more agent personas (CFO, CTO, etc.)
- [ ] Implement real NEO L1 blockchain integration
- [ ] Add PDF export of debate transcripts
- [ ] Support for multiple LLM providers
- [ ] Add debate history and session management
- [ ] Implement user authentication
- [ ] Add A/B testing for different agent prompts

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

- Built with [SpoonOS](https://spoonos.ai) for agent orchestration
- Powered by [Anthropic Claude](https://www.anthropic.com) 3.5 Haiku
- Blockchain verification via [NEO L1](https://neo.org)
- Inspired by real startup compliance challenges

## ⚠️ Disclaimer

This is a demonstration project for hackathon purposes. **Always consult qualified legal, tax, and compliance professionals for actual business decisions.** NEXUS provides analysis and recommendations but does not constitute legal advice.

## 📧 Contact

**Built for [Scoop Hackathon 2025]**

For questions or demo requests:
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---

<div align="center">

**🌟 Star this repo if you found it helpful!**

*Built with SpoonOS • Powered by Anthropic Claude • Verified on NEO L1*

</div>
