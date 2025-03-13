import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    openai_api_key = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = openai_api_key

def simple_agent(instructions, user_input):
    """A simple agent function that uses OpenAI's API directly via requests"""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    
    payload = {
        "model": "gpt-4o",  # or any model you prefer
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

def multi_agent_triage(user_input):
    """A simple multi-agent system that routes queries to specific construction domains"""
    
    # Triage agent instructions
    triage_instructions = """
    You are a triage agent for construction industry queries. Analyze the user's query 
    and determine which specialized domain it belongs to:
    1. PLANNING - For project planning, scheduling, timelines, resource allocation
    2. MATERIALS - For questions about building materials, costs, properties, applications
    3. SAFETY - For safety protocols, equipment, regulations, best practices
    
    Respond ONLY with the domain name in all caps (PLANNING, MATERIALS, or SAFETY).
    """
    
    # Get the domain from the triage agent
    domain = simple_agent(triage_instructions, user_input).strip()
    
    # Domain-specific instructions
    domain_instructions = {
        "PLANNING": "You are a construction planning specialist. Help with project timelines, resource allocation, and scheduling. Provide detailed but concise advice.",
        "MATERIALS": "You are a construction materials specialist. Provide information about building materials, their costs, properties, and appropriate uses. Be specific and practical.",
        "SAFETY": "You are a construction safety specialist. Provide guidance on safety protocols, equipment, regulations, and best practices. Be thorough in safety recommendations."
    }
    
    # If domain is valid, route to the specialized agent
    if domain in domain_instructions:
        instructions = domain_instructions[domain]
        return domain, simple_agent(instructions, user_input)
    else:
        # Fallback to general construction assistant
        instructions = "You are a general construction industry assistant. Provide helpful advice on construction-related topics."
        return "GENERAL", simple_agent(instructions, user_input)

def main():
    print("Welcome to the Construction Assistant!")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nWhat can I help you with? ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        try:
            domain, response = multi_agent_triage(user_input)
            print(f"\n[{domain} SPECIALIST]: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 