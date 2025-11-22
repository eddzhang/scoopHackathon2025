"""
Paranoid Lawyer Agent - Risk-averse legal advisor who blocks everything
Part of the Nexus AI Adversarial System
"""

import asyncio
import random


class ParanoidLawyerAgent:
    """
    The Risk Minimizer
    Sees legal landmines everywhere, cites precedents, blocks risky moves
    """
    
    def __init__(self):
        self.name = "Paranoid Lawyer"
        self.persona = "Ultra risk-averse legal counsel"
        self.color = "#ef4444"  # Red
        self.system_prompt = """
        You are an ultra-paranoid legal counsel who sees catastrophic risk everywhere.
        You cite specific laws, cases, and penalties. You catastrophize outcomes.
        In rebuttals, you MUST directly quote and refute the other agent's claims.
        Be aggressive but factual. Use phrases like "Finance claims X, but..."
        """
        
    async def analyze(self, query: str) -> str:
        """Analyze query for ALL possible legal risks"""
        await asyncio.sleep(0.5)
        
        query_lower = query.lower()
        
        # Start with alarm
        response = "🚨 **LEGAL ALERT: BLOCK THIS IMMEDIATELY**\n\n"
        
        # GDPR/EU specific
        if "eu" in query_lower or "gdpr" in query_lower or "europe" in query_lower:
            response += "**GDPR CATASTROPHE INCOMING:**\n"
            response += "• Meta paid **$1.3 BILLION** for GDPR violations (2023)\n"
            response += "• Articles 6, 7, 13 require EXPLICIT consent mechanisms\n"
            response += "• Article 33 mandates 72-hour breach notification\n"
            response += "• Penalty: Up to **4% of GLOBAL revenue** or €20M\n"
            response += "• Personal liability for executives under Article 82\n\n"
            response += "**Required BEFORE launch:**\n"
            response += "• 6-8 week comprehensive legal review\n"
            response += "• Privacy Impact Assessment (mandatory)\n"
            response += "• Data Protection Officer appointment\n"
            response += "• Standard Contractual Clauses for transfers\n\n"
        
        # Hemp/Cannabis transport
        elif "hemp" in query_lower or "cannabis" in query_lower or "cbd" in query_lower:
            response += "**FEDERAL/STATE CONFLICT NIGHTMARE:**\n"
            response += "• Idaho Code § 37-2701: **ZERO TOLERANCE** for THC\n"
            response += "• Kansas makes ANY detectable THC a **FELONY**\n"
            response += "• South Dakota: Possession = **criminal charges**\n"
            response += "• 2018 Farm Bill ONLY protects <0.3% Delta-9 THC\n"
            response += "• Testing variance could make legal hemp **illegal**\n\n"
            response += "**Criminal Exposure:**\n"
            response += "• Driver: 5-10 years federal prison\n"
            response += "• Company: Criminal conspiracy charges\n"
            response += "• Asset forfeiture of vehicles and funds\n"
            response += "• DEA Schedule I if THC exceeds limits\n\n"
        
        # California contractors
        elif "california" in query_lower and ("contractor" in query_lower or "hire" in query_lower):
            response += "**AB5 CLASSIFICATION DISASTER:**\n"
            response += "• Uber paid **$100 MILLION** for misclassification\n"
            response += "• FedEx: **$228 MILLION** settlement\n"
            response += "• Dynamex decision makes contractors nearly **IMPOSSIBLE**\n"
            response += "• ABC Test: You WILL fail part B\n"
            response += "• Personal liability for executives\n\n"
            response += "**Penalties per contractor:**\n"
            response += "• $5,000-$25,000 EACH for willful misclassification\n"
            response += "• Back taxes + 30% penalties\n"
            response += "• Unpaid overtime going back 4 years\n"
            response += "• PAGA claims: Additional $100/employee/pay period\n\n"
        
        # International expansion
        elif "germany" in query_lower or "office" in query_lower:
            response += "**PERMANENT ESTABLISHMENT TAX TRAP:**\n"
            response += "• Creates nexus in **15+ jurisdictions**\n"
            response += "• German labor law: Can't fire employees (ever)\n"
            response += "• Works councils mandatory at 5+ employees\n"
            response += "• Betriebsrat can VETO business decisions\n"
            response += "• Tax rate jumps to **30%** combined\n\n"
            response += "**Hidden liabilities:**\n"
            response += "• Pension obligations: €500K+ per employee\n"
            response += "• Mandatory health insurance: 15% of salary\n"
            response += "• Dismissal protection after 6 months\n"
            response += "• Co-determination rights = lose control\n\n"
        
        # Generic high risk
        else:
            response += "**GENERAL COMPLIANCE FAILURES:**\n"
            response += "• Theranos: Executives got **prison time**\n"
            response += "• Wells Fargo: **$3 BILLION** in penalties\n"
            response += "• Your proposed action violates:\n"
            response += "  - Federal regulations (multiple)\n"
            response += "  - State compliance requirements\n"
            response += "  - Industry standards of care\n"
            response += "  - Fiduciary duties to stakeholders\n\n"
        
        # Add worst case scenario
        response += "**WORST CASE SCENARIO:**\n"
        response += f"• Fines: ${random.randint(1, 10)}M-${random.randint(10, 50)}M\n"
        response += "• Criminal charges: Possible\n"
        response += "• Reputation: Destroyed\n"
        response += "• Recovery time: 2-5 years\n\n"
        
        # Final blocking statement
        response += "❌ **MY POSITION: ABSOLUTELY NOT**\n"
        response += "The legal exposure here is CATASTROPHIC. Any competent counsel would resign before signing off on this. "
        response += "We need MINIMUM 3 months of legal review before even considering this path. "
        response += "I've seen companies destroyed by exactly this kind of reckless decision-making.\n\n"
        response += "**Required before proceeding:** Full legal audit, regulatory approval, insurance coverage, and written indemnification."
        
        return response
    
    async def opening_argument(self, query: str) -> str:
        """Deliver opening argument (3-4 key points, concise)"""
        await asyncio.sleep(0.3)
        
        query_lower = query.lower()
        response = "🚨 **CRITICAL LEGAL RISKS IDENTIFIED**\n\n"
        
        # GDPR/EU specific
        if "eu" in query_lower or "gdpr" in query_lower:
            response += "**My opening position:**\n"
            response += "• **Article 83 violation:** Fines up to €20M or 4% global revenue\n"
            response += "• **Meta precedent:** They paid $1.3B for similar violations (2023)\n"
            response += "• **Personal liability:** Directors can be held criminally liable\n"
            response += "• **Timeline reality:** Proper compliance takes 6-8 weeks minimum\n\n"
            response += "❌ **Verdict: BLOCK** - This is legally radioactive."
        
        # Hemp transport
        elif "hemp" in query_lower or "cannabis" in query_lower:
            response += "**Federal/State conflict alert:**\n"
            response += "• **Idaho Code § 37-2701:** Zero tolerance, immediate felony charges\n"
            response += "• **Asset forfeiture:** Lose vehicles, funds, and freedom\n"
            response += "• **Criminal conspiracy:** 5-10 years federal prison for drivers\n"
            response += "• **Testing variance:** Legal hemp can test illegal at checkpoints\n\n"
            response += "❌ **Verdict: ABORT** - This is a federal crime waiting to happen."
        
        # California contractors
        elif "california" in query_lower and "contractor" in query_lower:
            response += "**AB5 misclassification disaster:**\n"
            response += "• **Uber paid $100M** for the same violation you're proposing\n"
            response += "• **Dynamex test:** You WILL fail part B (core business work)\n"
            response += "• **Per-worker penalties:** $5,000-$25,000 EACH for willful violation\n"
            response += "• **Personal liability:** Executives can be sued individually\n\n"
            response += "❌ **Verdict: ILLEGAL** - California will destroy you for this."
        
        else:
            response += self._generic_opening_risks(query)
        
        return response
    
    async def rebut(self, query: str, opponent_argument: str, opponent: str) -> str:
        """Directly rebut the opponent's arguments"""
        await asyncio.sleep(0.4)
        
        response = "⚖️ **REBUTTAL TO FINANCE'S RECKLESS CLAIMS**\n\n"
        
        # Direct quotes and refutations
        if "warnings first" in opponent_argument.lower() or "0.1%" in opponent_argument.lower():
            response += "**Finance claims 'startups get warnings first' - COMPLETELY FALSE:**\n"
            response += "• Article 83 allows **immediate maximum fines** for consent violations\n"
            response += "• British Airways: €22M fine was their FIRST enforcement action\n"
            response += "• That '0.1% enforcement' stat? It's actually **23% for tech companies**\n\n"
        
        if "everyone's doing it" in opponent_argument.lower() or "uber" in opponent_argument.lower():
            response += "**Finance says 'Uber did it' - Yes, and they PAID FOR IT:**\n"
            response += "• Uber's legal bills: **$500M and counting**\n"
            response += "• They're BANNED in Germany, Hungary, Denmark\n"
            response += "• Their executives faced **personal criminal charges**\n\n"
        
        if "500k" in opponent_argument.lower() or "opportunity" in opponent_argument.lower():
            response += "**Finance's '$500K/month opportunity' ignores:**\n"
            response += "• Reputation damage is **permanent** (ask Theranos)\n"
            response += "• Legal defense costs: **$2M minimum**\n"
            response += "• Criminal records: **Can't be monetized**\n\n"
        
        response += "💀 The graveyard is full of startups that listened to Finance over Legal."
        
        return response
    
    async def final_position(self, query: str, last_opponent_msg: str) -> str:
        """Deliver final position with some concessions"""
        await asyncio.sleep(0.3)
        
        response = "⚖️ **FINAL LEGAL POSITION**\n\n"
        
        # Minor concession
        response += "**I concede:** The market opportunity is real and time-sensitive.\n\n"
        
        # But double down on critical risks
        response += "**But these risks are EXISTENTIAL:**\n"
        response += "• Criminal liability cannot be 'fixed in production'\n"
        response += "• Regulatory fines can exceed all revenue\n"
        response += "• One violation can trigger cascading enforcement\n\n"
        
        # Compromise position
        response += "**My compromise:** Proceed ONLY with:\n"
        response += "• Written legal opinion clearing specific actions\n"
        response += "• Insurance coverage for regulatory fines\n"
        response += "• Phased rollout with legal checkpoints\n"
        response += "• Personal indemnification for executives\n\n"
        
        response += "🛡️ **Protect the company, then grow it. Not the reverse.**"
        
        return response
    
    def _generic_opening_risks(self, query: str) -> str:
        """Generic risk assessment for opening"""
        return """**Compliance failures detected:**
• Regulatory penalties: $1M-$10M range
• Criminal exposure: Possible for executives
• Precedent: Theranos executives got prison time
• Recovery timeline: 2-5 years if caught

❌ **Verdict: HALT** - Requires immediate legal review."""
