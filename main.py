"""
main.py - Aira API Server
Production-ready FastAPI application for Railway deployment
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from uuid import uuid4

from agent import create_agent, detect_crisis, get_crisis_response

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Lifespan for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🌿 Aira is starting up...")
    os.makedirs("data", exist_ok=True)
    yield
    # Shutdown
    logger.info("🌿 Aira is shutting down gracefully...")


# FastAPI application
app = FastAPI(
    title="Aira API",
    description="A gentle emotional support companion API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware - Allow Flutter app requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=5000, description="User's message")
    session_id: str | None = Field(None, description="Optional session ID for conversation continuity")
    user_id: str | None = Field(None, description="Optional user identifier")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="Aira's response")
    session_id: str = Field(..., description="Session ID for this conversation")
    is_crisis: bool = Field(False, description="Whether crisis support was triggered")


# Endpoints
@app.get("/health")
async def health_check():
    """
    Health check endpoint for Railway and monitoring services.
    Returns a simple status to confirm the service is running.
    """
    return {"status": "healthy", "service": "aira", "version": "1.0.0"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to Aira and receive a response.
    
    - **message**: The user's message (required)
    - **session_id**: Optional session ID for conversation continuity
    - **user_id**: Optional user identifier for personalization
    
    Returns Aira's gentle, supportive response.
    """
    try:
        # Generate IDs if not provided
        session_id = request.session_id or str(uuid4())
        user_id = request.user_id or "anonymous"
        
        logger.info(f"Chat request - User: {user_id}, Session: {session_id[:8]}...")
        
        # Check for crisis indicators first
        is_crisis = detect_crisis(request.message)
        
        if is_crisis:
            logger.warning(f"Crisis detected for session {session_id[:8]}")
            return ChatResponse(
                response=get_crisis_response(),
                session_id=session_id,
                is_crisis=True
            )
        
        # Create agent and get response
        agent = create_agent(user_id=user_id, session_id=session_id)
        run_response = agent.run(request.message)
        
        # Extract text from RunResponse
        response_text = ""
        
        logger.info(f"Run response type: {type(run_response)}")
        
        if run_response is not None:
            # Check for content attribute first
            if hasattr(run_response, 'content') and run_response.content:
                content = run_response.content
                # Handle if content is a Response object (error case)
                if hasattr(content, 'text'):
                    response_text = content.text
                elif isinstance(content, str):
                    response_text = content
                else:
                    response_text = str(content)
            # Check for messages attribute
            elif hasattr(run_response, 'messages') and run_response.messages:
                for msg in reversed(run_response.messages):
                    if hasattr(msg, 'content') and msg.content:
                        content = msg.content
                        if isinstance(content, str):
                            response_text = content
                        else:
                            response_text = str(content)
                        break
            else:
                response_text = str(run_response)
        
        # Filter out error-like responses
        if not response_text or '<Response' in response_text or 'Error' in response_text:
            response_text = "I'm here with you. Would you like to share more?"
        
        logger.info(f"Response sent for session {session_id[:8]}: {response_text[:50]}...")
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            is_crisis=False
        )
        
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="I'm having trouble responding right now. Please try again in a moment."
        )


@app.get("/")
async def root():
    """
    Root endpoint with API information and available endpoints.
    """
    return {
        "name": "Aira",
        "tagline": "A gentle emotional support companion",
        "version": "1.0.0",
        "description": "Aira is a calm, supportive space where you can express your thoughts and feelings freely.",
        "endpoints": {
            "chat": {
                "method": "POST",
                "path": "/chat",
                "description": "Send a message to Aira"
            },
            "health": {
                "method": "GET",
                "path": "/health",
                "description": "Check service health"
            },
            "docs": {
                "method": "GET",
                "path": "/docs",
                "description": "Interactive API documentation"
            }
        }
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
