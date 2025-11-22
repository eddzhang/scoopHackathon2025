"""
Multi-Round Debate Orchestrator with State Machine
Implements adversarial debate with rebuttals using SpoonOS StateGraph
"""

from typing import Dict, Any, List, Optional
from enum import Enum
import asyncio
from datetime import datetime
from pydantic import BaseModel

# Import agent classes
from agents.paranoid_lawyer import ParanoidLawyerAgent
from agents.greedy_finance import GreedyFinanceAgent
from agents.mediator import MediatorAgent


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


class DebateContext(BaseModel):
    """Context passed between debate states"""
    query: str
    session_id: str
    current_state: DebateState
    current_round: DebateRound
    messages: List[DebateMessage] = []
    lawyer_opening: Optional[str] = None
    finance_opening: Optional[str] = None
    lawyer_rebuttal: Optional[str] = None
    finance_rebuttal: Optional[str] = None
    lawyer_final: Optional[str] = None
    finance_final: Optional[str] = None
    synthesis: Optional[Dict[str, Any]] = None


class DebateOrchestrator:
    """
    Orchestrates multi-round adversarial debates between agents
    """
    
    def __init__(self):
        self.lawyer = ParanoidLawyerAgent()
        self.finance = GreedyFinanceAgent()
        self.mediator = MediatorAgent()
        
        # State transition map
        self.transitions = {
            DebateState.INIT: DebateState.LAWYER_OPENING,
            DebateState.LAWYER_OPENING: DebateState.FINANCE_OPENING,
            DebateState.FINANCE_OPENING: DebateState.LAWYER_REBUTTAL,
            DebateState.LAWYER_REBUTTAL: DebateState.FINANCE_REBUTTAL,
            DebateState.FINANCE_REBUTTAL: DebateState.LAWYER_FINAL,
            DebateState.LAWYER_FINAL: DebateState.FINANCE_FINAL,
            DebateState.FINANCE_FINAL: DebateState.MEDIATOR_SYNTHESIS,
            DebateState.MEDIATOR_SYNTHESIS: DebateState.COMPLETE
        }
    
    async def run_debate(self, query: str, session_id: str) -> DebateContext:
        """
        Run a complete multi-round debate
        """
        context = DebateContext(
            query=query,
            session_id=session_id,
            current_state=DebateState.INIT,
            current_round=DebateRound.OPENING
        )
        
        # Execute state machine
        while context.current_state != DebateState.COMPLETE:
            context = await self._execute_state(context)
            
            # Transition to next state
            if context.current_state in self.transitions:
                context.current_state = self.transitions[context.current_state]
            else:
                break
        
        return context
    
    async def _execute_state(self, context: DebateContext) -> DebateContext:
        """
        Execute the current state and update context
        """
        state = context.current_state
        
        if state == DebateState.INIT:
            # Initialize debate
            context.current_round = DebateRound.OPENING
            
        elif state == DebateState.LAWYER_OPENING:
            # Lawyer's opening argument
            response = await self.lawyer.opening_argument(context.query)
            context.lawyer_opening = response
            context.messages.append(DebateMessage(
                agent="Paranoid Lawyer",
                role="lawyer",
                round=DebateRound.OPENING.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=False
            ))
            
        elif state == DebateState.FINANCE_OPENING:
            # Finance's opening argument
            response = await self.finance.opening_argument(context.query)
            context.finance_opening = response
            context.messages.append(DebateMessage(
                agent="Greedy Finance",
                role="finance",
                round=DebateRound.OPENING.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=False
            ))
            context.current_round = DebateRound.REBUTTAL
            
        elif state == DebateState.LAWYER_REBUTTAL:
            # Lawyer rebuts Finance's opening
            response = await self.lawyer.rebut(
                context.query,
                context.finance_opening,
                "finance"
            )
            context.lawyer_rebuttal = response
            context.messages.append(DebateMessage(
                agent="Paranoid Lawyer",
                role="lawyer",
                round=DebateRound.REBUTTAL.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=True,
                references_previous=True
            ))
            
        elif state == DebateState.FINANCE_REBUTTAL:
            # Finance rebuts Lawyer's arguments
            response = await self.finance.rebut(
                context.query,
                f"{context.lawyer_opening}\n\n{context.lawyer_rebuttal}",
                "lawyer"
            )
            context.finance_rebuttal = response
            context.messages.append(DebateMessage(
                agent="Greedy Finance",
                role="finance",
                round=DebateRound.REBUTTAL.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=True,
                references_previous=True
            ))
            context.current_round = DebateRound.FINAL
            
        elif state == DebateState.LAWYER_FINAL:
            # Lawyer's final position
            response = await self.lawyer.final_position(
                context.query,
                context.finance_rebuttal
            )
            context.lawyer_final = response
            context.messages.append(DebateMessage(
                agent="Paranoid Lawyer",
                role="lawyer",
                round=DebateRound.FINAL.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=False
            ))
            
        elif state == DebateState.FINANCE_FINAL:
            # Finance's final position
            response = await self.finance.final_position(
                context.query,
                context.lawyer_rebuttal
            )
            context.finance_final = response
            context.messages.append(DebateMessage(
                agent="Greedy Finance",
                role="finance",
                round=DebateRound.FINAL.value,
                content=response,
                timestamp=datetime.now(),
                is_rebuttal=False
            ))
            context.current_round = DebateRound.SYNTHESIS
            
        elif state == DebateState.MEDIATOR_SYNTHESIS:
            # Mediator synthesizes the debate
            full_lawyer_position = f"""
            OPENING: {context.lawyer_opening}
            REBUTTAL: {context.lawyer_rebuttal}
            FINAL: {context.lawyer_final}
            """
            
            full_finance_position = f"""
            OPENING: {context.finance_opening}
            REBUTTAL: {context.finance_rebuttal}
            FINAL: {context.finance_final}
            """
            
            synthesis = await self.mediator.synthesize(
                full_lawyer_position,
                full_finance_position,
                context.query
            )
            context.synthesis = synthesis
            context.messages.append(DebateMessage(
                agent="The Mediator",
                role="mediator",
                round=DebateRound.SYNTHESIS.value,
                content=synthesis["verdict"],
                timestamp=datetime.now(),
                is_rebuttal=False
            ))
        
        return context
    
    async def stream_debate(self, query: str, session_id: str):
        """
        Generator that yields debate messages as they're created
        Allows for real-time streaming to the UI
        """
        context = DebateContext(
            query=query,
            session_id=session_id,
            current_state=DebateState.INIT,
            current_round=DebateRound.OPENING
        )
        
        previous_message_count = 0
        
        while context.current_state != DebateState.COMPLETE:
            # Add typing delay BEFORE generating the message
            # This simulates the agent "thinking"
            if context.current_state != DebateState.INIT:
                await asyncio.sleep(2.5)  # 2.5 seconds typing animation
            
            context = await self._execute_state(context)
            
            # Yield new messages immediately after generation
            for msg in context.messages[previous_message_count:]:
                yield msg
                # Small delay after message appears before next typing starts
                await asyncio.sleep(0.3)
            
            previous_message_count = len(context.messages)
            
            # Transition to next state
            if context.current_state in self.transitions:
                context.current_state = self.transitions[context.current_state]
            else:
                break
        
        # Return final context with synthesis
        yield context
