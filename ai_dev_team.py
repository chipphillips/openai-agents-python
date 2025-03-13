import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
load_dotenv()

# Set up OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    openai_api_key = input("Please enter your OpenAI API key: ")
    os.environ["OPENAI_API_KEY"] = openai_api_key

class SpecializedAgent:
    """Represents a specialized agent with specific domain expertise"""
    
    def __init__(self, name, instructions, description=None):
        self.name = name
        self.instructions = instructions
        self.description = description or f"{name} Agent"
        self.messages = []
        
    def add_message(self, role, content):
        """Add a message to the conversation history"""
        self.messages.append({"role": role, "content": content})
        
    def reset_messages(self):
        """Reset the conversation history"""
        self.messages = []
        
    def process_query(self, query, include_history=True):
        """Process a query and return a response using direct API call"""
        # Prepare messages for the API call
        messages = []
        messages.append({"role": "system", "content": self.instructions})
        
        if include_history:
            messages.extend(self.messages)
            
        messages.append({"role": "user", "content": query})
        
        # Make the direct API call
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            assistant_message = response.json()["choices"][0]["message"]["content"]
            
            # Add the new messages to the history
            self.add_message("user", query)
            self.add_message("assistant", assistant_message)
            
            return assistant_message
        else:
            error_message = f"Error: {response.status_code} - {response.text}"
            print(error_message)
            return error_message


class WebSearchTool:
    """A tool that can perform web searches"""
    
    def search(self, query):
        """Simulate a web search by using the OpenAI model to generate information"""
        # In a real implementation, this would call a search API
        # For now, we'll simulate it with the OpenAI API
        messages = [
            {"role": "system", "content": "You are a web search tool. Provide factual, up-to-date information about the query as if you were displaying search results. Format your response like real search results with bullet points for key information."},
            {"role": "user", "content": f"Search query: {query}"}
        ]
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }
        
        payload = {
            "model": "gpt-4o",
            "messages": messages,
            "temperature": 0.3
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


class AIDevTeam:
    """Main class that orchestrates the AI development team workflow"""
    
    def __init__(self):
        # Create specialized agents with specific instructions
        self.product_manager = SpecializedAgent(
            name="Product Manager",
            description="Handles requirements gathering and user stories",
            instructions="""
            You are an experienced product manager who helps define requirements and user stories.
            
            Your responsibilities:
            - Clarify user requirements through questions
            - Break down vague requests into specific functional requirements
            - Create clear user stories with acceptance criteria
            - Identify potential scope issues early
            - Help prioritize features for MVP vs future releases
            
            Always maintain a business-focused perspective while translating client needs into technical specifications.
            """
        )
        
        self.architect = SpecializedAgent(
            name="Software Architect",
            description="Designs system architecture",
            instructions="""
            You are an expert software architect who designs robust, scalable application architecture.
            
            Your responsibilities:
            - Design overall system architecture based on requirements
            - Select appropriate technologies and frameworks
            - Create high-level component diagrams
            - Identify potential technical challenges
            - Make architecture recommendations considering scalability, security, and performance
            
            Focus on creating clear, maintainable designs that balance business needs with technical implementation.
            """
        )
        
        self.frontend_dev = SpecializedAgent(
            name="Frontend Developer",
            description="Implements frontend code",
            instructions="""
            You are a skilled frontend developer specializing in modern web technologies.
            
            Your responsibilities:
            - Write clean, efficient frontend code (HTML, CSS, JavaScript/TypeScript)
            - Implement responsive, accessible UI components
            - Create engaging user interfaces with excellent UX
            - Work with modern frontend frameworks (React, Vue, Angular)
            
            Always prioritize user experience, accessibility, and performance in your implementations.
            """
        )
        
        self.backend_dev = SpecializedAgent(
            name="Backend Developer",
            description="Implements backend code",
            instructions="""
            You are an experienced backend developer who excels at creating robust APIs and services.
            
            Your responsibilities:
            - Design and implement APIs and server-side functionality
            - Create efficient database schemas and queries
            - Write secure, well-tested backend code
            - Implement proper error handling and logging
            
            Focus on performance, security, and maintainability in all your code.
            """
        )
        
        self.qa_tester = SpecializedAgent(
            name="QA Tester",
            description="Tests and ensures quality",
            instructions="""
            You are a thorough QA tester who finds and reports issues.
            
            Your responsibilities:
            - Create test plans and test cases
            - Review code for potential issues
            - Design user acceptance testing scenarios
            - Identify edge cases and potential bugs
            
            Be meticulous and comprehensive in your testing approach.
            """
        )
        
        self.tech_writer = SpecializedAgent(
            name="Technical Writer",
            description="Creates documentation",
            instructions="""
            You are a skilled technical writer who creates clear documentation.
            
            Your responsibilities:
            - Write user guides and README files
            - Document APIs
            - Create installation/setup instructions
            - Explain complex concepts in simple terms
            
            Make your documentation accessible to both technical and non-technical users.
            """
        )
        
        self.orchestrator = SpecializedAgent(
            name="Project Orchestrator",
            description="Coordinates the development process",
            instructions="""
            You are the central coordinator for the entire development process.
            
            Your responsibilities:
            - Understand user requirements and triage tasks to specialized agents
            - Manage the flow of information between agents and the user
            - Track project status and progress
            - Identify dependencies and blockers
            - Synthesize outputs from different agents into a cohesive product
            
            You must maintain the big picture while coordinating the details of implementation.
            
            When triaging a task, determine which specialized agent is most appropriate:
            - Product Manager: For requirements gathering and clarification
            - Software Architect: For system design and technology selection
            - Frontend Developer: For UI/UX implementation and frontend code
            - Backend Developer: For server-side implementation and APIs
            - QA Tester: For quality assurance and testing
            - Technical Writer: For documentation
            
            Reply with your assessment and the agent you're handing off to.
            """
        )
        
        # Create tools
        self.web_search = WebSearchTool()
        
        # Store all agents in a dictionary for easy access
        self.agents = {
            "orchestrator": self.orchestrator,
            "product_manager": self.product_manager,
            "architect": self.architect,
            "frontend_dev": self.frontend_dev,
            "backend_dev": self.backend_dev,
            "qa_tester": self.qa_tester,
            "tech_writer": self.tech_writer
        }
        
        # Track the current agent
        self.current_agent = "orchestrator"
        
        # Project context
        self.project_context = {
            "name": "",
            "requirements": [],
            "architecture": {},
            "components": [],
            "status": {}
        }
    
    def process_query(self, query):
        """Process a query through the current agent"""
        # Add project context to the query
        context_json = json.dumps(self.project_context, indent=2)
        enriched_query = f"""
        User Query: {query}
        
        Current Project Context:
        ```json
        {context_json}
        ```
        
        Please consider the project context in your response.
        """
        
        # Get the current agent
        agent = self.agents[self.current_agent]
        
        # Check if we need to handle tools
        if "search" in query.lower() and self.current_agent != "orchestrator":
            # Use the web search tool
            search_query = query.replace("search", "").strip()
            search_results = self.web_search.search(search_query)
            enriched_query += f"\n\nWeb Search Results for '{search_query}':\n{search_results}"
        
        # Process the query with the current agent
        response = agent.process_query(enriched_query)
        
        # Check for handoff intent in the response
        handoff_agent = self._check_for_handoff(response)
        if handoff_agent and handoff_agent != self.current_agent:
            old_agent = self.current_agent
            self.current_agent = handoff_agent
            handoff_message = f"\n\n[Handoff from {old_agent} to {handoff_agent}]\n\n"
            
            # Add handoff context to the next agent
            handoff_query = f"{handoff_message}Previous agent said: {response}\n\nOriginal user query: {query}"
            new_agent = self.agents[handoff_agent]
            response = new_agent.process_query(handoff_query)
            
            return f"{handoff_message}{response}"
        
        return response
    
    def _check_for_handoff(self, response):
        """Check if the response indicates a handoff to another agent"""
        # Keywords that might indicate handoffs
        handoff_keywords = {
            "product_manager": ["product manager", "requirements", "user stories", "clarify requirements"],
            "architect": ["architect", "architecture", "design", "system design", "technology selection"],
            "frontend_dev": ["frontend", "ui", "ux", "interface", "component", "react", "html", "css"],
            "backend_dev": ["backend", "server", "api", "database", "service"],
            "qa_tester": ["test", "qa", "quality assurance", "edge cases", "bugs"],
            "tech_writer": ["documentation", "docs", "readme", "guide", "manual"]
        }
        
        # Check for explicit handoff phrases
        if "hand off to" in response.lower() or "handoff to" in response.lower():
            for agent_id, keywords in handoff_keywords.items():
                for keyword in keywords:
                    if keyword in response.lower():
                        return agent_id
        
        # If no explicit handoff found, return None to keep the current agent
        return None
    
    def reset(self):
        """Reset the conversation history for all agents"""
        for agent in self.agents.values():
            agent.reset_messages()
        self.current_agent = "orchestrator"


def main():
    print("Welcome to the AI Development Team!")
    print("Type 'exit' to quit or 'reset' to start a new conversation.")
    
    dev_team = AIDevTeam()
    
    while True:
        user_input = input("\nWhat can I help you with? ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'reset':
            dev_team.reset()
            print("Conversation reset. Starting fresh!")
            continue
        
        try:
            # Show which agent is currently active
            current_agent_name = dev_team.agents[dev_team.current_agent].name
            print(f"\n[Current Agent: {current_agent_name}]")
            
            # Process the query
            response = dev_team.process_query(user_input)
            
            # Display the response
            print(f"\n{response}")
            
            # Show which agent is now active after any handoffs
            new_agent_name = dev_team.agents[dev_team.current_agent].name
            if new_agent_name != current_agent_name:
                print(f"\n[Now speaking with: {new_agent_name}]")
                
        except Exception as e:
            print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 