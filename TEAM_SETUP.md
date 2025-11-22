# 🚀 Team Setup Guide - Nexus AI Council

## Quick Start for Team Members

### 1. Clone the Repository
```bash
git clone https://github.com/eddzhang/scoopHackathon2025.git
cd scoopHackathon2025
```

### 2. Set Up Python Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key or other LLM provider keys
```

### 4. Run the Application

#### Option A: Web Dashboard (Recommended)
```bash
python3 web_app.py
# Open http://localhost:8000 in your browser
```

#### Option B: Command Line
```bash
python3 nexus_council_standalone.py "Your compliance question"
```

#### Option C: Use the Launch Script
```bash
./run.sh
# Select option 2 for web dashboard
```

## 📁 Project Structure

- **`agents/`** - Three AI agents with distinct personas
- **`web_app.py`** - FastAPI web dashboard (main interface)
- **`nexus_council_standalone.py`** - Core deliberation engine
- **`web3_audit.py`** - Blockchain audit functionality

## 🎯 Key Features to Know

1. **Case File System** - 4 structured input fields for compliance queries
2. **Three AI Agents** - Legal, Tax, and Growth perspectives
3. **Real-time Debate** - Watch agents deliberate in the dashboard
4. **Audit Trail** - SHA-256 hashing for compliance records

## 🔧 For Developers

### Making Changes
```bash
git pull origin main  # Get latest changes
# Make your edits
git add .
git commit -m "Your change description"
git push origin main
```

### Areas to Enhance
- **Frontend**: The HTML is in `web_app.py` (lines 78-650)
- **Agent Logic**: Modify agents in `agents/` folder
- **Add New Agents**: Create new file in `agents/` and integrate in `nexus_council_standalone.py`
- **Blockchain**: Real implementation in `web3_audit.py`

## 💡 Tips
- The app works without SpoonOS installed (uses standalone version)
- Mock blockchain mode is enabled by default
- Test with the example hemp transport scenario for best demo

## 🐛 Troubleshooting
- **Port 8000 in use**: Kill existing process or change port in `web_app.py`
- **No OpenAI key**: The mock agents will still provide simulated responses
- **Import errors**: Make sure you activated the virtual environment

## 📞 Contact
For questions, check the README.md or create an issue on GitHub.

---
Happy Hacking! 🏛️
