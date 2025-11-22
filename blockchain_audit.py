"""
Blockchain Audit Trail for Debate Decisions
Records debate outcomes and reasoning on-chain for compliance
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import uuid

class BlockchainAuditor:
    """
    Handles creation and submission of audit records to blockchain
    """
    
    def __init__(self):
        self.pending_audits = {}
        
    def create_audit_payload(self, 
                            query: str, 
                            debate_messages: list,
                            synthesis: Dict[str, Any],
                            session_id: str) -> Dict[str, Any]:
        """
        Create structured audit record for blockchain submission
        """
        # Extract debate rounds from messages
        rounds = {
            "opening": {"lawyer": None, "finance": None},
            "rebuttal": {"lawyer": None, "finance": None},
            "final": {"lawyer": None, "finance": None}
        }
        
        for msg in debate_messages:
            if msg.role == "lawyer":
                if msg.round == "opening":
                    rounds["opening"]["lawyer"] = msg.content
                elif msg.round == "rebuttal":
                    rounds["rebuttal"]["lawyer"] = msg.content
                elif msg.round == "final":
                    rounds["final"]["lawyer"] = msg.content
            elif msg.role == "finance":
                if msg.round == "opening":
                    rounds["opening"]["finance"] = msg.content
                elif msg.round == "rebuttal":
                    rounds["rebuttal"]["finance"] = msg.content
                elif msg.round == "final":
                    rounds["final"]["finance"] = msg.content
        
        # Build audit payload
        payload = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "session_id": session_id,
            "query": query,
            "debate": {
                "round1_opening": rounds["opening"],
                "round2_rebuttal": rounds["rebuttal"],
                "round3_final": rounds["final"]
            },
            "synthesis": {
                "verdict": synthesis.get("verdict", ""),
                "risk_score": synthesis.get("risk_score", ""),
                "risk_color": synthesis.get("risk_color", ""),
                "cost_of_delay": synthesis.get("cost_of_delay", ""),
                "confidence": synthesis.get("confidence", 0),
                "approach": synthesis.get("approach", "")
            },
            "decision": {
                "risk_score": synthesis.get("risk_score", ""),
                "cost_of_delay": synthesis.get("cost_of_delay", ""),
                "confidence": synthesis.get("confidence", 0),
                "recommendation": synthesis.get("approach", "")
            }
        }
        
        return payload
    
    def hash_payload(self, payload: Dict[str, Any]) -> str:
        """
        Create SHA-256 hash of the audit payload
        """
        payload_string = json.dumps(payload, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(payload_string.encode()).hexdigest()
    
    async def submit_to_blockchain(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit audit hash to blockchain (NEO L1 or similar)
        For demo, simulates blockchain submission
        """
        # Hash the payload
        content_hash = self.hash_payload(payload)
        
        # Generate transaction ID (simulated for demo)
        tx_hash = f"0x{hashlib.sha256(f'{content_hash}{datetime.now()}'.encode()).hexdigest()[:40]}"
        
        # Simulate blockchain submission delay
        await asyncio.sleep(2.0)
        
        # In production, this would call NEO RPC or use neo-py:
        # from neo.api.rpc import RPCClient
        # client = RPCClient("https://mainnet.neo.org")
        # tx = await client.submit_data_transaction(content_hash)
        
        # Return transaction details
        return {
            "success": True,
            "tx_hash": tx_hash,
            "block_number": 15234567 + hash(tx_hash) % 1000,  # Simulated
            "content_hash": content_hash,
            "explorer_url": f"https://neoscan.io/transaction/{tx_hash}",
            "timestamp": datetime.now().isoformat()
        }
    
    async def record_decision(self, 
                            query: str,
                            debate_messages: list,
                            synthesis: Dict[str, Any],
                            session_id: str) -> Dict[str, Any]:
        """
        Complete audit recording flow
        """
        # Create audit payload
        payload = self.create_audit_payload(query, debate_messages, synthesis, session_id)
        
        # Store pending audit
        self.pending_audits[session_id] = {
            "status": "recording",
            "payload": payload
        }
        
        try:
            # Submit to blockchain
            result = await self.submit_to_blockchain(payload)
            
            # Update pending audit
            self.pending_audits[session_id] = {
                "status": "completed",
                "payload": payload,
                "blockchain": result
            }
            
            return result
            
        except Exception as e:
            self.pending_audits[session_id] = {
                "status": "failed",
                "error": str(e)
            }
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_audit_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status of a pending audit
        """
        return self.pending_audits.get(session_id)

# Global auditor instance
auditor = BlockchainAuditor()
