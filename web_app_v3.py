"""
FastAPI web application for Nexus AI Adversarial System
Multi-Round Debate with Real-Time Streaming
"""

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import asyncio
import json
from datetime import datetime
import uuid
import hashlib

# Import our debate orchestrator
from debate_orchestrator import DebateOrchestrator, DebateMessage as OrchestratorMessage
from debate_orchestrator_llm import DebateOrchestratorLLM, DebateMessage as LLMMessage
from blockchain_audit import auditor

import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Pydantic models
class QueryRequest(BaseModel):
    query: str


class DebateMessage(BaseModel):
    agent: str
    role: str
    round: str
    content: str
    timestamp: str
    is_rebuttal: bool = False


class DebateResponse(BaseModel):
    session_id: str
    messages: List[DebateMessage]
    summary: Dict[str, Any]
    audit_hash: str


# Initialize FastAPI
app = FastAPI(
    title="Nexus Adversarial System v3",
    description="Multi-round AI debate with real-time rebuttals",
    version="3.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the orchestrator
# Check if we should use LLM version
USE_LLM = os.getenv('USE_LLM', 'true').lower() == 'true'
logger.info(f"USE_LLM setting: {USE_LLM}")

if USE_LLM:
    logger.info("Initializing LLM-powered orchestrator...")
    try:
        from debate_orchestrator_llm import orchestrator_llm
        orchestrator = orchestrator_llm
        logger.info("✅ Using LLM-powered orchestrator")
    except Exception as e:
        logger.error(f"Failed to initialize LLM orchestrator: {e}")
        logger.info("Falling back to mock orchestrator")
        orchestrator = DebateOrchestrator()
else:
    logger.info("Using mock orchestrator (USE_LLM=false)")
    orchestrator = DebateOrchestrator()
sessions = {}
active_websockets = []

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the multi-round debate interface"""
    try:
        with open("templates/debate_v3.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        # Fallback to inline HTML if template not found
        return HTMLResponse(content="<h1>Template not found. Please check templates/debate_v3.html</h1>")


@app.websocket("/ws/debate")
async def websocket_debate(websocket: WebSocket):
    """WebSocket endpoint for real-time debate streaming"""
    await websocket.accept()
    active_websockets.append(websocket)
    
    try:
        while True:
            # Receive query from client
            data = await websocket.receive_json()
            query = data.get("query")
            session_id = str(uuid.uuid4())
            
            # Stream debate messages
            logger.info(f"Starting debate stream for query: {query[:50]}...")
            async for item in orchestrator.stream_debate(query, session_id):
                # Handle both message types
                if isinstance(item, (OrchestratorMessage, LLMMessage)):
                    # Convert to dict and send
                    message_data = {
                        "type": "message",
                        "agent": item.agent,
                        "role": item.role,
                        "round": item.round,
                        "content": item.content,
                        "timestamp": item.timestamp.isoformat(),
                        "is_rebuttal": item.is_rebuttal
                    }
                    await websocket.send_json(message_data)
                else:
                    # Final context with synthesis
                    context = item
                    synthesis = context.synthesis
                    
                    # Send synthesis with metadata
                    if synthesis:
                        # Extract metadata from synthesis
                        metadata = synthesis.get("metadata", {})
                        
                        # Create summary structure from metadata
                        summary_data = {
                            "risk_score": metadata.get("risk_score", "UNKNOWN"),
                            "risk_color": metadata.get("risk_color", "#64748b"),
                            "cost_of_delay": metadata.get("cost_of_delay", "Unknown"),
                            "confidence": metadata.get("confidence", 0),
                            "approach": metadata.get("approach", "Needs Analysis")
                        }
                        
                        logger.info(f"Sending synthesis metadata: {summary_data}")
                        
                        await websocket.send_json({
                            "type": "synthesis",
                            "summary": summary_data,
                            "metadata": metadata
                        })
                        
                        # Record to blockchain
                        await websocket.send_json({
                            "type": "audit_status",
                            "status": "recording",
                            "message": "Recording to blockchain..."
                        })
                        
                        # Submit audit to blockchain
                        audit_result = await auditor.record_decision(
                            query=query,
                            debate_messages=context.messages,
                            synthesis=synthesis,
                            session_id=session_id
                        )
                        
                        if audit_result["success"]:
                            await websocket.send_json({
                                "type": "audit",
                                "tx_hash": audit_result["tx_hash"],
                                "explorer_url": audit_result["explorer_url"],
                                "content_hash": audit_result["content_hash"][:16] + "...",
                                "status": "completed"
                            })
                        else:
                            await websocket.send_json({
                                "type": "audit",
                                "status": "failed",
                                "error": audit_result.get("error", "Unknown error")
                            })
                    
    except WebSocketDisconnect:
        active_websockets.remove(websocket)
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
        active_websockets.remove(websocket)


@app.post("/api/debate")
async def run_debate(request: QueryRequest):
    """Run multi-round debate (non-streaming fallback)"""
    
    try:
        session_id = str(uuid.uuid4())
        messages = []
        
        # Run full debate
        context = await orchestrator.run_debate(request.query, session_id)
        
        # Convert messages
        for msg in context.messages:
            messages.append(DebateMessage(
                agent=msg.agent,
                role=msg.role,
                round=msg.round,
                content=msg.content,
                timestamp=msg.timestamp.isoformat(),
                is_rebuttal=msg.is_rebuttal
            ))
        
        # Generate audit hash
        audit_data = {
            "session_id": session_id,
            "query": request.query,
            "debate_rounds": len(context.messages),
            "timestamp": datetime.now().isoformat()
        }
        
        audit_string = json.dumps(audit_data, sort_keys=True)
        audit_hash = f"0x{hashlib.sha256(audit_string.encode()).hexdigest()[:16]}..."
        
        # Store session
        sessions[session_id] = {
            "messages": messages,
            "summary": context.synthesis,
            "audit_hash": audit_hash
        }
        
        return DebateResponse(
            session_id=session_id,
            messages=messages,
            summary=context.synthesis or {},
            audit_hash=audit_hash
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents": ["Paranoid Lawyer", "Greedy Finance", "Mediator"],
        "version": "3.0.0",
        "features": ["multi-round", "rebuttals", "streaming"]
    }


if __name__ == "__main__":
    import uvicorn
    print("\nNEXUS ADVERSARIAL SYSTEM v3")
    print("="*40)
    print("Multi-Round Debate with Real-Time Rebuttals")
    print("Starting server on http://localhost:8001")
    print("="*40)
    uvicorn.run(app, host="0.0.0.0", port=8001)
