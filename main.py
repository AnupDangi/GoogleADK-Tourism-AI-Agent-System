"""
Tourism AI Agent System - Main Entry Point
"""
import os
from dotenv import load_dotenv
from agents.parent_agent import TourismAIAgent

# Load environment variables from .env file
load_dotenv()

def main():
    """Main function to run the tourism AI agent system"""
    # Initialize the Tourism AI Agent
    agent = TourismAIAgent()
    
    print("=" * 60)
    print("Tourism AI Agent System")
    print("=" * 60)
    print("Enter a place you want to visit and ask about weather or places.")
    print("Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! Have a great trip!")
                break
            
            if not user_input:
                continue
            
            # Get response from the agent
            response = agent.process_query(user_input)
            print(f"\nAgent: {response}\n")
            print("-" * 60)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! Have a great trip!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")

if __name__ == "__main__":
    main()


