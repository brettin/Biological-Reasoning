import os
import sys
import traceback
from openai import OpenAI
from load_model_configs import load_model_configs

def initialize_client(model_shortname='gpt41', is_reflection=False):
    """
    Initialize the OpenAI client based on the selected model configuration.
    
    Args:
        model_shortname: Shortname of the model to use
        is_reflection: Whether this client is for the reflection agent
        
    Returns:
        Tuple of (client, model_id, config)
    """
    # Load model configurations
    models = load_model_configs()
    
    if not models:
        print("Error: No model configurations found. Check model_servers.yaml file.")
        sys.exit(1)
    
    # Validate model selection
    if model_shortname not in models:
        print(f"Error: Model '{model_shortname}' not found in configuration.")
        print(f"Available models: {', '.join(models.keys())}")
        sys.exit(1)
    
    config = models[model_shortname]
    client_type = "Reflection" if is_reflection else "Main"
    print(f"Using {client_type} model: {model_shortname} ({config['openai_model']})")
    
    # Handle API key - either from env var or literal
    api_key = config['openai_api_key']
    if api_key.startswith("${") and api_key.endswith("}"):
        # Extract environment variable name
        env_var = api_key[2:-1]
        api_key = os.getenv(env_var)
        if not api_key:
            print(f"Error: Environment variable {env_var} not set")
            sys.exit(1)
    
    # Create OpenAI client
    try:
        return OpenAI(
            api_key=api_key,
            base_url=config['openai_api_base']
        ), config['openai_model'], config
    except Exception as e:
        print(f"Error initializing OpenAI client: {e}")
        traceback.print_exc()
        sys.exit(1)

