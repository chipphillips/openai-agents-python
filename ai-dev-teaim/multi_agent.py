import os
import json
import openai
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    openai_api_key = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Initialize the OpenAI client
client = openai.OpenAI(api_key=openai_api_key)

class Agent:
    """A simple agent class that can handle messages and decide when to hand off to another agent"""
    
    def __init__(self, name, instructions):
        self.name = name
        self.instructions = instructions
        self.messages = []
        
    def add_message(self, role, content):
        """Add a message to the conversation history"""
        self.messages.append({"role": role, "content": content})
        
    def reset_messages(self):
        """Reset the conversation history"""
        self.messages = []
        
    def process(self, user_input, available_agents=None):
        """Process user input and decide whether to respond or hand off to another agent"""
        # Add system instructions
        system_message = {
            "role": "system", 
            "content": self.instructions
        }
        
        if available_agents and len(available_agents) > 0:
            # Add handoff functionality to instructions
            agent_names = [agent.name for agent in available_agents if agent.name != self.name]
            system_message["content"] += f"\n\nYou can hand off the conversation to another agent if needed. Available agents: {', '.join(agent_names)}. To hand off, respond with JSON formatted as: {{\"handoff\": \"agent_name\"}}. Otherwise, respond normally."
        
        # Prepare messages for API call
        messages = [system_message]
        messages.extend(self.messages)
        messages.append({"role": "user", "content": user_input})
        
        # Call the API
        response = client.chat.completions.create(
            model="gpt-4o",  # or any model you prefer
            messages=messages,
            temperature=0.7,
        )
        
        response_content = response.choices[0].message.content
        
        # Check if this is a handoff response
        if available_agents and response_content.strip().startswith("{") and response_content.strip().endswith("}"):
            try:
                response_json = json.loads(response_content)
                if "handoff" in response_json:
                    target_agent_name = response_json["handoff"]
                    # Find the target agent
                    target_agent = next((a for a in available_agents if a.name == target_agent_name), None)
                    if target_agent:
                        # Add the handoff message 
                        handoff_message = f"I'm handing this conversation off to {target_agent_name}."
                        self.add_message("assistant", handoff_message)
                        
                        # Return indicating handoff
                        return {
                            "type": "handoff",
                            "message": handoff_message,
                            "target_agent": target_agent
                        }
            except json.JSONDecodeError:
                # Not a valid JSON, treat as a normal response
                pass
        
        # If we get here, it's a normal response
        self.add_message("assistant", response_content)
        return {
            "type": "response",
            "message": response_content
        }

def main():
    # Create our agents
    triage_agent = Agent(
        "Triage Agent", 
        "You are a triage agent that determines whether a request is related to construction planning, "
        "materials, or safety, and routes it to the appropriate specialized agent. "
        "Be brief and professional in your handoffs."
    )
    
    planning_agent = Agent(
        "Planning Agent",
        "You are a construction planning specialist. You help with project timelines, "
        "resource allocation, and scheduling. Provide detailed but concise advice on construction planning."
    )
    
    materials_agent = Agent(
        "Materials Agent",
        "You are a construction materials specialist. You provide information about building materials, "
        "their costs, properties, and appropriate uses. Be specific and practical in your advice."
    )
    
    safety_agent = Agent(
        "Safety Agent",
        "You are a construction safety specialist. You provide guidance on safety protocols, "
        "equipment, regulations, and best practices. Be thorough in safety recommendations."
    )
    
    # List of all available agents
    all_agents = [triage_agent, planning_agent, materials_agent, safety_agent]
    
    # Start with the triage agent
    current_agent = triage_agent
    
    print("Welcome to the Multi-Agent Construction Assistant!")
    print("Type 'exit' to quit or 'reset' to start a new conversation.")
    
    while True:
        user_input = input(f"\n[{current_agent.name}] What can I help you with? ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        if user_input.lower() == 'reset':
            print("Starting a new conversation.")
            for agent in all_agents:
                agent.reset_messages()
            current_agent = triage_agent
            continue
        
        # Process the input with the current agent
        result = current_agent.process(user_input, all_agents)
        
        if result["type"] == "handoff":
            print(f"\n[{current_agent.name}]: {result['message']}")
            current_agent = result["target_agent"]
            print(f"\n[System]: Now speaking with {current_agent.name}")
        else:
            print(f"\n[{current_agent.name}]: {result['message']}")

if __name__ == "__main__":
    main() 