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
