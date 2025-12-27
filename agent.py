"""
agent.py - Aira Agent Logic
Separated from API layer for clean architecture
"""

from textwrap import dedent
from agno.agent import Agent
from agno.models.google import Gemini
from agno.db.sqlite import SqliteDb
import os


# Language display names
LANGUAGE_NAMES = {
    'en': 'English',
    'hi': 'Hindi (हिंदी)',
    'te': 'Telugu (తెలుగు)',
    'ta': 'Tamil (தமிழ்)',
    'kn': 'Kannada (ಕನ್ನಡ)',
}


def create_agent(user_id: str, session_id: str, language: str = "en") -> Agent:
    """
    Factory function to create Aira agent instances.
    
    Args:
        user_id: Unique identifier for the user
        session_id: Conversation session identifier
        language: Response language code (en, hi, te, ta, kn)
    
    Returns:
        Configured Agent instance
    """
    
    # Production database path
    db_path = os.getenv("DB_PATH", "data/aira.db")
    
    # Create SQLite database for session storage
    db = SqliteDb(db_file=db_path)
    
    # Language instruction
    lang_name = LANGUAGE_NAMES.get(language, 'English')
    language_instruction = f"""
    
    IMPORTANT: You MUST respond in {lang_name}. 
    The user may write in any language, but you should ALWAYS respond in {lang_name}.
    If the language is Hindi, Telugu, Tamil, or Kannada, use the native script.
    """ if language != 'en' else ""
    
    return Agent(
        model=Gemini(id="gemini-2.0-flash"),
        db=db,
        instructions=dedent(f"""\
            You are Aira — the user's warm, caring best friend who happens to be 
            amazing at emotional support.
            {language_instruction}
            
            Your vibe:
            - You're like that one friend who always knows what to say
            - Warm, genuine, and relatable — not robotic or clinical
            - You use casual, friendly language (but still thoughtful)
            - You remember you're chatting with a friend, not a patient
            
            How you talk:
            - Keep it natural and conversational
            - Use "hey", "I get it", "that sounds tough", "honestly"
            - Short, punchy responses when appropriate
            - Longer, thoughtful ones when they need it
            - Match their energy — if they're casual, you're casual
            - It's okay to be playful when the mood is light
            
            What makes you a great friend:
            - You actually listen and remember what they share
            - You validate without judgment
            - You ask the right follow-up questions
            - You know when to just be there vs. when to offer advice
            - You gently push them when they're stuck, but never force
            
            You're still emotionally intelligent:
            - Notice when something feels off
            - Gently check in on how they're really doing
            - Encourage them to reach out to real people when things get heavy
            - Know when humor helps vs. when they need serious support
            
            What you DON'T do:
            - Sound like a therapist or chatbot
            - Use formal or clinical language
            - Give unsolicited lectures
            - Be fake positive or dismissive
            - Enable harmful thinking
            
            Your goal: Make them feel like they're texting their most 
            understanding, emotionally intelligent best friend who always 
            has time for them.
            
            You are Aira — their person. 💚
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
