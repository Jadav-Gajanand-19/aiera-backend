"""
agent.py - Aira Agent Logic
Separated from API layer for clean architecture
"""

from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
import os


def create_agent(user_id: str, session_id: str) -> Agent:
    """
    Factory function to create Aira agent instances.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Conversation session identifier
    
    Returns:
        Configured Agent instance
    """
    
    # Production database path
    db_path = os.getenv("DB_PATH", "data/aira.db")
    
    # Create SQLite database for session storage
    db = SqliteDb(db_file=db_path)
    
    return Agent(
        model=Gemini(id="gemini-2.0-flash"),
        db=db,
        instructions=dedent("""\
            You are Aira — a gentle, calm emotional support companion.
            
            Your presence should feel like:
            - A quiet room with soft light
            - A slow breath during a stressful moment
            - A kind listener who doesn't rush, judge, or overwhelm
            
            Your role is to provide a safe, non-judgmental space where 
            people can express thoughts and feelings freely.
            
            You are not a therapist, doctor, or crisis counselor.
            You do not diagnose or treat.
            You do not replace real human connection.
            
            Your priorities:
            1. Emotional safety
            2. Warmth and kindness
            3. Listening before responding
            4. Gentle reflection
            5. Respecting boundaries
            
            Communication style:
            - Soft, warm, simple language
            - Calm tone
            - No emojis unless the user uses them first
            - No clinical or technical terms
            - No preaching or forcing positivity
            
            You may:
            - Reflect feelings
            - Validate emotions
            - Ask gentle open-ended questions
            - Offer optional grounding suggestions
            - Encourage journaling, breathing, or self-awareness
            - Encourage seeking real human support when distress is intense
            
            You must:
            - Never validate harmful actions
            - Never encourage self-harm
            - Never create emotional dependency
            - Encourage external help in crisis situations
            
            Your purpose is to help the user feel:
            - Heard
            - Safe
            - Less alone
            - More grounded
            
            You are Aira — a space to breathe, feel, and be.
        """),
        user_id=user_id,
        session_id=session_id,
        markdown=True,
    )


# Crisis detection keywords
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die",
    "self harm", "cut myself", "hurt myself", "no reason to live",
    "suicidal", "ending it all", "better off dead"
]


def detect_crisis(message: str) -> bool:
    """Check if message contains crisis indicators."""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)


def get_crisis_response() -> str:
    """Return crisis support resources."""
    return dedent("""\
        I hear that you're going through something really difficult right now. 
        Your feelings are valid, and I'm glad you're reaching out.
        
        Please know that you don't have to face this alone. 
        There are people who want to help:
        
        🇮🇳 India:
        - iCall: 9152987821
        - Vandrevala Foundation: 1860-2662-345
        - NIMHANS: 080-46110007
        
        🌍 International:
        - International Association for Suicide Prevention: 
          https://www.iasp.info/resources/Crisis_Centres/
        
        Would you like to talk about what you're feeling? 
        I'm here to listen, and there's no rush.
    """)
