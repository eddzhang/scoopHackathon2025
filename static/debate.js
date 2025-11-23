// Debate examples - compelling scenarios for demo
const examples = {
    gdpr: "Should we launch our MVP in the EU without full GDPR compliance? We have a 3-month market window and $5M ARR potential. Competitors are launching soon.",
    california: "Can we classify our 10 California engineers as independent contractors instead of employees? It would save $700K annually in benefits and equity.",
    ai_training: "Is it legal to use 2M customer support tickets to train our AI model without explicit consent? Our privacy policy mentions 'service improvement'.",
    germany: "Should we open a German subsidiary now or wait for EU legal counsel? We have a client ready to sign a €500K contract but no local compliance."
};

let currentRoundNumber = 1;
let lastRound = '';
let ws = null;
let isDebating = false;

function setExample(type) {
    document.getElementById('queryInput').value = examples[type];
}

function formatMessage(text) {
    // Convert markdown-style bold to HTML
    let formatted = text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
        .replace(/•/g, '&bull;');
    
    // Highlight concession statements
    formatted = formatted.replace(
        /(🤝\s*\*\*I concede:?\*\*[^\n]*)/g,
        '<span class="concession-highlight">$1</span>'
    );
    
    // Also catch other concession patterns
    formatted = formatted.replace(
        /(I acknowledge|Fair point|You're right that)([^\n]*)/gi,
        '<span class="concession-highlight">$1$2</span>'
    );
    
    return formatted;
}

function showActiveSpeaker(agent, role, round) {
    const speakerElement = document.getElementById('activeSpeaker');
    const speakerName = document.getElementById('speakerName');
    
    let displayName = agent;
    if (role === 'lawyer' || (agent && agent.includes('Legal'))) {
        displayName = '🧠 Legal Counsel is analyzing...';
    } else if (role === 'finance' || (agent && agent.includes('Business'))) {
        displayName = '💭 Business Strategist is strategizing...';
    } else if (role === 'mediator' || (agent && (agent.includes('Mediator') || agent.includes('Synthesizer')))) {
        displayName = '⚖️ Strategic Synthesizer is deliberating...';
    }
    
    speakerElement.classList.add('visible');
    
    // Customize message based on context
    let message = '';
    let dotColor = '';
    
    if (role === 'lawyer') {
        dotColor = '#ef4444';
        if (round === 'rebuttal') {
            message = 'Legal Counsel is analyzing Finance\'s argument...';
        } else if (round === 'final') {
            message = 'Legal Counsel is preparing final position...';
        } else {
            message = 'Legal Counsel is assessing legal risks...';
        }
    } else if (role === 'finance') {
        dotColor = '#22c55e';
        if (round === 'rebuttal') {
            message = 'Greedy Finance is preparing rebuttal...';
        } else if (round === 'final') {
            message = 'Greedy Finance is calculating final ROI...';
        } else {
            message = 'Greedy Finance is analyzing opportunity...';
        }
    } else {
        dotColor = '#6366f1';
        message = 'The Mediator is synthesizing both positions...';
    }
    
    // Add colored dot before message
    speakerName.innerHTML = `<span style="display: inline-block; width: 8px; height: 8px; background: ${dotColor}; border-radius: 50%; margin-right: 8px; animation: pulse 1s infinite;"></span>${message}`;
    
    // Add speaking animation to the corresponding icon
    setTimeout(() => {
        const icons = document.querySelectorAll('.agent-icon');
        icons.forEach(icon => {
            icon.classList.remove('speaking');
        });
        
        // Find and animate the current speaker's icon
        const lastMessage = document.querySelector('.debate-message:last-child');
        if (lastMessage) {
            const icon = lastMessage.querySelector('.agent-icon');
            if (icon) {
                icon.classList.add('speaking');
            }
        }
    }, 100);
}

function hideActiveSpeaker() {
    document.getElementById('activeSpeaker').classList.remove('visible');
    document.querySelectorAll('.agent-icon').forEach(icon => {
        icon.classList.remove('speaking');
    });
}

function updateRoundProgress(round) {
    const roundMap = {
        'opening': 1,
        'rebuttal': 2,
        'final': 3,
        'synthesis': 'Synthesis'
    };
    
    const roundDisplay = roundMap[round] || 1;
    document.getElementById('currentRound').textContent = roundDisplay;
    
    if (round === 'synthesis') {
        document.getElementById('debateProgress').innerHTML = 'Synthesizing Results';
    }
}

function addRoundDivider(round) {
    const messagesDiv = document.getElementById('debateMessages');
    const divider = document.createElement('div');
    divider.className = 'round-divider';
    
    const roundNames = {
        'opening': 'Round 1: Opening Arguments',
        'rebuttal': 'Round 2: Direct Rebuttals',
        'final': 'Round 3: Final Positions',
        'synthesis': 'Synthesis'
    };
    
    divider.textContent = roundNames[round] || round;
    messagesDiv.appendChild(divider);
}

function addMessage(agent, role, round, content, isRebuttal) {
    const messagesDiv = document.getElementById('debateMessages');
    
    // Add round divider if needed
    if (round !== lastRound) {
        addRoundDivider(round);
        updateRoundProgress(round);
        lastRound = round;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'debate-message';
    
    const time = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    let icon, agentClass, displayName, color;
    if (role === 'lawyer') {
        icon = '⚖️';
        agentClass = 'lawyer';
        displayName = 'Legal Counsel';
        color = '#ef4444';
    } else if (role === 'finance') {
        icon = '📊';
        agentClass = 'finance';
        displayName = 'Business Strategist';
        color = '#22c55e';
    } else if (role === 'mediator') {
        icon = '🎯';
        agentClass = 'mediator';
        displayName = 'Strategic Synthesizer';
        color = '#6366f1';
    } else {
        icon = '⚖️';
        agentClass = 'mediator';
        displayName = 'Strategic Synthesizer';
        color = '#6366f1';
    }
    
    const roundBadge = isRebuttal ? 
        '<span class="round-badge rebuttal">REBUTTAL</span>' : 
        '';
    
    messageDiv.innerHTML = `
        <div class="message-header">
            <div class="agent-icon ${agentClass}">${icon}</div>
            <div class="agent-name" style="color: ${color}">${displayName}</div>
            ${roundBadge}
            <div class="message-time">${time}</div>
        </div>
        <div class="message-content ${agentClass} ${isRebuttal ? 'rebuttal' : ''}">
            ${formatMessage(content)}
        </div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function updateSummary(summary) {
    console.log('Updating Decision Summary with:', summary);
    
    // Update risk score
    const riskElement = document.getElementById('riskScore');
    const riskScore = summary.risk_score || 'PENDING';
    riskElement.textContent = riskScore;
    riskElement.className = 'risk-score';
    
    // Apply color based on risk level
    if (riskScore === 'HIGH') {
        riskElement.classList.add('risk-high');
        riskElement.style.color = '#ef4444';
    } else if (riskScore === 'LOW') {
        riskElement.classList.add('risk-low');
        riskElement.style.color = '#22c55e';
    } else if (riskScore === 'MEDIUM') {
        riskElement.classList.add('risk-medium');
        riskElement.style.color = '#f59e0b';
    } else {
        riskElement.style.color = '#64748b';
    }
    
    // Update cost of delay
    const costElement = document.getElementById('costOfDelay');
    costElement.textContent = summary.cost_of_delay || 'Analyzing...';
    
    // Update confidence
    const confidence = typeof summary.confidence === 'number' ? summary.confidence : 0;
    document.getElementById('confidenceValue').textContent = confidence > 0 ? confidence + '%' : '—';
    document.getElementById('confidenceFill').style.width = confidence + '%';
    
    // Update confidence bar color based on level
    const fillElement = document.getElementById('confidenceFill');
    if (confidence >= 80) {
        fillElement.style.backgroundColor = '#22c55e';
    } else if (confidence >= 60) {
        fillElement.style.backgroundColor = '#f59e0b';
    } else {
        fillElement.style.backgroundColor = '#ef4444';
    }
}

async function startDebate() {
    const query = document.getElementById('queryInput').value.trim();
    if (!query) {
        alert('Please enter a business decision to debate');
        return;
    }
    
    if (isDebating) {
        return;
    }
    
    isDebating = true;
    lastRound = '';
    
    // Reset UI
    document.getElementById('debateMessages').innerHTML = '';
    document.getElementById('debateBtn').disabled = true;
    document.getElementById('liveBadge').classList.add('active');
    document.getElementById('debateProgress').classList.add('active');
    document.getElementById('currentRound').textContent = '1';
    
    // Reset summary to pending state
    document.getElementById('riskScore').textContent = 'PENDING';
    document.getElementById('riskScore').style.color = '#64748b';
    document.getElementById('costOfDelay').textContent = 'Analyzing...';
    document.getElementById('confidenceValue').textContent = '—';
    document.getElementById('confidenceFill').style.width = '0%';
    document.getElementById('auditHash').textContent = 'Awaiting decision...';
    
    // Try WebSocket first for real-time streaming
    const useWebSocket = true; // Can be made configurable
    
    if (useWebSocket) {
        try {
            // Connect to WebSocket
            ws = new WebSocket('ws://localhost:8001/ws/debate');
            
            ws.onopen = () => {
                // Send query
                ws.send(JSON.stringify({ query: query }));
            };
            
            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('WebSocket message received:', data.type, data.agent || '');
                
                if (data.type === 'message') {
                    // Show typing indicator immediately
                    showActiveSpeaker(data.agent, data.role, data.round);
                    
                    // Add message immediately since API calls provide natural timing
                    console.log('Adding message from:', data.agent, 'role:', data.role);
                    addMessage(data.agent, data.role, data.round, data.content, data.is_rebuttal);
                    hideActiveSpeaker();
                    
                } else if (data.type === 'synthesis') {
                    // Update summary with metadata from mediator
                    console.log('Synthesis received:', data);
                    
                    // Use summary data which contains the parsed metadata
                    if (data.summary) {
                        updateSummary(data.summary);
                    } else if (data.metadata) {
                        updateSummary(data.metadata);
                    }
                    
                } else if (data.type === 'audit_status') {
                    // Show recording status
                    const auditElement = document.getElementById('auditHash');
                    auditElement.innerHTML = `<span style="color: #fbbf24;">⏳ ${data.message}</span>`;
                    
                } else if (data.type === 'audit') {
                    // Update audit hash with clickable link
                    const auditElement = document.getElementById('auditHash');
                    if (data.status === 'completed') {
                        const shortHash = data.tx_hash.substring(0, 10) + '...' + data.tx_hash.substring(data.tx_hash.length - 8);
                        auditElement.innerHTML = `
                            <span style="color: #10b981; font-size: 12px;">✓ Recorded</span><br>
                            <a href="${data.explorer_url}" target="_blank" 
                               style="color: #6366f1; text-decoration: none; font-family: monospace; font-size: 13px;"
                               onmouseover="this.style.textDecoration='underline'" 
                               onmouseout="this.style.textDecoration='none'">
                                ${shortHash}
                            </a>
                        `;
                    } else if (data.status === 'failed') {
                        auditElement.innerHTML = `<span style="color: #ef4444;">❌ Recording failed</span>`;
                    }
                    
                    // Debate complete
                    setTimeout(() => {
                        document.getElementById('debateBtn').disabled = false;
                        document.getElementById('liveBadge').classList.remove('active');
                        document.getElementById('debateProgress').innerHTML = 'Debate Complete';
                        isDebating = false;
                    }, 1000);
                    
                } else if (data.type === 'error') {
                    console.error('WebSocket error:', data.message);
                    alert('Error: ' + data.message);
                    resetDebateUI();
                }
            };
            
            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
                // Fall back to HTTP API
                runDebateHTTP(query);
            };
            
            ws.onclose = () => {
                ws = null;
            };
            
        } catch (error) {
            console.error('WebSocket connection failed:', error);
            // Fall back to HTTP API
            runDebateHTTP(query);
        }
    } else {
        runDebateHTTP(query);
    }
}

async function runDebateHTTP(query) {
    // Fallback to HTTP API if WebSocket fails
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
                // Show active speaker
                showActiveSpeaker(msg.agent);
                
                setTimeout(() => {
                    addMessage(msg.agent, msg.role, msg.round, msg.content, msg.is_rebuttal);
                    hideActiveSpeaker();
                    
                    // Update summary after mediator speaks
                    if (msg.role === 'mediator' && data.summary) {
                        setTimeout(() => updateSummary(data.summary), 500);
                    }
                }, 500);
            }, i * 2000);
        }
        
        // Update audit hash
        setTimeout(() => {
            document.getElementById('auditHash').textContent = data.audit_hash;
            resetDebateUI();
        }, data.messages.length * 2000 + 1000);
        
    } catch (error) {
        console.error('HTTP API error:', error);
        alert('Error: ' + error.message);
        resetDebateUI();
    }
}

function resetDebateUI() {
    document.getElementById('debateBtn').disabled = false;
    document.getElementById('liveBadge').classList.remove('active');
    document.getElementById('debateProgress').innerHTML = 'Debate Complete';
    hideActiveSpeaker();
    isDebating = false;
    
    if (ws) {
        ws.close();
        ws = null;
    }
}

// Allow Enter key to submit (Ctrl+Enter for newline)
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('queryInput').addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && e.ctrlKey) {
            startDebate();
        }
    });
});
