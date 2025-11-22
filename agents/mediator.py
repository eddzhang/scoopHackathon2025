"""
Mediator Agent - Synthesizes adversarial arguments into actionable decisions
Part of the Nexus AI Adversarial System
"""

import asyncio
from typing import Dict, Any


class MediatorAgent:
    """
    The Balanced Judge
    Synthesizes opposing viewpoints into actionable recommendations
    """
    
    def __init__(self):
        self.name = "The Mediator"
        self.persona = "Balanced synthesizer"
        self.color = "#6366f1"  # Purple
    
    async def synthesize(self, legal_position: str, finance_position: str, query: str) -> Dict[str, Any]:
        """Synthesize the debate into an actionable decision"""
        await asyncio.sleep(0.8)  # Thinking time
        
        # Analyze positions
        legal_blocks = "BLOCK" in legal_position or "risk" in legal_position.lower()
        finance_pushes = "SHIP" in finance_position or "NOW" in finance_position
        
        # Calculate metrics
        if legal_blocks and finance_pushes:
            risk_score = "HIGH"
            risk_color = "#ef4444"
            confidence = 45
            approach = "PROCEED WITH CAUTION"
        elif legal_blocks:
            risk_score = "MEDIUM-HIGH"
            risk_color = "#f59e0b"
            confidence = 60
            approach = "PHASED APPROACH REQUIRED"
        elif finance_pushes:
            risk_score = "MEDIUM"
            risk_color = "#eab308"
            confidence = 75
            approach = "PROCEED WITH MONITORING"
        else:
            risk_score = "LOW"
            risk_color = "#22c55e"
            confidence = 85
            approach = "SAFE TO PROCEED"
        
        # Extract cost of delay (mock analysis)
        cost_of_delay = "$500K/month"
        if "50k" in query.lower() or "bonus" in query.lower():
            cost_of_delay = "$50K immediate + $200K/month"
        elif "5m" in query.lower() or "million" in query.lower():
            cost_of_delay = "$1M/month"
        
        # Build verdict
        verdict = f"""⚖️ **MEDIATOR VERDICT: {approach}**

After analyzing both positions, here's my synthesis:

**📊 Risk Assessment:**
- Risk Score: **{risk_score}**
- Legal Exposure: {self._assess_legal_exposure(legal_position)}
- Growth Impact: {self._assess_growth_impact(finance_position)}

**💰 Financial Analysis:**
- Cost of Delay: **{cost_of_delay}**
- Opportunity Window: {self._assess_window(query)}
- Break-even Point: {self._calculate_breakeven(risk_score, cost_of_delay)}

**🎯 Recommended Action Plan:**
{self._generate_action_plan(risk_score, legal_blocks, finance_pushes, query)}

**📈 Confidence Level:** {confidence}%
**⚡ Decision Speed:** Execute within 2 weeks

This balances legal compliance with business growth, reducing risk by 80% while capturing 70% of the opportunity."""
        
        return {
            "verdict": verdict,
            "risk_score": risk_score,
            "risk_color": risk_color,
            "cost_of_delay": cost_of_delay,
            "confidence": confidence,
            "approach": approach
        }
    
    def _assess_legal_exposure(self, legal_position: str) -> str:
        if "GDPR" in legal_position:
            return "Up to 4% global revenue"
        elif "criminal" in legal_position.lower():
            return "Criminal liability risk"
        elif "violation" in legal_position.lower():
            return "$100K-$1M in fines"
        else:
            return "Manageable with documentation"
    
    def _assess_growth_impact(self, finance_position: str) -> str:
        if "BILLIONS" in finance_position:
            return "Massive first-mover advantage"
        elif "500K" in finance_position:
            return "Significant market opportunity"
        else:
            return "Moderate growth potential"
    
    def _assess_window(self, query: str) -> str:
        if "3 month" in query.lower() or "3-month" in query.lower():
            return "3 months (closing fast)"
        elif "10 days" in query.lower():
            return "10 days (urgent)"
        else:
            return "6-12 months"
    
    def _calculate_breakeven(self, risk: str, cost: str) -> str:
        if risk == "HIGH":
            return "18 months (high risk premium)"
        elif risk == "MEDIUM":
            return "9 months"
        else:
            return "4 months"
    
    def _generate_action_plan(self, risk: str, legal_blocks: bool, finance_pushes: bool, query: str) -> str:
        if "gdpr" in query.lower() or "eu" in query.lower():
            return """1. **Immediate:** Launch US-only version (2 weeks)
2. **Week 3-4:** Implement cookie consent + data minimization
3. **Week 5-6:** Add data portability + deletion features  
4. **Week 7-8:** EU soft launch with 95% GDPR compliance
5. **Ongoing:** Complete remaining 5% while operating"""
        
        elif "hemp" in query.lower() or "transport" in query.lower():
            return """1. **Immediate:** Legal review of Idaho/Kansas laws (24 hours)
2. **Day 2:** Secure legal counsel in transit states
3. **Day 3:** Document federal compliance (2018 Farm Bill)
4. **Day 4-5:** Alternative route if legal risk too high
5. **Execute:** Choose route based on risk/reward analysis"""
        
        elif "contractor" in query.lower() or "california" in query.lower():
            return """1. **Immediate:** Structure as corp-to-corp contracts
2. **Week 1:** Implement clear contractor agreements
3. **Week 2:** Ensure no day-to-day management
4. **Month 2:** Review for AB5 compliance
5. **Month 3:** Convert high-risk roles to employment"""
        
        else:
            return """1. **Week 1:** Complete risk assessment
2. **Week 2:** Implement minimum viable compliance
3. **Month 2:** Launch with monitoring
4. **Month 3:** Iterate based on feedback
5. **Ongoing:** Scale compliance with growth"""
