"""
Nexus AI Council - Main orchestration using SpoonOS StateGraph
Implements debate workflow between three specialized agents
"""

from typing import TypedDict, Dict, Any, List, Optional, Annotated
from spoon_ai.graph import StateGraph, GraphAgent, END, RunnableNode
from spoon_ai.chat import ChatBot
from spoon_ai.llm import LLMManager
from agents.legal_scholar import LegalScholarAgent
from agents.tax_comptroller import TaxComptrollerAgent
from agents.growth_hacker import GrowthHackerAgent
import asyncio
import hashlib
import json
from datetime import datetime


# Define the state schema for our debate workflow
class DebateState(TypedDict):
    """State schema for the Nexus Council debate"""
    user_query: str
    legal_analysis: Annotated[Optional[str], "Legal compliance analysis"]
    tax_analysis: Annotated[Optional[str], "Tax implications analysis"] 
    growth_analysis: Annotated[Optional[str], "Growth strategy analysis"]
    debate_rounds: Annotated[List[Dict[str, str]], "History of debate rounds"]
    final_decision: Annotated[Optional[str], "Synthesized council decision"]
    consensus: Annotated[bool, "Whether consensus was reached"]
    dissents: Annotated[List[str], "List of dissenting opinions"]
    debate_hash: Annotated[Optional[str], "SHA-256 hash of debate for audit"]


class NexusCouncil:
    """
    Main orchestration class for the Nexus AI Council
    Manages the debate workflow between three specialized agents
    """
    
    def __init__(self, llm_manager: Optional[LLMManager] = None):
        """Initialize the council with agents and workflow"""
        
        # Initialize LLM manager
        self.llm_manager = llm_manager or LLMManager()
        
        # Create ChatBot instance for agents
        self.chatbot = ChatBot(llm_manager=self.llm_manager)
        
        # Initialize the three council agents
        self.legal_agent = LegalScholarAgent(llm=self.chatbot)
        self.tax_agent = TaxComptrollerAgent(llm=self.chatbot)
        self.growth_agent = GrowthHackerAgent(llm=self.chatbot)
        
        # Build the debate workflow graph
        self.graph = self._build_debate_graph()
        
        # Create the graph agent for execution
        self.agent = GraphAgent(
            name="nexus_council",
            graph=self.graph,
            preserve_state=True
        )
        
        print("🏛️ Nexus Council initialized successfully")
        print("Council Members:")
        print("  ⚖️  Dr. Miranda Blackstone, Esq. (Legal Scholar)")
        print("  💰 Harold P. Pennywhistle, CPA (Tax Comptroller)")
        print("  🚀 Blake 'Rocket' Morrison (Growth Hacker)\n")
    
    def _build_debate_graph(self) -> StateGraph:
        """Build the debate workflow graph"""
        
        # Create the state graph
        graph = StateGraph(DebateState)
        
        # Add nodes for each agent's initial analysis
        graph.add_node("legal_analysis", RunnableNode("legal", self._legal_analysis))
        graph.add_node("tax_analysis", RunnableNode("tax", self._tax_analysis))
        graph.add_node("growth_analysis", RunnableNode("growth", self._growth_analysis))
        
        # Add debate round nodes
        graph.add_node("debate_round_1", RunnableNode("debate1", self._conduct_debate_round))
        graph.add_node("debate_round_2", RunnableNode("debate2", self._conduct_debate_round))
        
        # Add synthesis node
        graph.add_node("synthesize", RunnableNode("synthesis", self._synthesize_decision))
        
        # Add audit trail node
        graph.add_node("create_audit", RunnableNode("audit", self._create_audit_trail))
        
        # Define the execution flow
        graph.set_entry_point("legal_analysis")
        
        # Parallel initial analysis
        graph.add_edge("legal_analysis", "tax_analysis")
        graph.add_edge("tax_analysis", "growth_analysis")
        
        # Debate rounds
        graph.add_edge("growth_analysis", "debate_round_1")
        graph.add_edge("debate_round_1", "debate_round_2")
        
        # Synthesis and audit
        graph.add_edge("debate_round_2", "synthesize")
        graph.add_edge("synthesize", "create_audit")
        graph.add_edge("create_audit", END)
        
        return graph.compile()
    
    async def _legal_analysis(self, state: DebateState) -> Dict[str, Any]:
        """Run legal compliance analysis"""
        print("\n⚖️  Legal Scholar analyzing...")
        
        # Set query in agent memory
        await self.legal_agent.add_message("user", state["user_query"])
        
        # Run analysis
        analysis = await self.legal_agent.run()
        
        return {
            "legal_analysis": analysis,
            "debate_rounds": [{"agent": "legal", "content": analysis}]
        }
    
    async def _tax_analysis(self, state: DebateState) -> Dict[str, Any]:
        """Run tax implications analysis"""
        print("💰 Tax Comptroller analyzing...")
        
        # Set query in agent memory
        await self.tax_agent.add_message("user", state["user_query"])
        
        # Run analysis
        analysis = await self.tax_agent.run()
        
        # Append to debate rounds
        rounds = state.get("debate_rounds", [])
        rounds.append({"agent": "tax", "content": analysis})
        
        return {
            "tax_analysis": analysis,
            "debate_rounds": rounds
        }
    
    async def _growth_analysis(self, state: DebateState) -> Dict[str, Any]:
        """Run growth strategy analysis"""
        print("🚀 Growth Hacker analyzing...")
        
        # Set query in agent memory
        await self.growth_agent.add_message("user", state["user_query"])
        
        # Run analysis
        analysis = await self.growth_agent.run()
        
        # Append to debate rounds
        rounds = state.get("debate_rounds", [])
        rounds.append({"agent": "growth", "content": analysis})
        
        return {
            "growth_analysis": analysis,
            "debate_rounds": rounds
        }
    
    async def _conduct_debate_round(self, state: DebateState) -> Dict[str, Any]:
        """Conduct a round of debate between agents"""
        round_num = len([r for r in state.get("debate_rounds", []) if "Round" in r.get("content", "")]) + 1
        print(f"\n🔄 Conducting Debate Round {round_num}...")
        
        rounds = state.get("debate_rounds", [])
        
        # Each agent responds to the others
        other_analyses = f"""
        Legal position: {state.get('legal_analysis', 'No analysis yet')}
        Tax position: {state.get('tax_analysis', 'No analysis yet')}
        Growth position: {state.get('growth_analysis', 'No analysis yet')}
        """
        
        # Legal response
        await self.legal_agent.add_message("user", f"Respond to other positions: {other_analyses}")
        legal_response = await self.legal_agent.run()
        rounds.append({"agent": "legal", "content": f"Round {round_num}: {legal_response}"})
        
        # Tax response  
        await self.tax_agent.add_message("user", f"Respond to other positions: {other_analyses}")
        tax_response = await self.tax_agent.run()
        rounds.append({"agent": "tax", "content": f"Round {round_num}: {tax_response}"})
        
        # Growth response
        await self.growth_agent.add_message("user", f"Respond to other positions: {other_analyses}")
        growth_response = await self.growth_agent.run()
        rounds.append({"agent": "growth", "content": f"Round {round_num}: {growth_response}"})
        
        return {"debate_rounds": rounds}
    
    async def _synthesize_decision(self, state: DebateState) -> Dict[str, Any]:
        """Synthesize final decision from debate"""
        print("\n📋 Synthesizing council decision...")
        
        # Check for consensus
        legal = state.get("legal_analysis", "")
        tax = state.get("tax_analysis", "")
        growth = state.get("growth_analysis", "")
        
        legal_blocks = "❌" in legal or "risk" in legal.lower()
        tax_blocks = "❌" in tax or "exposure" in tax.lower()
        growth_pushes = "✅" in growth and "ship" in growth.lower()
        
        consensus = not (legal_blocks and tax_blocks and growth_pushes)
        
        # Collect dissents
        dissents = []
        if legal_blocks:
            dissents.append("Legal Scholar: Significant compliance risks must be addressed")
        if tax_blocks:
            dissents.append("Tax Comptroller: Unacceptable tax exposure detected")
        if not growth_pushes:
            dissents.append("Growth Hacker: Missing growth opportunity")
        
        # Create final decision
        if legal_blocks or tax_blocks:
            decision = """
📋 **NEXUS COUNCIL DECISION**

After extensive deliberation, the Council recommends:

**Decision: PROCEED WITH CAUTION** ⚠️

**Key Findings:**
1. Legal: Critical compliance issues identified that require immediate attention
2. Tax: Significant financial exposure that needs restructuring
3. Growth: Strong market opportunity but must be balanced with compliance

**Required Actions Before Proceeding:**
1. Complete comprehensive legal review and implement safeguards
2. Restructure operations to minimize tax nexus exposure
3. Phase rollout to balance growth with compliance milestones

**Risk Assessment:** MEDIUM-HIGH
**Compliance Priority:** CRITICAL
**Implementation:** Phased approach with legal checkpoints

The Council emphasizes that while the growth opportunity is compelling, 
regulatory compliance and tax optimization must be addressed to ensure 
long-term sustainability and avoid potentially catastrophic penalties.
"""
        else:
            decision = """
📋 **NEXUS COUNCIL DECISION**

After extensive deliberation, the Council recommends:

**Decision: PROCEED WITH MONITORING** ✅

**Key Findings:**
1. Legal: Manageable compliance requirements identified
2. Tax: Acceptable tax implications with optimization opportunities
3. Growth: Strong market opportunity with first-mover advantage

**Recommended Approach:**
1. Implement basic compliance documentation
2. Set up tax-efficient structure as outlined
3. Launch quickly while maintaining audit trail

**Risk Assessment:** LOW-MEDIUM
**Growth Priority:** HIGH
**Implementation:** Immediate with compliance monitoring

The Council finds this opportunity favorable with manageable risks.
Proceed with implementation while maintaining compliance documentation.
"""
        
        return {
            "final_decision": decision,
            "consensus": consensus,
            "dissents": dissents
        }
    
    async def _create_audit_trail(self, state: DebateState) -> Dict[str, Any]:
        """Create immutable audit trail hash"""
        print("🔐 Creating audit trail...")
        
        # Create audit log
        audit_log = {
            "timestamp": datetime.now().isoformat(),
            "query": state["user_query"],
            "decision": state["final_decision"],
            "consensus": state["consensus"],
            "dissents": state["dissents"],
            "debate_rounds": state["debate_rounds"]
        }
        
        # Generate SHA-256 hash
        audit_string = json.dumps(audit_log, sort_keys=True)
        hash_object = hashlib.sha256(audit_string.encode())
        audit_hash = f"0x{hash_object.hexdigest()}"
        
        print(f"✅ Audit hash generated: {audit_hash[:16]}...")
        
        return {"debate_hash": audit_hash}
    
    async def deliberate(self, query: str) -> Dict[str, Any]:
        """
        Main entry point for council deliberation
        
        Args:
            query: Business compliance question to analyze
            
        Returns:
            Complete debate results including decision and audit hash
        """
        print("\n" + "="*60)
        print("🔮 NEXUS COUNCIL DELIBERATION STARTING")
        print("="*60)
        print(f"Query: {query}")
        print("-"*60)
        
        # Initialize state
        initial_state = DebateState(
            user_query=query,
            legal_analysis=None,
            tax_analysis=None,
            growth_analysis=None,
            debate_rounds=[],
            final_decision=None,
            consensus=False,
            dissents=[],
            debate_hash=None
        )
        
        # Run the debate workflow
        result = await self.agent.run(json.dumps(initial_state))
        
        # Parse result
        if isinstance(result, str):
            try:
                result = json.loads(result)
            except:
                pass
        
        print("\n" + "="*60)
        print("✅ DELIBERATION COMPLETE")
        print("="*60)
        
        return result
    
    def get_audit_report(self, result: Dict[str, Any]) -> str:
        """Generate formatted audit report"""
        
        report = f"""
NEXUS COMPLIANCE AUDIT REPORT
==============================
Generated: {datetime.now().isoformat()}
Debate Hash: {result.get('debate_hash', 'N/A')}

QUERY
-----
{result.get('user_query', 'N/A')}

DECISION SUMMARY
----------------
{result.get('final_decision', 'N/A')}

CONSENSUS: {'YES' if result.get('consensus') else 'NO'}

DISSENTING OPINIONS
-------------------
"""
        for dissent in result.get('dissents', []):
            report += f"• {dissent}\n"
        
        report += """

IMMUTABILITY GUARANTEE
----------------------
This audit trail has been hashed using SHA-256.
The hash can be used to verify no tampering has occurred.

END OF REPORT
"""
        return report


# CLI interface for testing
async def main():
    """Command-line interface for Nexus Council"""
    import sys
    
    print("\n🌟 Welcome to NEXUS - AI General Counsel\n")
    
    # Initialize council
    council = NexusCouncil()
    
    # Get query from command line or prompt
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        query = input("Enter your compliance question: ")
    
    # Run deliberation
    result = await council.deliberate(query)
    
    # Print audit report
    print(council.get_audit_report(result))


if __name__ == "__main__":
    asyncio.run(main())
