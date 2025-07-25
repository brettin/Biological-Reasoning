import sys
from initialize_client import initialize_client
from load_model_configs import load_model_configs
from call_agent import call_agent
from generation_agent import get_generation_agent_prompt
from parse_ideas_from_text import parse_ideas_from_text

# Initialize clients
main_client, MAIN_MODEL_ID, main_config = initialize_client('gpt41', is_reflection=False)
reflection_client, REFLECTION_MODEL_ID, reflection_config = initialize_client('gpto1', is_reflection=True)

# Set the clients in the call_agent module
from call_agent import set_clients
set_clients(main_client, reflection_client, MAIN_MODEL_ID, REFLECTION_MODEL_ID)

# Call an agent
response = call_agent(
    agent_system_prompt=get_generation_agent_prompt(),
    user_prompt="Generate 4 ideas about EFGR tyrosine kinase inhibitor resistance",
    agent_name="generation"
)

print(response)

print("\n" + "="*50)
print("TESTING PARSE IDEAS FUNCTION")
print("="*50)

# Parse the generated ideas
generation_output = response
initial_ideas = parse_ideas_from_text(generation_output, expected_count=5)

print(f"Parsed {len(initial_ideas)} ideas:")
for i, idea in enumerate(initial_ideas, 1):
    print(f"\n--- Idea {i} ---")
    print(idea)