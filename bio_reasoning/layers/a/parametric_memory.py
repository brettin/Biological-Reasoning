from typing import Callable
from ...utils import query_chat_completion


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