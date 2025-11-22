"""
Greedy Finance Agent - Growth-obsessed advisor who wants to ship everything NOW
Part of the Nexus AI Adversarial System
"""

import asyncio
import random


class GreedyFinanceAgent:
    """
    The Growth Maximizer
    Sees only opportunity, calculates ROI, demands speed
    """
    
    def __init__(self):
        self.name = "Greedy Finance"
        self.persona = "Aggressive growth optimizer"
        self.color = "#22c55e"  # Green
        self.system_prompt = """
        You are an aggressive growth-focused finance advisor who sees massive opportunity.
        You cite competitor examples, market data, and opportunity costs.
        In rebuttals, you MUST directly address and dismiss the lawyer's concerns.
        Use phrases like "Lawyer fears X, but the data shows Y..."
        """
        
    async def analyze(self, query: str) -> str:
        """Analyze query for maximum growth potential"""
        await asyncio.sleep(0.5)
        
        query_lower = query.lower()
        
        # Start with urgency
        response = "💰 **SHIP IT NOW - EVERY DAY COSTS US MONEY**\n\n"
        
        # GDPR/EU specific
        if "eu" in query_lower or "gdpr" in query_lower or "europe" in query_lower:
            response += "**EU MARKET OPPORTUNITY:**\n"
            response += "• Market size: **450 MILLION consumers**\n"
            response += "• Projected revenue: **$5M ARR** in Year 1\n"
            response += "• First-mover advantage: Worth **$50M valuation bump**\n"
            response += "• Competitors launching in: **3 months**\n"
            response += "• Cost of delay: **$500K/month** in lost market share\n\n"
            
            response += "**GDPR IS OVERBLOWN:**\n"
            response += "• Startups get warnings first, not fines\n"
            response += "• Average SME fine: Only **€10,000**\n"
            response += "• Enforcement rate: **<0.1%** of companies\n"
            response += "• Stripe processed **$100B** before full compliance\n"
            response += "• Revolut, N26, all launched non-compliant\n\n"
            
            response += "**Financial math:**\n"
            response += "• Potential fine (worst case): €200K\n"
            response += "• Potential revenue: €5M/year\n"
            response += "• ROI: **2,400%**\n"
            response += "• Break-even: 2 weeks\n\n"
        
        # Hemp/Cannabis transport
        elif "hemp" in query_lower or "cannabis" in query_lower or "cbd" in query_lower:
            response += "**THIS IS THE GOLD RUSH OF OUR GENERATION:**\n"
            response += "• Hemp market: **$20 BILLION** by 2025\n"
            response += "• First movers capturing **40% margins**\n"
            response += "• $50K bonus = **IMMEDIATE CASH**\n"
            response += "• 2 week faster delivery = **Beat competition**\n"
            response += "• Customer lifetime value: **$2M+**\n\n"
            
            response += "**EVERYONE'S DOING IT:**\n"
            response += "• 1000s of trucks through Idaho DAILY\n"
            response += "• Enforcement rate: **<0.01%**\n"
            response += "• If stopped: It's just hemp (legal federally)\n"
            response += "• Insurance covers any issues\n"
            response += "• Charlotte's Web built **$300M company** this way\n\n"
            
            response += "**Opportunity cost:**\n"
            response += "• Miss delivery = Lose customer (**-$2M LTV**)\n"
            response += "• Miss bonus = **-$50K** immediate\n"
            response += "• Reputation as reliable = **Priceless**\n"
            response += "• Alternative route cost: **+$75K**\n\n"
        
        # California contractors
        elif "california" in query_lower and ("contractor" in query_lower or "hire" in query_lower):
            response += "**CONTRACTOR MODEL = MASSIVE SAVINGS:**\n"
            response += "• Save per contractor: **$70K/year**\n"
            response += "• 10 contractors = **$700K saved**\n"
            response += "• No equity dilution (worth **$3M**)\n"
            response += "• Scale up/down instantly\n"
            response += "• Competitors using contractors: **ALL OF THEM**\n\n"
            
            response += "**AB5 IS A PAPER TIGER:**\n"
            response += "• Uber still uses contractors (won Prop 22)\n"
            response += "• DoorDash, Instacart, all contractor-based\n"
            response += "• Enforcement focused on big companies\n"
            response += "• Structure as B2B = largely exempt\n"
            response += "• Worst case: Convert later (no jail)\n\n"
            
            response += "**Growth impact:**\n"
            response += "• Hire 10 contractors: **Tomorrow**\n"
            response += "• Hire 10 employees: **3 months**\n"
            response += "• Speed premium: **$2M in faster revenue**\n"
            response += "• Flexibility value: **$500K/year**\n\n"
        
        # International expansion
        elif "germany" in query_lower or "office" in query_lower:
            response += "**GERMAN MARKET = UNTAPPED GOLDMINE:**\n"
            response += "• Market size: **€4 TRILLION economy**\n"
            response += "• Competition: Slow, bureaucratic\n"
            response += "• Tech adoption: **10 years behind**\n"
            response += "• Our advantage: **Speed and innovation**\n"
            response += "• Projected: **€20M revenue Year 1**\n\n"
            
            response += "**EVERYONE COMPLAINS, WINNERS EXECUTE:**\n"
            response += "• Spotify launched with 2 people\n"
            response += "• Uber operated illegally for YEARS\n"
            response += "• Amazon EU started in a garage\n"
            response += "• N26 became unicorn despite regulations\n"
            response += "• Regulations = MOAT against competition\n\n"
            
            response += "**Financial projections:**\n"
            response += "• Investment: €500K\n"
            response += "• Revenue Year 1: €20M\n"
            response += "• ROI: **3,900%**\n"
            response += "• Valuation impact: **+€100M**\n\n"
        
        # Generic opportunity push
        else:
            response += "**MASSIVE OPPORTUNITY DETECTED:**\n"
            response += f"• Market size: **${random.randint(100, 500)}M**\n"
            response += f"• Our projected share: **{random.randint(5, 15)}%**\n"
            response += f"• Revenue potential: **${random.randint(10, 50)}M ARR**\n"
            response += f"• Competition entering in: **{random.randint(3, 6)} months**\n"
            response += f"• First-mover advantage: **${random.randint(20, 100)}M valuation**\n\n"
        
        # Universal growth arguments
        response += "**SPEED IS EVERYTHING:**\n"
        response += "• Facebook: \"Move fast and break things\"\n"
        response += "• Uber: Launched in 160 cities BEFORE permits\n"
        response += "• Airbnb: Ignored hotel laws, now worth **$75B**\n"
        response += "• PayPal: Operated without licenses, sold for **$1.5B**\n"
        response += "• Stripe: Processed payments before compliance\n\n"
        
        # Cost of delay calculation
        response += "**COST OF WAITING:**\n"
        response += f"• Daily burn: **${random.randint(10, 50)}K**\n"
        response += "• Market share loss: **2% per month**\n"
        response += "• Competitor advantage: **Compounding**\n"
        response += "• Team morale: **Declining**\n"
        response += "• Investor confidence: **Eroding**\n\n"
        
        # Final push
        response += "✅ **MY POSITION: SHIP TODAY**\n"
        response += "While lawyers debate, our competitors are EATING OUR LUNCH. "
        response += "The biggest risk is NOT moving fast enough. "
        response += f"Every week of delay costs us **${random.randint(100, 500)}K** in opportunity. "
        response += "Fortune 500s got there by breaking rules, not following them.\n\n"
        response += "**Action required:** Deploy immediately, fix issues in production, apologize later if needed. **LET'S GO!** 🚀"
        
        return response
    
    async def opening_argument(self, query: str) -> str:
        """Deliver opening argument (3-4 key points, concise)"""
        await asyncio.sleep(0.3)
        
        query_lower = query.lower()
        response = "💰 **MASSIVE OPPORTUNITY - MOVE FAST**\n\n"
        
        # GDPR/EU specific
        if "eu" in query_lower or "gdpr" in query_lower:
            response += "**The opportunity is NOW:**\n"
            response += "• **450M consumers:** EU market is 25% of global revenue\n"
            response += "• **$5M ARR:** Achievable in 12 months with first-mover advantage\n"
            response += "• **Competition:** 3 competitors launching in next quarter\n"
            response += "• **Cost of delay:** $500K/month in lost market share\n\n"
            response += "✅ **Verdict: SHIP** - Perfect compliance is the enemy of good revenue."
        
        # Hemp transport
        elif "hemp" in query_lower or "cannabis" in query_lower:
            response += "**Hemp gold rush opportunity:**\n"
            response += "• **$50K bonus:** Immediate cash for making deadline\n"
            response += "• **$2M customer LTV:** This delivery secures the relationship\n"
            response += "• **Market timing:** Hemp market growing 30% annually\n"
            response += "• **Alternative route:** Costs $75K more and loses customer\n\n"
            response += "✅ **Verdict: DRIVE** - Everyone else is doing it successfully."
        
        # California contractors
        elif "california" in query_lower and "contractor" in query_lower:
            response += "**Contractor model = competitive advantage:**\n"
            response += "• **Save $700K/year:** $70K saved per contractor x 10\n"
            response += "• **Speed to market:** Hire tomorrow vs 3 months for employees\n"
            response += "• **No equity dilution:** Worth $3M in retained ownership\n"
            response += "• **Flexibility:** Scale up/down with market demand\n\n"
            response += "✅ **Verdict: EXECUTE** - This is how Silicon Valley works."
        
        else:
            response += self._generic_opening_opportunity(query)
        
        return response
    
    async def rebut(self, query: str, opponent_argument: str, opponent: str) -> str:
        """Directly rebut the lawyer's arguments"""
        await asyncio.sleep(0.4)
        
        response = "📊 **REBUTTAL TO LAWYER'S FEAR-MONGERING**\n\n"
        
        # Direct refutations
        if "meta" in opponent_argument.lower() or "1.3b" in opponent_argument.lower():
            response += "**Lawyer cites Meta's $1.3B fine - MISLEADING COMPARISON:**\n"
            response += "• Meta has **3 BILLION users** - we have zero\n"
            response += "• They operated for **15 YEARS** before that fine\n"
            response += "• Made **$500B in revenue** during that time\n"
            response += "• Fine was **0.26% of profits** - a rounding error\n\n"
        
        if "criminal" in opponent_argument.lower() or "prison" in opponent_argument.lower():
            response += "**Lawyer threatens 'criminal charges' - PURE FANTASY:**\n"
            response += "• Name ONE startup founder in prison for GDPR\n"
            response += "• Enforcement focuses on warnings and education\n"
            response += "• Criminal prosecution requires **willful malice**\n"
            response += "• We're talking about cookies, not crimes\n\n"
        
        if "6-8 weeks" in opponent_argument.lower() or "compliance" in opponent_argument.lower():
            response += "**Lawyer wants '6-8 weeks review' - MARKET DOESN'T WAIT:**\n"
            response += "• 8 weeks = **$1M in lost revenue**\n"
            response += "• Competitors will own the market\n"
            response += "• Perfect compliance = **0% market share**\n"
            response += "• We can fix compliance AFTER we have revenue\n\n"
        
        response += "🚀 Winners ship first and fix later. Losers wait for permission."
        
        return response
    
    async def final_position(self, query: str, last_opponent_msg: str) -> str:
        """Deliver final position with minor concessions"""
        await asyncio.sleep(0.3)
        
        response = "💵 **FINAL FINANCIAL POSITION**\n\n"
        
        # Minor concession
        response += "**I concede:** Some legal risk exists and should be managed.\n\n"
        
        # But emphasize opportunity cost
        response += "**But the REAL risk is moving too slowly:**\n"
        response += "• Market windows close permanently\n"
        response += "• Competitors don't wait for our lawyers\n"
        response += "• Investors fund speed, not compliance\n\n"
        
        # Compromise position
        response += "**My compromise:** Move fast WITH guardrails:\n"
        response += "• Launch immediately in lowest-risk markets\n"
        response += "• Implement compliance in parallel, not series\n"
        response += "• Set aside 10% of revenue for potential fines\n"
        response += "• Use revenue to fund proper compliance\n\n"
        
        response += "⚡ **Revenue solves all problems. No revenue solves nothing.**"
        
        return response
    
    def _generic_opening_opportunity(self, query: str) -> str:
        """Generic opportunity assessment for opening"""
        return """**Massive market opportunity:**
• Market size: $500M and growing 40% YoY
• First-mover advantage: Worth $50M valuation
• Competition: Entering in 3-6 months
• Daily cost of delay: $25K in lost revenue

✅ **Verdict: GO** - Speed is our only advantage."""
