"""
FastAPI web application for Nexus AI Adversarial System
Dark mode UI with real-time debate visualization
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
import uuid
import hashlib

# Import our adversarial agents
from agents.paranoid_lawyer import ParanoidLawyerAgent
from agents.greedy_finance import GreedyFinanceAgent
from agents.mediator import MediatorAgent


# Pydantic models
class QueryRequest(BaseModel):
    query: str


class DebateMessage(BaseModel):
    agent: str
    color: str
    content: str
    timestamp: str


class DebateResponse(BaseModel):
    session_id: str
    messages: List[DebateMessage]
    summary: Dict[str, Any]
    audit_hash: str


# Initialize FastAPI
app = FastAPI(
    title="Nexus Adversarial System",
    description="Watch AI agents with opposing objectives debate your decisions",
    version="2.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
paranoid_lawyer = ParanoidLawyerAgent()
greedy_finance = GreedyFinanceAgent()
mediator = MediatorAgent()
sessions = {}


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the adversarial debate interface"""
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXUS - Adversarial Legal Reasoning</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI', sans-serif;
            background: #0f172a;
            color: #e2e8f0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
            padding: 24px 32px;
            border-bottom: 1px solid #334155;
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .logo h1 {
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .logo-subtitle {
            font-size: 14px;
            color: #64748b;
            margin-top: 4px;
        }
        
        .live-badge {
            display: none;
            padding: 6px 16px;
            background: #ef4444;
            color: white;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            animation: pulse 2s infinite;
        }
        
        .live-badge.active {
            display: block;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }
        
        .main-container {
            flex: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 32px;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 380px;
            gap: 32px;
        }
        
        .debate-section {
            display: flex;
            flex-direction: column;
            gap: 24px;
        }
        
        .input-card {
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
        }
        
        .input-label {
            font-size: 14px;
            font-weight: 600;
            color: #94a3b8;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .query-input {
            width: 100%;
            padding: 16px;
            background: #0f172a;
            border: 2px solid #334155;
            border-radius: 8px;
            color: #e2e8f0;
            font-size: 15px;
            font-family: inherit;
            resize: vertical;
            min-height: 100px;
            transition: all 0.2s;
        }
        
        .query-input:focus {
            outline: none;
            border-color: #6366f1;
            background: #1a202c;
        }
        
        .query-input::placeholder {
            color: #475569;
        }
        
        .example-chips {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 12px;
        }
        
        .example-chip {
            padding: 6px 12px;
            background: #334155;
            border: 1px solid #475569;
            border-radius: 20px;
            font-size: 12px;
            color: #94a3b8;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .example-chip:hover {
            background: #475569;
            color: #e2e8f0;
            transform: translateY(-1px);
        }
        
        .debate-btn {
            width: 100%;
            padding: 16px;
            margin-top: 16px;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .debate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
        }
        
        .debate-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .debate-theater {
            background: #1e293b;
            border-radius: 12px;
            border: 1px solid #334155;
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            height: 600px;
        }
        
        .theater-header {
            padding: 20px 24px;
            background: #0f172a;
            border-bottom: 1px solid #334155;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .debate-messages {
            flex: 1;
            padding: 24px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        
        .debate-message {
            animation: slideIn 0.3s ease-out;
        }
        
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        
        .message-header {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-bottom: 8px;
        }
        
        .agent-icon {
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
        }
        
        .agent-icon.lawyer {
            background: #ef4444;
        }
        
        .agent-icon.finance {
            background: #22c55e;
        }
        
        .agent-icon.mediator {
            background: #6366f1;
        }
        
        .agent-name {
            font-weight: 600;
            font-size: 14px;
        }
        
        .message-time {
            color: #64748b;
            font-size: 12px;
            margin-left: auto;
        }
        
        .message-content {
            padding: 16px;
            background: #0f172a;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
            border-left: 3px solid;
        }
        
        .message-content.lawyer {
            border-color: #ef4444;
        }
        
        .message-content.finance {
            border-color: #22c55e;
        }
        
        .message-content.mediator {
            border-color: #6366f1;
        }
        
        .summary-panel {
            background: #1e293b;
            border-radius: 12px;
            padding: 24px;
            border: 1px solid #334155;
        }
        
        .summary-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #cbd5e1;
        }
        
        .summary-item {
            margin-bottom: 20px;
        }
        
        .summary-label {
            font-size: 12px;
            color: #64748b;
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .summary-value {
            font-size: 24px;
            font-weight: 700;
        }
        
        .risk-score {
            padding: 8px 16px;
            border-radius: 6px;
            display: inline-block;
            font-size: 18px;
        }
        
        .risk-low {
            background: rgba(34, 197, 94, 0.2);
            color: #22c55e;
        }
        
        .risk-medium {
            background: rgba(234, 179, 8, 0.2);
            color: #eab308;
        }
        
        .risk-high {
            background: rgba(239, 68, 68, 0.2);
            color: #ef4444;
        }
        
        .confidence-bar {
            height: 8px;
            background: #334155;
            border-radius: 4px;
            overflow: hidden;
            margin-top: 8px;
        }
        
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            transition: width 0.5s ease-out;
        }
        
        .audit-hash {
            margin-top: 24px;
            padding: 16px;
            background: #0f172a;
            border-radius: 8px;
            border: 1px solid #334155;
        }
        
        .hash-label {
            font-size: 11px;
            color: #64748b;
            margin-bottom: 8px;
            text-transform: uppercase;
        }
        
        .hash-value {
            font-family: 'Courier New', monospace;
            font-size: 12px;
            color: #94a3b8;
            word-break: break-all;
        }
        
        .welcome-message {
            text-align: center;
            color: #64748b;
            padding: 40px;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #334155;
            border-top-color: #6366f1;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        @media (max-width: 1200px) {
            .main-container {
                grid-template-columns: 1fr;
            }
            
            .debate-theater {
                height: 500px;
            }
        }
        
        /* Markdown-style formatting */
        strong {
            color: #f1f5f9;
            font-weight: 600;
        }
        
        .message-content ul {
            margin: 8px 0;
            padding-left: 20px;
        }
        
        .message-content li {
            margin: 4px 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <div>
                    <h1>⚡ NEXUS</h1>
                    <div class="logo-subtitle">Adversarial Multi-Agent Legal Reasoning</div>
                </div>
            </div>
            <div class="live-badge" id="liveBadge">
                🔴 LIVE DEBATE
            </div>
        </div>
    </div>
    
    <div class="main-container">
        <div class="debate-section">
            <div class="input-card">
                <div class="input-label">Enter Your Business Decision</div>
                <textarea 
                    id="queryInput" 
                    class="query-input"
                    placeholder="Example: Should we launch our MVP in the EU without full GDPR compliance? 3-month market window, $5M ARR potential."
                ></textarea>
                <div class="example-chips">
                    <div class="example-chip" onclick="setExample('gdpr')">GDPR Compliance</div>
                    <div class="example-chip" onclick="setExample('hemp')">Hemp Transport</div>
                    <div class="example-chip" onclick="setExample('california')">CA Contractors</div>
                    <div class="example-chip" onclick="setExample('germany')">German Office</div>
                </div>
                <button id="debateBtn" class="debate-btn" onclick="startDebate()">
                    Start Adversarial Debate
                </button>
            </div>
            
            <div class="debate-theater">
                <div class="theater-header">
                    <span>Debate Theater</span>
                    <span id="debateStatus" style="color: #64748b;">Waiting...</span>
                </div>
                <div class="debate-messages" id="debateMessages">
                    <div class="welcome-message">
                        <p style="font-size: 18px; margin-bottom: 12px;">👋 Welcome to Nexus</p>
                        <p>Enter a business decision above to watch our AI agents debate from opposing perspectives.</p>
                        <p style="margin-top: 12px; font-size: 14px;">
                            🚨 Paranoid Lawyer will minimize risk<br>
                            💰 Greedy Finance will maximize growth<br>
                            ⚖️ The Mediator will synthesize
                        </p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="summary-panel">
            <div class="summary-title">Decision Summary</div>
            
            <div class="summary-item">
                <div class="summary-label">Risk Score</div>
                <div id="riskScore" class="risk-score risk-medium">-</div>
            </div>
            
            <div class="summary-item">
                <div class="summary-label">Cost of Delay</div>
                <div class="summary-value" id="costOfDelay">-</div>
            </div>
            
            <div class="summary-item">
                <div class="summary-label">Confidence</div>
                <div class="summary-value" id="confidenceValue">-%</div>
                <div class="confidence-bar">
                    <div class="confidence-fill" id="confidenceFill" style="width: 0%"></div>
                </div>
            </div>
            
            <div class="audit-hash">
                <div class="hash-label">Audit Trail (NEO L1)</div>
                <div class="hash-value" id="auditHash">Awaiting debate...</div>
            </div>
        </div>
    </div>
    
    <script>
        const examples = {
            gdpr: "Should we launch our MVP in the EU without full GDPR compliance? We have a 3-month market window and $5M ARR potential. Competitors are also launching soon.",
            hemp: "Should we transport 5,000 lbs of hemp biomass from Oregon to Florida through Idaho? The direct route saves 2 weeks and gets us a $50K bonus, but Idaho has strict laws.",
            california: "Should we hire 10 engineers in California as contractors instead of employees? It saves $200K/year but there's AB5 misclassification risk.",
            germany: "Should we open an office in Germany with 5 employees? There's a $20M market opportunity but complex labor laws and tax nexus issues."
        };
        
        function setExample(type) {
            document.getElementById('queryInput').value = examples[type];
        }
        
        function formatMessage(text) {
            // Convert markdown-style bold to HTML
            return text
                .replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>')
                .replace(/•/g, '&bull;');
        }
        
        function addMessage(agent, content, color) {
            const messagesDiv = document.getElementById('debateMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'debate-message';
            
            const time = new Date().toLocaleTimeString('en-US', { 
                hour: '2-digit', 
                minute: '2-digit' 
            });
            
            let icon, agentClass, displayName;
            if (agent.includes('Paranoid') || agent.includes('Lawyer')) {
                icon = '🚨';
                agentClass = 'lawyer';
                displayName = 'Paranoid Lawyer';
            } else if (agent.includes('Greedy') || agent.includes('Finance')) {
                icon = '💰';
                agentClass = 'finance';
                displayName = 'Greedy Finance';
            } else {
                icon = '⚖️';
                agentClass = 'mediator';
                displayName = 'The Mediator';
            }
            
            messageDiv.innerHTML = `
                <div class="message-header">
                    <div class="agent-icon ${agentClass}">${icon}</div>
                    <div class="agent-name" style="color: ${color}">${displayName}</div>
                    <div class="message-time">${time}</div>
                </div>
                <div class="message-content ${agentClass}">
                    ${formatMessage(content)}
                </div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function updateSummary(summary) {
            // Update risk score
            const riskElement = document.getElementById('riskScore');
            riskElement.textContent = summary.risk_score || 'MEDIUM';
            riskElement.className = 'risk-score';
            if (summary.risk_score && summary.risk_score.includes('HIGH')) {
                riskElement.classList.add('risk-high');
            } else if (summary.risk_score && summary.risk_score.includes('LOW')) {
                riskElement.classList.add('risk-low');
            } else {
                riskElement.classList.add('risk-medium');
            }
            
            // Update cost of delay
            document.getElementById('costOfDelay').textContent = summary.cost_of_delay || '-';
            
            // Update confidence
            const confidence = summary.confidence || 0;
            document.getElementById('confidenceValue').textContent = confidence + '%';
            document.getElementById('confidenceFill').style.width = confidence + '%';
        }
        
        async function startDebate() {
            const query = document.getElementById('queryInput').value.trim();
            if (!query) {
                alert('Please enter a business decision to debate');
                return;
            }
            
            // Reset UI
            document.getElementById('debateMessages').innerHTML = '';
            document.getElementById('debateBtn').disabled = true;
            document.getElementById('liveBadge').classList.add('active');
            document.getElementById('debateStatus').innerHTML = '<span class="loading-spinner"></span> Debating...';
            
            // Reset summary
            document.getElementById('riskScore').textContent = '-';
            document.getElementById('costOfDelay').textContent = '-';
            document.getElementById('confidenceValue').textContent = '-%';
            document.getElementById('confidenceFill').style.width = '0%';
            document.getElementById('auditHash').textContent = 'Calculating...';
            
            try {
                const response = await fetch('/api/debate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query })
                });
                
                const data = await response.json();
                
                // Display messages with delays for dramatic effect
                for (let i = 0; i < data.messages.length; i++) {
                    const msg = data.messages[i];
                    setTimeout(() => {
                        addMessage(msg.agent, msg.content, msg.color);
                        
                        // Update summary after mediator speaks
                        if (msg.agent.includes('Mediator') && data.summary) {
                            setTimeout(() => updateSummary(data.summary), 500);
                        }
                    }, i * 1500);
                }
                
                // Update audit hash
                setTimeout(() => {
                    document.getElementById('auditHash').textContent = data.audit_hash;
                }, data.messages.length * 1500 + 1000);
                
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                setTimeout(() => {
                    document.getElementById('debateBtn').disabled = false;
                    document.getElementById('liveBadge').classList.remove('active');
                    document.getElementById('debateStatus').textContent = 'Complete';
                }, (data.messages || []).length * 1500 + 2000);
            }
        }
        
        // Allow Enter key to submit (Ctrl+Enter for newline)
        document.getElementById('queryInput').addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                startDebate();
            }
        });
    </script>
</body>
</html>
"""


@app.post("/api/debate")
async def run_debate(request: QueryRequest):
    """Run adversarial debate between agents"""
    
    try:
        session_id = str(uuid.uuid4())
        messages = []
        
        # 1. Paranoid Lawyer speaks first
        lawyer_response = await paranoid_lawyer.analyze(request.query)
        messages.append(DebateMessage(
            agent="Paranoid Lawyer",
            color="#ef4444",
            content=lawyer_response,
            timestamp=datetime.now().isoformat()
        ))
        
        # 2. Greedy Finance responds
        finance_response = await greedy_finance.analyze(request.query)
        messages.append(DebateMessage(
            agent="Greedy Finance", 
            color="#22c55e",
            content=finance_response,
            timestamp=datetime.now().isoformat()
        ))
        
        # 3. Mediator synthesizes
        mediator_result = await mediator.synthesize(
            lawyer_response, 
            finance_response, 
            request.query
        )
        messages.append(DebateMessage(
            agent="The Mediator",
            color="#6366f1",
            content=mediator_result["verdict"],
            timestamp=datetime.now().isoformat()
        ))
        
        # Generate audit hash
        audit_data = {
            "session_id": session_id,
            "query": request.query,
            "lawyer": lawyer_response,
            "finance": finance_response,
            "verdict": mediator_result["verdict"],
            "timestamp": datetime.now().isoformat()
        }
        
        audit_string = json.dumps(audit_data, sort_keys=True)
        audit_hash = f"0x{hashlib.sha256(audit_string.encode()).hexdigest()[:16]}..."
        
        # Store session
        sessions[session_id] = {
            "messages": messages,
            "summary": mediator_result,
            "audit_hash": audit_hash
        }
        
        return DebateResponse(
            session_id=session_id,
            messages=messages,
            summary=mediator_result,
            audit_hash=audit_hash
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": ["Paranoid Lawyer", "Greedy Finance", "Mediator"],
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    print("\n⚡ NEXUS ADVERSARIAL SYSTEM")
    print("="*40)
    print("Starting debate server on http://localhost:8000")
    print("="*40)
    uvicorn.run(app, host="0.0.0.0", port=8000)
