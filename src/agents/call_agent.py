import time
from openai import APITimeoutError, APIConnectionError, RateLimitError, APIError

# Global variables for clients and models (will be set by initialize_clients)
main_client = None
reflection_client = None
MAIN_MODEL_ID = None
REFLECTION_MODEL_ID = None
DEBUG_MODE = True
MAX_RETRIES_TIMEOUT = 3

def set_clients(main_cl, reflection_cl, main_model, reflection_model):
    """Set the global client instances and model IDs"""
    global main_client, reflection_client, MAIN_MODEL_ID, REFLECTION_MODEL_ID
    main_client = main_cl
    reflection_client = reflection_cl
    MAIN_MODEL_ID = main_model
    REFLECTION_MODEL_ID = reflection_model

def call_agent(
    agent_system_prompt: str,
    user_prompt: str,
    agent_name: str,
    additional_context: str = "",
    max_retries: int = 3,
    retry_delay: float = 2.0
) -> str:
    '''
    Given an agent-specific system prompt, a user-level prompt, and optional
    additional context (e.g., lists of ideas, feedback from other agents), call
    the OpenAI API to get the agent's response.
    
    Includes retry logic with exponential backoff for handling temporary errors.
    
    Args:
        agent_system_prompt: System prompt defining the agent's role and behavior
        user_prompt: The main user query or instruction
        additional_context: Optional context to include in the conversation
        max_retries: Maximum number of retry attempts on failure
        retry_delay: Initial delay between retries (increases exponentially)
        
    Returns:
        The agent's response text
    '''
    # Select appropriate client and model based on agent type
    if agent_name.lower() == "reflection":
        client_instance = reflection_client
        model_id = REFLECTION_MODEL_ID
    else:
        client_instance = main_client
        model_id = MAIN_MODEL_ID

    messages = [
        {"role": "system", "content": agent_system_prompt},
    ]

    if additional_context:
        messages.append({"role": "assistant", "content": additional_context})

    messages.append({"role": "user", "content": user_prompt})

    # Create a display name from the agent name for output
    agent_display_name = agent_name.title()
    model_display = f" [{model_id}]" if DEBUG_MODE else ""

    # Retry logic with exponential backoff
    for attempt in range(max_retries):
        try:
            print(f"Calling {agent_display_name} Agent{model_display}... ", end="", flush=True)
            # For O3 and O4mini models, don't use temperature parameter
            if "o3" in model_id.lower() or "o4" in model_id.lower():
                response = client_instance.chat.completions.create(
                    model=model_id,
                    messages=messages
                )
            else:
                response = client_instance.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    temperature=0.7
                )
            print("✓")
            return response.choices[0].message.content
            
        except APITimeoutError as e:
            if attempt < MAX_RETRIES_TIMEOUT - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Timeout error occurred. Retrying ({attempt+1}/{MAX_RETRIES_TIMEOUT}) in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
                print(f"Resuming {agent_display_name} Agent request with longer timeout...")
                pass
            else:
                print(f"Failed after {MAX_RETRIES_TIMEOUT} timeout retries: {e}")
                raise
                
        except APIConnectionError as e:
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"Connection error. Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
                
        except RateLimitError as e:
            wait_time = retry_delay * (2 ** attempt) + 1  # Add extra time for rate limits
            print(f"Rate limit exceeded. Waiting {wait_time:.1f} seconds before retry...")
            time.sleep(wait_time)
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
                
        except APIError as e:
            # Don't retry on 4xx errors, only retry on 5xx errors
            if e.status_code and 400 <= e.status_code < 500:
                print(f"Client error {e.status_code}: {e}")
                raise
            
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)
                print(f"API error {e.status_code}. Retrying in {wait_time:.1f} seconds...")
                time.sleep(wait_time)
            else:
                print(f"Failed after {max_retries} attempts: {e}")
                raise
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            print(f"Error type: {type(e).__name__}")
            raise
            
        finally:
            pass

