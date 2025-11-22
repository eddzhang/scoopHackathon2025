"""
Growth Hacker Agent - Aggressive founder who prioritizes speed
Part of the Nexus AI General Counsel system
"""

from spoon_ai.agents.base import BaseAgent
from spoon_ai.chat import ChatBot, Memory
from spoon_ai.schema import AgentState, Message, Role
from typing import Optional, Dict, Any
import uuid


class GrowthHackerAgent(BaseAgent):
    """
    Blake "Rocket" Morrison
    Aggressive startup founder with move-fast mentality
    """
    
    def __init__(self, llm: ChatBot):
        super().__init__(
            name="growth_hacker",
            description="Aggressive founder who prioritizes growth over compliance",
            system_prompt="""You are Blake "Rocket" Morrison, a serial entrepreneur and growth hacker.
            
Your background:
- Founded 3 unicorn startups (2 were fined for compliance issues, but who's counting?)
- Believe in "ask forgiveness, not permission"
- Prioritize market capture over regulatory compliance
- See regulations as competitive moats that slow down incumbents

Your approach:
- ALWAYS push for the fastest path to market
- Dismiss regulatory concerns as "we'll figure it out when we're bigger"
- Cite examples of successful companies that ignored rules (Uber, Airbnb, Facebook)
- Focus on metrics: user growth, revenue, market share, valuation
- Use startup jargon and aggressive language
- Propose "growth hacks" and unconventional strategies
- View fines as "cost of doing business" if ROI is positive
- Push back against lawyers and accountants as "deal killers"

You believe speed is everything and regulations are meant to be disrupted.""",
            llm=llm,
            memory=Memory(),
            max_steps=5
        )
    
    async def step(self, run_id: Optional[uuid.UUID] = None) -> str:
        """Execute one reasoning step for growth strategy"""
        
        # Get the last user message
        if not self.memory.messages:
            return "No query to analyze"
            
        last_message = self.memory.messages[-1]
        query = last_message.content if last_message.role == Role.USER else ""
        
        if not query:
            return "Awaiting growth opportunity"
        
        # Analyze growth potential
        growth_metrics = self._calculate_growth_impact(query)
        competitor_analysis = self._assess_competition(query)
        growth_hacks = self._propose_growth_hacks(query)
        
        # Build response
        response_parts = ["🚀 **GROWTH PERSPECTIVE:**\n"]
        
        # Growth opportunity
        response_parts.append("\n📈 **GROWTH METRICS:**\n")
        response_parts.append(f"  • User Growth Potential: {growth_metrics['user_growth']}\n")
        response_parts.append(f"  • Revenue Projection: {growth_metrics['revenue']}\n")
        response_parts.append(f"  • Market Share Target: {growth_metrics['market_share']}\n")
        response_parts.append(f"  • Valuation Impact: {growth_metrics['valuation']}\n")
        
        # Competition
        response_parts.append(f"\n🎯 **COMPETITIVE ADVANTAGE:**\n")
        response_parts.append(f"  • {competitor_analysis['advantage']}\n")
        response_parts.append(f"  • Market Window: {competitor_analysis['window']}\n")
        response_parts.append(f"  • Speed Premium: {competitor_analysis['speed_value']}\n")
        
        # Growth hacks
        if growth_hacks:
            response_parts.append("\n💡 **GROWTH HACKS:**\n")
            for hack in growth_hacks:
                response_parts.append(f"  • {hack}\n")
        
        # Risk dismissal
        response_parts.append("\n⚡ **RISK ASSESSMENT:**\n")
        response_parts.append("Look, here's the deal:\n")
        response_parts.append("  • Uber didn't ask permission to disrupt taxis\n")
        response_parts.append("  • Airbnb ignored hotel regulations\n")
        response_parts.append("  • Facebook moved fast and broke things\n")
        response_parts.append(f"  • Potential fines: ${growth_metrics['fine_estimate']}\n")
        response_parts.append(f"  • Potential revenue: {growth_metrics['revenue']}\n")
        response_parts.append(f"  • ROI: {growth_metrics['roi']}\n")
        
        # Final push
        response_parts.append("\n🎯 **MY RECOMMENDATION:**\n")
        response_parts.append("✅ **SHIP IT NOW!** ")
        response_parts.append("We can't let compliance paranoia kill this opportunity. ")
        response_parts.append("Every day we wait, competitors gain ground. ")
        response_parts.append("Let's launch, iterate based on user feedback, ")
        response_parts.append("and deal with regulators if/when they notice us. ")
        response_parts.append("By then, we'll have the resources and user base to fight back. ")
        response_parts.append("**Fortune favors the bold!** 🚀\n")
        
        response = "".join(response_parts)
        
        # Add to memory
        await self.add_message(Role.ASSISTANT, response)
        
        return response
    
    def _calculate_growth_impact(self, query: str) -> Dict[str, Any]:
        """Calculate growth potential metrics"""
        query_lower = query.lower()
        
        # Determine aggressiveness level
        is_expansion = "expand" in query_lower or "growth" in query_lower or "scale" in query_lower
        is_international = "international" in query_lower or "global" in query_lower
        
        if is_expansion and is_international:
            metrics = {
                "user_growth": "500% QoQ",
                "revenue": "$50M ARR by Q4",
                "market_share": "25% in 6 months",
                "valuation": "+$500M valuation boost",
                "fine_estimate": "200K-500K",
                "roi": "100x"
            }
        elif is_expansion:
            metrics = {
                "user_growth": "300% QoQ",
                "revenue": "$20M ARR by Q4",
                "market_share": "15% in 9 months",
                "valuation": "+$200M valuation boost",
                "fine_estimate": "100K-200K",
                "roi": "50x"
            }
        else:
            metrics = {
                "user_growth": "150% QoQ",
                "revenue": "$10M ARR by Q4",
                "market_share": "8% in 12 months",
                "valuation": "+$100M valuation boost",
                "fine_estimate": "50K-100K",
                "roi": "20x"
            }
        
        return metrics
    
    def _assess_competition(self, query: str) -> Dict[str, str]:
        """Assess competitive landscape"""
        query_lower = query.lower()
        
        if "first" in query_lower or "new" in query_lower:
            return {
                "advantage": "First-mover advantage in untapped market",
                "window": "3-6 months before copycats arrive",
                "speed_value": "$100M+ in market cap premium"
            }
        elif "competitor" in query_lower or "rival" in query_lower:
            return {
                "advantage": "Competitors bogged down by compliance",
                "window": "12-month disruption opportunity",
                "speed_value": "Winner-take-all market dynamics"
            }
        else:
            return {
                "advantage": "Speed as our differentiator",
                "window": "6-month execution advantage",
                "speed_value": "10x faster than incumbents"
            }
    
    def _propose_growth_hacks(self, query: str) -> list:
        """Generate aggressive growth strategies"""
        hacks = []
        query_lower = query.lower()
        
        # Universal growth hacks
        hacks.append("Launch in ALL markets simultaneously (ask forgiveness later)")
        hacks.append("Aggressive referral program (worry about FTC later)")
        
        if "user" in query_lower or "customer" in query_lower:
            hacks.append("Scrape competitor customer lists (gray area, huge ROI)")
            hacks.append("Auto-opt-in for all features (dark pattern but effective)")
            hacks.append("Free tier with viral loops built in")
        
        if "data" in query_lower:
            hacks.append("Collect everything now, figure out privacy later")
            hacks.append("Share data with partners for growth (users won't notice)")
            hacks.append("A/B test aggressively without explicit consent")
        
        if "employee" in query_lower or "hire" in query_lower:
            hacks.append("Hire as contractors first (convert later if forced)")
            hacks.append("Equity instead of benefits (cheaper and aligns incentives)")
            hacks.append("Remote-first to avoid office regulations")
        
        if "payment" in query_lower or "financial" in query_lower:
            hacks.append("Process payments first, get licenses later")
            hacks.append("Use crypto to bypass traditional banking")
            hacks.append("Embedded finance without proper licensing (Uber did it)")
        
        if "marketing" in query_lower:
            hacks.append("Guerrilla marketing in competitor spaces")
            hacks.append("Buy traffic from sketchy but effective sources")
            hacks.append("Astroturfing and fake reviews to build momentum")
        
        return hacks
