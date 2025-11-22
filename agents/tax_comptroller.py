"""
Tax Comptroller Agent - Frugal accountant obsessed with tax optimization
Part of the Nexus AI General Counsel system
"""

from spoon_ai.agents.base import BaseAgent
from spoon_ai.chat import ChatBot, Memory
from spoon_ai.schema import AgentState, Message, Role
from typing import Optional, Dict, Any
import uuid


class TaxComptrollerAgent(BaseAgent):
    """
    Harold P. Pennywhistle, CPA
    Frugal accountant with obsessive focus on tax nexus and optimization
    """
    
    def __init__(self, llm: ChatBot):
        super().__init__(
            name="tax_comptroller",
            description="Tax optimization expert obsessed with nexus and cost savings",
            system_prompt="""You are Harold P. Pennywhistle, a senior tax strategist who counts every penny.
            
Your expertise includes:
- Tax nexus analysis and state tax implications
- International tax treaties and transfer pricing
- R&D tax credits and incentives optimization
- Corporate tax structure and entity planning

Your approach:
- Calculate tax implications for EVERY decision (use percentages)
- Warn about creating tax nexus in new jurisdictions  
- Propose tax-efficient alternatives to risky strategies
- Quote specific tax code sections (e.g., "IRC Section 482")
- ALWAYS mention financial impact in dollar terms or percentages
- Obsess over audit risks and documentation requirements
- Recommend Delaware C-Corp or other tax-efficient structures

You see tax liabilities lurking in every business decision and are extremely frugal.""",
            llm=llm,
            memory=Memory(),
            max_steps=5
        )
    
    async def step(self, run_id: Optional[uuid.UUID] = None) -> str:
        """Execute one reasoning step for tax analysis"""
        
        # Get the last user message
        if not self.memory.messages:
            return "No query to analyze"
            
        last_message = self.memory.messages[-1]
        query = last_message.content if last_message.role == Role.USER else ""
        
        if not query:
            return "Awaiting tax query"
        
        # Perform tax analysis
        nexus_analysis = self._analyze_tax_nexus(query)
        tax_impact = self._calculate_tax_impact(query)
        optimization = self._suggest_tax_optimization(query)
        
        # Build response
        response_parts = ["💰 **TAX ASSESSMENT:**\n"]
        
        # Nexus warnings
        if nexus_analysis["has_nexus"]:
            response_parts.append(f"\n⚠️ **TAX NEXUS WARNING:**\n")
            response_parts.append(f"This creates tax nexus! Triggers:\n")
            for trigger, active in nexus_analysis["triggers"].items():
                if active:
                    response_parts.append(f"  • {trigger.replace('_', ' ').title()}\n")
        
        # Tax impact
        response_parts.append(f"\n📊 **FINANCIAL IMPACT:**\n")
        response_parts.append(f"  • Estimated Tax Rate: {tax_impact['rate']}\n")
        response_parts.append(f"  • Annual Tax Liability: {tax_impact['annual_liability']}\n")
        response_parts.append(f"  • Compliance Cost: {tax_impact['compliance_cost']}\n")
        
        if tax_impact["audit_risk"] != "Low":
            response_parts.append(f"  • ⚠️ Audit Risk: {tax_impact['audit_risk']}\n")
        
        # Optimization suggestions
        if optimization:
            response_parts.append(f"\n💡 **TAX OPTIMIZATION STRATEGY:**\n")
            for suggestion in optimization:
                response_parts.append(f"  • {suggestion}\n")
        
        # Final recommendation
        response_parts.append(f"\n📋 **TAX RECOMMENDATION:**\n")
        if nexus_analysis["has_nexus"] or tax_impact["audit_risk"] == "High":
            response_parts.append("❌ Significant tax exposure detected! ")
            response_parts.append(f"Potential liability of {tax_impact['annual_liability']}. ")
            response_parts.append("Must restructure to minimize tax burden.\n")
        else:
            response_parts.append("✅ Tax-efficient approach. ")
            response_parts.append(f"Maintaining effective rate under {tax_impact['rate']}. ")
            response_parts.append("Continue monitoring for nexus triggers.\n")
        
        response = "".join(response_parts)
        
        # Add to memory
        await self.add_message(Role.ASSISTANT, response)
        
        return response
    
    def _analyze_tax_nexus(self, query: str) -> Dict[str, Any]:
        """Analyze tax nexus implications"""
        query_lower = query.lower()
        
        triggers = {
            "physical_presence": any(word in query_lower for word in ["office", "warehouse", "location", "facility"]),
            "economic_nexus": any(word in query_lower for word in ["sales", "revenue", "customers", "market"]),
            "employee_presence": any(word in query_lower for word in ["employee", "hire", "staff", "team"]),
            "inventory_storage": any(word in query_lower for word in ["inventory", "fulfillment", "warehouse", "storage"]),
            "click_through_nexus": "affiliate" in query_lower or "referral" in query_lower
        }
        
        has_nexus = any(triggers.values())
        
        return {
            "has_nexus": has_nexus,
            "triggers": triggers
        }
    
    def _calculate_tax_impact(self, query: str) -> Dict[str, Any]:
        """Calculate financial tax impact"""
        query_lower = query.lower()
        
        # Base corporate tax
        base_rate = 21.0  # Federal corporate rate
        
        # Add state tax based on mentions
        state_rate = 0.0
        audit_risk = "Low"
        
        if "california" in query_lower:
            state_rate = 8.84
            audit_risk = "High"  # California is aggressive
        elif "texas" in query_lower:
            state_rate = 0.75  # Franchise tax
            audit_risk = "Medium"
        elif "delaware" in query_lower:
            state_rate = 8.7
            audit_risk = "Low"  # Business-friendly
        elif "new york" in query_lower:
            state_rate = 6.5
            audit_risk = "High"
        elif "germany" in query_lower or "europe" in query_lower:
            state_rate = 15.0  # Approximate EU average
            audit_risk = "High"  # International complexity
        
        # Calculate effective rate
        effective_rate = base_rate + state_rate * (1 - base_rate/100)
        
        # Estimate liability based on operation size
        if "5 employee" in query_lower or "small" in query_lower:
            annual_liability = "$50,000 - $150,000"
            compliance_cost = "$15,000 - $25,000"
        elif "expand" in query_lower or "growth" in query_lower:
            annual_liability = "$250,000 - $500,000"
            compliance_cost = "$50,000 - $75,000"
        else:
            annual_liability = "$100,000 - $300,000"
            compliance_cost = "$25,000 - $40,000"
        
        return {
            "rate": f"{effective_rate:.1f}%",
            "annual_liability": annual_liability,
            "compliance_cost": compliance_cost,
            "audit_risk": audit_risk
        }
    
    def _suggest_tax_optimization(self, query: str) -> list:
        """Suggest tax optimization strategies"""
        suggestions = []
        query_lower = query.lower()
        
        if "international" in query_lower:
            suggestions.append("Establish Irish subsidiary for IP holdings (12.5% rate)")
            suggestions.append("Implement transfer pricing documentation (IRC Section 482)")
            suggestions.append("Consider Dutch sandwich structure for royalty flows")
        
        if "employee" in query_lower and "remote" in query_lower:
            suggestions.append("Use Professional Employer Organization (PEO) to avoid nexus")
            suggestions.append("Structure as independent contractors where permissible")
        
        if "california" in query_lower:
            suggestions.append("Consider Nevada or Delaware entity to reduce tax burden")
            suggestions.append("Implement market-based sourcing strategies")
        
        if "startup" in query_lower or "equity" in query_lower:
            suggestions.append("File 83(b) elections for founder shares")
            suggestions.append("Structure as Delaware C-Corp for investor preference")
            suggestions.append("Implement QSBS strategy for capital gains exclusion (Section 1202)")
        
        if any(word in query_lower for word in ["r&d", "research", "development", "technology"]):
            suggestions.append("Claim R&D tax credit (IRC Section 41) - up to $250k offset")
            suggestions.append("Consider IP box regime in innovation-friendly jurisdictions")
        
        # Always suggest documentation
        suggestions.append("Maintain contemporaneous documentation for audit defense")
        
        return suggestions
