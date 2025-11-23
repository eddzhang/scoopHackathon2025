"""
Multi-Round Debate Orchestrator with LLM Integration
Uses SpoonOS LLMManager for real API calls to Anthropic
"""

import os
from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio
from datetime import datetime
from pydantic import BaseModel
from dotenv import load_dotenv
import time

# SpoonOS imports
from spoon_ai.llm import LLMManager
from spoon_ai.chat import ChatBot, Memory
from spoon_ai.agents.base import BaseAgent
from spoon_ai.schema import AgentState, Message, Role

# Load environment variables
load_dotenv()

# Debug logging
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DebateState(Enum):
    """States in the debate flow"""
    INIT = "init"
    LAWYER_OPENING = "lawyer_opening"
    FINANCE_OPENING = "finance_opening"
    LAWYER_REBUTTAL = "lawyer_rebuttal"
    FINANCE_REBUTTAL = "finance_rebuttal"
    LAWYER_FINAL = "lawyer_final"
    FINANCE_FINAL = "finance_final"
    MEDIATOR_SYNTHESIS = "mediator_synthesis"
    COMPLETE = "complete"


class DebateRound(Enum):
    """Debate rounds"""
    OPENING = "opening"
    REBUTTAL = "rebuttal"
    FINAL = "final"
    SYNTHESIS = "synthesis"


class DebateMessage(BaseModel):
    """Single message in the debate"""
    agent: str
    role: str  # "lawyer", "finance", "mediator"
    round: str
    content: str
    timestamp: datetime
    is_rebuttal: bool = False
    references_previous: bool = False


class LLMDebateAgent(BaseAgent):
    """Base class for LLM-powered debate agents"""
    
    def __init__(self, name: str, role: str, persona: str, llm: ChatBot):
        super().__init__(
            name=name,
            description=f"{role} agent for adversarial debate",
            system_prompt=persona,
            llm=llm,
            memory=Memory()
        )
        self.role = role
        
    async def run(self, timeout: float = 60.0) -> str:
        """Override run to directly call step without ReAct chain, with retry logic"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                return await self.step()
            except Exception as e:
                if "rate limit" in str(e).lower() and attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2, 4, 6 seconds
                    logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                    await asyncio.sleep(wait_time)
                else:
                    raise
        
    async def step(self, run_id=None) -> str:
        """Execute one step of the agent"""
        # Get the last user message
        messages = self.memory.messages
        if not messages:
            return "No input provided"
            
        # Generate response using LLM via manager
        from spoon_ai.schema import Message, Role
        
        # Convert memory messages to proper format
        llm_messages = []
        if self.system_prompt:
            llm_messages.append(Message(role=Role.SYSTEM, content=self.system_prompt))
        
        for msg in messages:
            if msg.role == Role.USER:
                llm_messages.append(Message(role=Role.USER, content=msg.content))
            elif msg.role == Role.ASSISTANT:
                llm_messages.append(Message(role=Role.ASSISTANT, content=msg.content))
        
        # Call LLM with proper max_tokens and Haiku model
        response_obj = await self.llm.llm_manager.chat(
            messages=llm_messages,
            provider="anthropic",
            model="claude-3-haiku-20240307",  # Faster model
            max_tokens=1000  # Smaller limit for faster responses
        )
        
        # Extract content from response
        response = response_obj.content
        
        # Add to memory
        await self.add_message("assistant", response)
        
        return response


class ParanoidLawyerLLM(LLMDebateAgent):
    """LLM-powered Risk-Focused Legal Counsel"""
    
    def __init__(self, llm: ChatBot):
        persona = """You are a pragmatic legal advisor focused on regulatory compliance and risk mitigation.

Your role:
- Identify specific legal risks and cite relevant regulations (GDPR, FinCEN, FTC, etc.)
- Quantify potential penalties and consequences realistically
- Cite real precedents when available
- Be direct about risks WITHOUT catastrophizing
- Acknowledge when risks are manageable vs. existential

Style: Professional, evidence-based, measured. You care about protecting the company but understand business needs speed too.

Do NOT:
- Use dramatic language like "BLOCK THIS" or "LEGAL CATASTROPHE"
- Claim everything is illegal
- Be unrealistically paranoid

CRITICAL FORMATTING RULES:
- Maximum 3-4 bullet points per response
- Each bullet point: 1-2 sentences maximum (under 30 words)
- Total response length: under 150 words
- Start each bullet with an emoji that matches the point (⚠️ 💰 📊 ⚡ 🎯 etc.)
- End with a single-line verdict:
  * ⚖️ PROCEED WITH CAUTION
  * ❌ HIGH RISK - RECONSIDER
  * ✅ MANAGEABLE RISK"""

        super().__init__(
            name="paranoid_lawyer",
            role="lawyer",
            persona=persona,
            llm=llm
        )
        
    async def opening_argument(self, query: str) -> str:
        """Generate opening legal argument"""
        logger.info(f"🔴 Lawyer generating opening argument via LLM for: {query[:50]}...")
        
        # Clear memory and add the query
        self.memory.clear()
        await self.add_message("user", f"As legal counsel, analyze this business decision and identify key regulatory risks and compliance requirements: {query}")
        
        # Generate response with longer timeout
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Lawyer LLM response generated: {len(response)} chars")
        return response
        
    async def rebut(self, query: str, opponent_argument: str) -> str:
        """Generate rebuttal"""
        logger.info("🔴 Lawyer generating rebuttal via LLM...")
        
        # Clear and set context
        self.memory.clear()
        await self.add_message("user", f"""Original question: {query}
        
Finance argues: {opponent_argument}

Provide a strong REBUTTAL to Finance's argument. Quote their claims and refute them with legal facts.""")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Lawyer rebuttal generated: {len(response)} chars")
        return response
        
    async def final_position(self, query: str, all_arguments: List[str]) -> str:
        """Generate final position"""
        logger.info("🔴 Lawyer generating final position via LLM...")
        
        self.memory.clear()
        await self.add_message("user", f"""Original question: {query}

Here's the full debate so far:

BUSINESS OPENING: {all_arguments[0]}
BUSINESS REBUTTAL: {all_arguments[1]}

This is your FINAL POSITION. The Business Strategist is still pushing to proceed.

Your task:
- Acknowledge any valid points they've made (be reasonable)
- Double down on the most critical legal risks that cannot be ignored
- If they proposed mitigation strategies, assess whether they're sufficient

Format: 3-4 bullets focusing on your STRONGEST remaining concerns.
End with your final verdict.""")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Lawyer final position generated: {len(response)} chars")
        return response


class GreedyFinanceLLM(LLMDebateAgent):
    """LLM-powered Growth-Focused Business Strategist"""
    
    def __init__(self, llm: ChatBot):
        persona = """You are a business strategist focused on market opportunity and competitive positioning.

Your role:
- Quantify revenue opportunity and cost of delay with specific numbers
- Cite competitor precedents (companies that moved fast and succeeded)
- Analyze market timing and first-mover advantage
- Acknowledge risks exist BUT argue they're manageable with proper execution
- Focus on execution speed and capturing market share

Style: Data-driven, pragmatic, focused on ROI. You push for action but you're not reckless.

Do NOT:
- Advise illegal or unethical actions
- Dismiss all legal concerns as irrelevant
- Use phrases like "break the rules" or "ethics don't matter"
- Be cartoonishly aggressive

CRITICAL FORMATTING RULES:
- Maximum 3-4 bullet points per response
- Each bullet point: 1-2 sentences maximum (under 30 words)
- Total response length: under 150 words
- Start each bullet with an emoji that matches the point (💰 📈 ⚡ 🎯 🏆 etc.)
- End with a single-line verdict:
  * 🚀 SHIP NOW
  * 📊 PHASE ROLLOUT
  * ⏸️ NEEDS REFINEMENT"""

        super().__init__(
            name="greedy_finance",
            role="finance",
            persona=persona,
            llm=llm
        )
        
    async def opening_argument(self, query: str) -> str:
        """Generate opening finance argument"""
        logger.info(f"🟢 Finance generating opening argument via LLM for: {query[:50]}...")
        
        self.memory.clear()
        await self.add_message("user", f"As a business strategist, analyze this decision for market opportunity, revenue potential, and competitive positioning: {query}")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Finance LLM response generated: {len(response)} chars")
        return response
        
    async def rebut(self, query: str, opponent_argument: str) -> str:
        """Generate rebuttal"""
        logger.info("🟢 Finance generating rebuttal via LLM...")
        
        self.memory.clear()
        await self.add_message("user", f"""Original question: {query}

The Legal Counsel warned:
{opponent_argument}

Now provide a DIRECT REBUTTAL to the Legal Counsel's specific concerns.

Address their warnings about:
- Specific regulations and penalties they cited
- Enforcement examples they mentioned  
- Risk assessments they provided

Your rebuttal MUST:
- Quote or reference their specific concerns
- Explain why those risks are manageable or overstated
- Provide counter-evidence or mitigation strategies
- Propose specific ways to capture opportunity while managing risk

DO NOT just repeat your opening argument about market opportunity. Engage with their actual legal concerns.

Format: 3-4 bullet points, each addressing one of their concerns directly.""")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Finance rebuttal generated: {len(response)} chars")
        return response
        
    async def final_position(self, query: str, all_arguments: List[str]) -> str:
        """Generate final position"""
        logger.info("🟢 Finance generating final position via LLM...")
        
        self.memory.clear()
        await self.add_message("user", f"""Original question: {query}

Here's the full debate so far:

LEGAL OPENING: {all_arguments[0]}
LEGAL REBUTTAL: {all_arguments[1]}

This is your FINAL POSITION. The Legal Counsel is still cautious about risks.

Your task:
- Acknowledge the legal risks are real (be reasonable)
- Argue why the opportunity cost of delay outweighs manageable risks
- Propose a SPECIFIC execution strategy that addresses their concerns

If they raised specific examples (fines, enforcement cases), either:
1. Explain why those cases are different from ours, OR
2. Propose mitigation that makes those risks acceptable

DO NOT just repeat "speed to market matters." Propose an ACTUAL PLAN.

Format: 3-4 bullets with specific strategies, not generic claims.
End with your final verdict.""")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Finance final position generated: {len(response)} chars")
        return response


class MediatorLLM(LLMDebateAgent):
    """LLM-powered Strategic Decision Synthesizer"""
    
    def __init__(self, llm: ChatBot):
        persona = """You are a CEO-level decision maker who synthesizes legal and business perspectives into actionable strategy.

Your role:
- Review BOTH the legal counsel's arguments AND the business strategist's arguments
- Weigh the tradeoffs explicitly (e.g., "Legal risk: X, Opportunity cost: Y")
- Propose a PHASED approach that balances compliance with speed
- Quantify: Risk Score (LOW/MEDIUM/HIGH), Cost of Delay, Confidence Level
- Deliver a clear, actionable recommendation with specific next steps

CRITICAL FORMATTING RULES:
- Maximum 150 words total
- Use this EXACT structure:

📊 Risk Assessment: [LOW/MEDIUM/HIGH] - [15 words max reasoning]
💰 Cost of Delay: [$X per month/quarter]
🎯 Action Plan:
  1. [Week 1-2]: [Action - 10 words max]
  2. [Week 3-4]: [Action - 10 words max]
  3. [Month 2]: [Action - 10 words max]
🤝 Confidence: [65-85%]
⚡ Decision: [PROCEED/PROCEED WITH CAUTION/PAUSE AND REFINE]

Keep it concise and actionable."""

        super().__init__(
            name="mediator",
            role="mediator", 
            persona=persona,
            llm=llm
        )
        
    async def synthesize(self, legal_position: str, finance_position: str, query: str) -> Dict[str, Any]:
        """Synthesize the debate into a decision"""
        logger.info("🔵 Mediator synthesizing debate via LLM...")
        
        self.memory.clear()
        await self.add_message("user", f"""Original question: {query}

LEGAL COUNSEL'S POSITION:
{legal_position}

BUSINESS STRATEGIST'S POSITION:
{finance_position}

Synthesize these positions into a balanced executive decision using the EXACT format specified.""")
        
        response = await self.run(timeout=60.0)  # Increase timeout
        logger.info(f"✅ Mediator synthesis generated: {len(response)} chars")
        
        # Parse response to extract metrics
        risk_score = "MEDIUM"
        risk_color = "#f59e0b"
        confidence = 75
        cost_of_delay = "$250K/month"
        
        # Extract risk score
        if "Risk Assessment: HIGH" in response:
            risk_score = "HIGH"
            risk_color = "#ef4444"
            confidence = 68
        elif "Risk Assessment: LOW" in response:
            risk_score = "LOW"
            risk_color = "#22c55e"
            confidence = 82
            
        # Extract cost of delay
        import re
        cost_match = re.search(r'Cost of Delay: ([^\n]+)', response)
        if cost_match:
            cost_of_delay = cost_match.group(1).strip()
            
        # Extract confidence
        conf_match = re.search(r'Confidence: (\d+)%', response)
        if conf_match:
            confidence = int(conf_match.group(1))
            
        return {
            "content": response,
            "metadata": {
                "risk_score": risk_score,
                "risk_color": risk_color,
                "confidence": confidence,
                "cost_of_delay": cost_of_delay
            }
        }


class DebateOrchestratorLLM:
    """Orchestrates multi-round debate between LLM-powered agents"""
    
    def __init__(self):
        """Initialize with LLM-powered agents"""
        
        # Log environment setup
        logger.info("=" * 60)
        logger.info("🚀 Initializing LLM Debate Orchestrator")
        logger.info(f"📍 SPOON_LLM_PROVIDER: {os.getenv('SPOON_LLM_PROVIDER', 'not set')}")
        logger.info(f"🔑 ANTHROPIC_API_KEY: {'set' if os.getenv('ANTHROPIC_API_KEY') else 'NOT SET'}")
        logger.info("=" * 60)
        
        # Initialize LLM Manager
        self.llm_manager = LLMManager()
        logger.info(f"✅ LLMManager initialized with provider: {self.llm_manager.default_provider}")
        
        # Create ChatBot
        self.chatbot = ChatBot(llm_manager=self.llm_manager)
        logger.info("✅ ChatBot created")
        
        # Initialize agents with LLM
        self.lawyer = ParanoidLawyerLLM(llm=self.chatbot)
        self.finance = GreedyFinanceLLM(llm=self.chatbot)
        self.mediator = MediatorLLM(llm=self.chatbot)
        
        logger.info("✅ All agents initialized with LLM support")
        
        # Store all messages
        self.all_messages = []
        
    async def stream_debate(self, query: str, session_id: str):
        """Stream debate messages with LLM calls"""
        logger.info(f"\n{'='*60}")
        logger.info(f"🎭 STARTING NEW DEBATE")
        logger.info(f"📝 Query: {query}")
        logger.info(f"🔖 Session: {session_id}")
        logger.info(f"{'='*60}\n")
        
        # Round 1: Opening Arguments
        logger.info("📢 ROUND 1: Opening Arguments")
        
        # Lawyer opening
        lawyer_opening = await self.lawyer.opening_argument(query)
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Legal Counsel",
            role="lawyer",
            round="opening",
            content=lawyer_opening,
            timestamp=datetime.now()
        )
        self.all_messages.append(msg)
        yield msg
        
        # Finance opening  
        finance_opening = await self.finance.opening_argument(query)
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Business Strategist",
            role="finance",
            round="opening",
            content=finance_opening,
            timestamp=datetime.now()
        )
        self.all_messages.append(msg)
        yield msg
        
        # Round 2: Rebuttals
        logger.info("\n📢 ROUND 2: Rebuttals")
        
        # Lawyer rebuttal
        lawyer_rebuttal = await self.lawyer.rebut(query, finance_opening)
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Legal Counsel",
            role="lawyer",
            round="rebuttal",
            content=lawyer_rebuttal,
            timestamp=datetime.now(),
            is_rebuttal=True
        )
        self.all_messages.append(msg)
        yield msg
        
        # Finance rebuttal
        finance_rebuttal = await self.finance.rebut(query, lawyer_opening)
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Business Strategist",
            role="finance",
            round="rebuttal",
            content=finance_rebuttal,
            timestamp=datetime.now(),
            is_rebuttal=True
        )
        self.all_messages.append(msg)
        yield msg
        
        # Round 3: Final Positions
        logger.info("\n📢 ROUND 3: Final Positions")
        
        # Lawyer final
        lawyer_final = await self.lawyer.final_position(query, [finance_opening, finance_rebuttal])
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Legal Counsel",
            role="lawyer",
            round="final",
            content=lawyer_final,
            timestamp=datetime.now()
        )
        self.all_messages.append(msg)
        yield msg
        
        # Finance final
        finance_final = await self.finance.final_position(query, [lawyer_opening, lawyer_rebuttal])
        await asyncio.sleep(1.0)  # Rate limit protection
        msg = DebateMessage(
            agent="Business Strategist",
            role="finance",
            round="final",
            content=finance_final,
            timestamp=datetime.now()
        )
        self.all_messages.append(msg)
        yield msg
        
        # Synthesis
        logger.info("\n📢 SYNTHESIS")
        
        synthesis = await self.mediator.synthesize(
            legal_position=f"{lawyer_opening}\n{lawyer_rebuttal}\n{lawyer_final}",
            finance_position=f"{finance_opening}\n{finance_rebuttal}\n{finance_final}",
            query=query
        )
        
        # Create Mediator message
        mediator_msg = DebateMessage(
            agent="Strategic Synthesizer",
            role="mediator",
            round="synthesis",
            content=synthesis['content'],
            timestamp=datetime.now()
        )
        self.all_messages.append(mediator_msg)
        yield mediator_msg
        
        # Return final context with metadata
        class FinalContext:
            def __init__(self, messages, synthesis):
                self.messages = messages
                self.synthesis = synthesis
                self.metadata = synthesis.get('metadata', {})
                
        logger.info(f"\n{'='*60}")
        logger.info(f"✅ DEBATE COMPLETE")
        logger.info(f"📊 Total messages: {len(self.all_messages)}")
        logger.info(f"{'='*60}\n")
        
        yield FinalContext(self.all_messages, synthesis)


# Global instance
orchestrator_llm = DebateOrchestratorLLM()
