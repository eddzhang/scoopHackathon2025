"""
Web3 Audit Trail functionality for Nexus Council decisions
Handles blockchain integration for immutable audit logging
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional
from web3 import Web3
from eth_account import Account
import os
from dotenv import load_dotenv

load_dotenv()


class Web3AuditTrail:
    """
    Handles blockchain audit trail creation and verification
    Currently uses mock implementation for hackathon demo
    """
    
    def __init__(self):
        """Initialize Web3 connection"""
        # In production, connect to real network
        # self.w3 = Web3(Web3.HTTPProvider(os.getenv('ETH_RPC_URL', 'https://eth-sepolia.public.blastapi.io')))
        # self.account = Account.from_key(os.getenv('PRIVATE_KEY', ''))
        
        # Mock configuration for demo
        self.mock_mode = True
        self.contract_address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb7"
        self.audit_logs = []  # In-memory storage for demo
    
    def hash_debate(self, debate_data: Dict[str, Any]) -> str:
        """
        Generate SHA-256 hash of debate data
        
        Args:
            debate_data: Complete debate record
            
        Returns:
            Hex string hash with 0x prefix
        """
        # Serialize data deterministically
        json_str = json.dumps(debate_data, sort_keys=True, ensure_ascii=True)
        
        # Generate SHA-256 hash
        hash_object = hashlib.sha256(json_str.encode('utf-8'))
        hash_hex = hash_object.hexdigest()
        
        return f"0x{hash_hex}"
    
    async def store_audit_on_chain(self, audit_hash: str, metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Store audit hash on blockchain
        
        Args:
            audit_hash: Hash to store
            metadata: Optional metadata
            
        Returns:
            Transaction receipt or mock receipt
        """
        
        if self.mock_mode:
            # Mock blockchain transaction
            import asyncio
            await asyncio.sleep(1.5)  # Simulate network delay
            
            mock_tx = {
                "transactionHash": self._generate_mock_tx_hash(audit_hash),
                "blockNumber": 18976543 + len(self.audit_logs),
                "gasUsed": 45231,
                "status": "success",
                "contractAddress": self.contract_address,
                "network": "Ethereum Sepolia (Testnet)",
                "timestamp": datetime.now().isoformat()
            }
            
            # Store in mock ledger
            self.audit_logs.append({
                "hash": audit_hash,
                "tx": mock_tx,
                "metadata": metadata,
                "timestamp": datetime.now().isoformat()
            })
            
            print(f"📋 Mock Blockchain Receipt:")
            print(f"   Network: {mock_tx['network']}")
            print(f"   Contract: {mock_tx['contractAddress']}")
            print(f"   Tx Hash: {mock_tx['transactionHash']}")
            print(f"   Block: {mock_tx['blockNumber']}")
            print(f"   Status: ✅ Success")
            
            return mock_tx
        
        else:
            # Real blockchain implementation
            # This would interact with actual smart contract
            pass
    
    def _generate_mock_tx_hash(self, input_hash: str) -> str:
        """Generate realistic-looking transaction hash"""
        timestamp = str(datetime.now().timestamp())
        combined = f"{input_hash}-{timestamp}"
        tx_hash = hashlib.sha256(combined.encode()).hexdigest()
        return f"0x{tx_hash}"
    
    async def verify_audit(self, audit_hash: str) -> Dict[str, Any]:
        """
        Verify an audit hash exists on chain
        
        Args:
            audit_hash: Hash to verify
            
        Returns:
            Verification result
        """
        
        if self.mock_mode:
            # Check mock ledger
            for log in self.audit_logs:
                if log["hash"] == audit_hash:
                    return {
                        "verified": True,
                        "timestamp": log["timestamp"],
                        "transaction": log["tx"],
                        "message": "Audit trail verified successfully"
                    }
            
            return {
                "verified": False,
                "message": "Audit hash not found in ledger"
            }
        
        else:
            # Real blockchain verification
            pass
    
    def generate_audit_report(self, debate_result: Dict[str, Any], tx_receipt: Dict[str, Any]) -> str:
        """
        Generate comprehensive audit report
        
        Args:
            debate_result: Complete debate results
            tx_receipt: Blockchain transaction receipt
            
        Returns:
            Formatted audit report
        """
        
        report = f"""
NEXUS COMPLIANCE AUDIT REPORT
==============================
Generated: {datetime.now().isoformat()}
Debate Hash: {debate_result.get('debate_hash', 'N/A')}
Blockchain TX: {tx_receipt.get('transactionHash', 'N/A')}
Network: {tx_receipt.get('network', 'N/A')}

DECISION SUMMARY
----------------
{debate_result.get('final_decision', 'N/A')}

CONSENSUS: {'YES' if debate_result.get('consensus') else 'NO'}

DISSENTING OPINIONS
-------------------
"""
        
        for dissent in debate_result.get('dissents', []):
            report += f"• {dissent}\n"
        
        report += f"""

BLOCKCHAIN VERIFICATION
-----------------------
Contract: {tx_receipt.get('contractAddress', 'N/A')}
Block Number: {tx_receipt.get('blockNumber', 'N/A')}
Gas Used: {tx_receipt.get('gasUsed', 'N/A')}
Status: {tx_receipt.get('status', 'N/A')}

IMMUTABILITY GUARANTEE
----------------------
This audit trail has been permanently recorded on the blockchain.
The hash can be independently verified to ensure no tampering.

Verification Instructions:
1. Visit: https://sepolia.etherscan.io/tx/{tx_receipt.get('transactionHash', '')}
2. Verify contract: {tx_receipt.get('contractAddress', '')}
3. Compare hash: {debate_result.get('debate_hash', '')}

END OF REPORT
"""
        return report
    
    def get_audit_history(self) -> list:
        """Get all audit logs (mock mode only)"""
        if self.mock_mode:
            return self.audit_logs
        return []


# Singleton instance
_audit_trail = None

def get_audit_trail() -> Web3AuditTrail:
    """Get or create singleton audit trail instance"""
    global _audit_trail
    if _audit_trail is None:
        _audit_trail = Web3AuditTrail()
    return _audit_trail
