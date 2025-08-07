from typing import Callable
import logging
from ...utils import query_chat_completion

# Set up logging
parametric_memory_logger = logging.getLogger(__name__)


def parametric_memory_factory(
    api_key: str,
    api_base_url: str,
    model_name: str,
    system_prompt: str,
) -> Callable[[str], str]:
    """
    Factory function to create a parametric memory function with the provided configuration.

    Args:
        api_key (str): The API key for authentication.
        api_base_url (str): The base URL of the API providing completion services.
        model_name (str): The name of the model to use for generating responses.
        system_prompt (str): A prompt to set the system context.

    Returns:
        Callable[[str], str]: A function that takes a user prompt and returns a model's response.
    """
    parametric_memory_logger.info("🏭 Creating parametric memory factory")
    parametric_memory_logger.info(f"🔧 Configuration: {model_name} at {api_base_url}")
    parametric_memory_logger.info(f"📝 System prompt: {system_prompt}")

    def parametric_memory(user_prompt: str) -> str:
        """
        Generates a distilled response based on the user's prompt.

        Args:
            user_prompt (str): The user's question or topic to be processed.

        Returns:
            str: The model's distilled response to the user prompt.
        """
        parametric_memory_logger.info("🧠 Parametric memory called")
        parametric_memory_logger.info(f"📤 User prompt: {user_prompt}")
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        parametric_memory_logger.info("📤 Sending messages to model:")
        for i, msg in enumerate(messages):
            parametric_memory_logger.info(f"  Message {i+1} ({msg['role']}): {msg['content'][:200]}{'...' if len(msg['content']) > 200 else ''}")

        # Delegate API call to the helper function
        parametric_memory_logger.info("🌐 Making API call to parametric memory...")
        response = query_chat_completion(api_base_url, api_key, model_name, messages)
        
        parametric_memory_logger.info("📥 Received response from parametric memory:")
        parametric_memory_logger.info(f"  Response length: {len(response)} characters")
        parametric_memory_logger.info(f"  Response preview: {response[:500]}{'...' if len(response) > 500 else ''}")
        
        return response

    return parametric_memory


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    system_prompt = (
        "You are an expert in biology. You are given a question and you need to answer "
        "it with the best of your knowledge."
    )

    parametric_memory = parametric_memory_factory(
        api_key=os.getenv("API_KEY"),
        api_base_url=os.getenv("BASE_URL"),
        model_name=os.getenv("MODEL_NAME"),
        system_prompt=system_prompt,
    )

    print(parametric_memory("What is the function of mitochondria?"))