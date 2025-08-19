from typing import Callable, Optional
from ...utils import query_chat_completion
from ...config import ConfigManager
from loguru import logger


def create_parametric_memory(
    system_prompt: str,
    endpoint_name: str = "primary"
) -> Callable[[str], str]:
    """
    Create a parametric memory function using centralized configuration.
    
    Args:
        system_prompt (str): A prompt to set the system context.
        endpoint_name (str): Which LLM endpoint to use (primary, registry, etc.). Defaults to "primary".
        
    Returns:
        Callable[[str], str]: A function that takes a user prompt and returns a model's response.
        
    Raises:
        ValueError: If the specified endpoint is not configured.
    """
    try:
        config = ConfigManager.get_config()
        
        if not config.has_endpoint(endpoint_name):
            available_endpoints = config.list_endpoints()
            raise ValueError(f"Endpoint '{endpoint_name}' not configured. Available: {available_endpoints}")
        
        llm_config = config.get_endpoint(endpoint_name).to_agent_config()
        logger.info(f"Created parametric memory using {endpoint_name} LLM endpoint")
        
        return parametric_memory_factory(
            api_key=llm_config.api_key,
            api_base_url=llm_config.api_base_url,
            model_name=llm_config.model_name,
            system_prompt=system_prompt
        )
        
    except Exception as e:
        logger.error(f"Failed to create parametric memory with centralized config: {e}")
        raise


def parametric_memory_factory(
    api_key: str,
    api_base_url: str,
    model_name: str,
    system_prompt: str,
) -> Callable[[str], str]:
    """
    Factory function to create a parametric memory function with the provided configuration.
    
    Note: For new code, prefer using create_parametric_memory() which uses centralized configuration.

    Args:
        api_key (str): The API key for authentication.
        api_base_url (str): The base URL of the API providing completion services.
        model_name (str): The name of the model to use for generating responses.
        system_prompt (str): A prompt to set the system context.

    Returns:
        Callable[[str], str]: A function that takes a user prompt and returns a model's response.
    """

    def parametric_memory(user_prompt: str) -> str:
        """
        Generates a distilled response based on the user's prompt.

        Args:
            user_prompt (str): The user's question or topic to be processed.

        Returns:
            str: The model's distilled response to the user prompt.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        # Delegate API call to the helper function
        response = query_chat_completion(api_base_url, api_key, model_name, messages)
        return response

    return parametric_memory


if __name__ == "__main__":
    # Demo the parametric memory functionality
    system_prompt = (
        "You are an expert in biology. You are given a question and you need to answer "
        "it with the best of your knowledge."
    )

    print("🧠 Parametric Memory Demo")
    print("=" * 40)
    
    try:
        # Test the new centralized configuration approach
        print("Testing centralized configuration approach...")
        config = ConfigManager.get_config()
        print(f"Available endpoints: {config.list_endpoints()}")
        
        # Create parametric memory using primary LLM
        memory_func = create_parametric_memory(system_prompt, "primary")
        print("✅ Parametric memory created successfully with centralized config")
        
        # Test query (would fail without actual LLM server)
        test_query = "What is the function of mitochondria?"
        print(f"Test query: {test_query}")
        
        try:
            response = memory_func(test_query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Query failed (expected without LLM server): {e}")
        
    except Exception as e:
        print(f"❌ Centralized config test failed: {e}")
        
        # Fallback to old approach
        print("\nFalling back to environment variable approach...")
        import os
        from dotenv import load_dotenv

        load_dotenv()
        
        api_key = os.getenv("API_KEY", "sk-test")
        api_base_url = os.getenv("BASE_URL", "https://api.openai.com/v1")
        model_name = os.getenv("MODEL_NAME", "gpt-4")
        
        if api_key != "sk-test":
            parametric_memory = parametric_memory_factory(
                api_key=api_key,
                api_base_url=api_base_url,
                model_name=model_name,
                system_prompt=system_prompt,
            )
            print("✅ Parametric memory created with environment variables")
        else:
            print("⚠️ No API key configured in environment variables")
    
    print("\n✅ Parametric memory demo complete!")