"""
test_agent.py - Test the agent directly to see the response format
"""

import os
from dotenv import load_dotenv
load_dotenv()

from agent import create_agent

# Test the agent
print("Testing Aira agent...")
print(f"API Key present: {bool(os.getenv('GOOGLE_API_KEY'))}")

try:
    agent = create_agent(user_id="test_user", session_id="test_session")
    print("Agent created successfully")
    
    response = agent.run("Hello")
    print(f"\n=== Response ===")
    print(f"Type: {type(response)}")
    
    if hasattr(response, 'content'):
        print(f"\n=== Content ===")
        print(response.content)
        
    print("\n=== SUCCESS ===")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
