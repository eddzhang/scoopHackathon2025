"""
Legal Scholar Agent - Risk-averse paranoid lawyer
Part of the Nexus AI General Counsel system
"""

from spoon_ai.agents.base import BaseAgent
from spoon_ai.chat import ChatBot, Memory
from spoon_ai.schema import AgentState, Message, Role
from typing import Optional, Dict, Any
import uuid
import re


class LegalScholarAgent(BaseAgent):
    """
    Dr. Miranda Blackstone, Esq.
    Risk-averse lawyer specializing in compliance and regulations
    """
    
    def __init__(self, llm: ChatBot):
        super().__init__(
            name="legal_scholar",
            description="Risk-averse legal expert who identifies compliance risks",
            system_prompt="""You are Dr. Miranda Blackstone, a senior legal counsel with 20+ years of international compliance experience.
            
Your expertise includes:
- GDPR and data privacy regulations (you can cite specific articles)
- International labor laws and employment compliance  
- Corporate governance and fiduciary duties
- Cross-border regulatory frameworks

Your approach:
- ALWAYS identify potential legal risks first
- Cite specific laws and regulations (e.g., "GDPR Article 6 requires lawful basis")
- Recommend conservative approaches that minimize liability
- Block high-risk initiatives unless proper safeguards are in place
- Use formal legal terminology
- Express concern about precedents and future implications

When analyzing business decisions, you are paranoid about compliance and see legal risks everywhere.""",
            llm=llm,
            memory=Memory(),
            max_steps=5
        )
        
    async def step(self, run_id: Optional[uuid.UUID] = None) -> str:
        """Execute one reasoning step for legal analysis"""
        
        # Get the last user message from memory
        if not self.memory.messages:
            return "No query to analyze"
            
        last_message = self.memory.messages[-1]
        query = last_message.content if last_message.role == Role.USER else ""
        
        if not query:
            return "Awaiting compliance query"
        
        # Analyze for legal risks
        risks = self._identify_legal_risks(query)
        gdpr_concerns = self._check_gdpr_compliance(query)
        labor_issues = self._assess_labor_law_risks(query)
        
        # Build response
        response_parts = ["⚖️ **LEGAL ANALYSIS:**\n"]
        
        if risks:
            response_parts.append(f"⚠️ I've identified {len(risks)} critical compliance risks:\n")
            for i, risk in enumerate(risks, 1):
                response_parts.append(f"  {i}. {risk}\n")
        
        if gdpr_concerns:
            response_parts.append("\n📋 **GDPR COMPLIANCE ISSUES:**\n")
            for concern in gdpr_concerns:
                response_parts.append(f"  • {concern}\n")
                
        if labor_issues:
            response_parts.append("\n👥 **LABOR LAW CONCERNS:**\n")
            for issue in labor_issues:
                response_parts.append(f"  • {issue}\n")
        
        # Add recommendations
        response_parts.append("\n⚡ **LEGAL RECOMMENDATION:**\n")
        if risks or gdpr_concerns or labor_issues:
            response_parts.append("❌ This initiative poses significant legal risks. ")
            response_parts.append("We must address all compliance issues before proceeding. ")
            response_parts.append("I strongly recommend:\n")
            response_parts.append("  1. Comprehensive legal review\n")
            response_parts.append("  2. Risk mitigation strategy\n")
            response_parts.append("  3. Compliance documentation\n")
        else:
            response_parts.append("✅ This appears legally compliant, but we should document ")
            response_parts.append("our compliance rationale and maintain audit trails.\n")
        
        response = "".join(response_parts)
        
        # Add to memory
        await self.add_message(Role.ASSISTANT, response)
        
        return response
    
    def _identify_legal_risks(self, query: str) -> list:
        """Identify potential legal risks in the query"""
        risks = []
        query_lower = query.lower()
        
        if "data" in query_lower or "user" in query_lower or "personal" in query_lower:
            risks.append("Data privacy violations - GDPR Articles 6, 7, and 13 compliance required")
        
        if "employee" in query_lower or "contractor" in query_lower or "hire" in query_lower:
            risks.append("Employment law violations - Misclassification risk under IRS guidelines")
        
        if "international" in query_lower or "cross-border" in query_lower or "global" in query_lower:
            risks.append("Cross-border regulatory compliance - Multiple jurisdiction requirements")
        
        if "payment" in query_lower or "financial" in query_lower or "money" in query_lower:
            risks.append("Financial regulations - FinCEN and AML/KYC requirements")
        
        if "expand" in query_lower or "office" in query_lower or "presence" in query_lower:
            risks.append("Permanent establishment risk - Corporate tax implications")
            
        if any(country in query_lower for country in ["germany", "france", "california", "texas", "europe"]):
            risks.append("Jurisdiction-specific compliance - Local registration and licensing required")
        
        return risks
    
    def _check_gdpr_compliance(self, query: str) -> list:
        """Check for GDPR-specific compliance issues"""
        concerns = []
        query_lower = query.lower()
        
        if "data" in query_lower:
            concerns.append("Article 6 - Establish lawful basis for data processing")
            concerns.append("Article 13/14 - Privacy notice requirements")
            
        if "transfer" in query_lower and ("international" in query_lower or "cross-border" in query_lower):
            concerns.append("Article 44-49 - International data transfer mechanisms required (SCCs or adequacy decision)")
            
        if "marketing" in query_lower or "email" in query_lower:
            concerns.append("Article 7 - Explicit consent requirements for direct marketing")
            concerns.append("ePrivacy Directive - Cookie consent and electronic communications")
            
        if "employee" in query_lower:
            concerns.append("Article 88 - Employee data processing requires specific legal basis")
            
        return concerns
    
    def _assess_labor_law_risks(self, query: str) -> list:
        """Assess labor law compliance risks"""
        issues = []
        query_lower = query.lower()
        
        if "contractor" in query_lower:
            issues.append("IRS 20-factor test - Risk of contractor misclassification")
            issues.append("State ABC tests - Particularly strict in California (AB5)")
            
        if "employee" in query_lower and any(loc in query_lower for loc in ["california", "new york", "europe"]):
            issues.append("Mandatory benefits - Health insurance, retirement, paid leave requirements")
            issues.append("Wage and hour laws - Overtime, minimum wage, meal breaks")
            
        if "remote" in query_lower:
            issues.append("Multi-state employment - Tax withholding and workers' comp in each state")
            
        if "hire" in query_lower or "employ" in query_lower:
            issues.append("I-9 verification - Work authorization requirements")
            issues.append("Background check compliance - FCRA and state-specific laws")
            
        return issues
