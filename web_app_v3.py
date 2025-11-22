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
from blockchain_audit import auditor


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

# Global instances
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
            async for item in orchestrator.stream_debate(query, session_id):
                if isinstance(item, OrchestratorMessage):
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
                    
                    # Send synthesis
                    if synthesis:
                        # Create summary structure from synthesis data
                        summary_data = {
                            "risk_score": synthesis.get("risk_score", "UNKNOWN"),
                            "risk_color": synthesis.get("risk_color", "#64748b"),
                            "cost_of_delay": synthesis.get("cost_of_delay", "Unknown"),
                            "confidence": synthesis.get("confidence", 0),
                            "approach": synthesis.get("approach", "Needs Analysis")
                        }
                        
                        await websocket.send_json({
                            "type": "synthesis",
                            "summary": summary_data
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
