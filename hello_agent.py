import os
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

def simple_agent(instructions, user_input):
    """A simple agent function that uses OpenAI's API directly"""
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": user_input}
    ]
    
    response = client.chat.completions.create(
        model="gpt-4o",  # or any model you prefer
        messages=messages,
        temperature=0.7,
    )
    
    return response.choices[0].message.content

def main():
    # Define agent instructions
    instructions = "You are a helpful assistant for the construction industry. You provide concise, practical advice."
    
    # Get user input
    print("Welcome to the Construction Assistant!")
    print("Type 'exit' to quit.")
    
    while True:
        user_input = input("\nWhat can I help you with? ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
            
        # Get response from the agent
        response = simple_agent(instructions, user_input)
        
        # Display the response
        print("\nAssistant:")
        print(response)

if __name__ == "__main__":
    main() 