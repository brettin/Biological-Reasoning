from typing import Callable, List, Union

from toolregistry import Tool

from .utils import load_image_data
from ...utils import query_chat_completion

def _get_visual_description(
    uris: Union[str, List[str]],
    api_base_url: str,
    api_key: str,
    model_name: str,
    system_prompt: str = None,
    user_prompt: str = None,
) -> str:
    """
    Generates a visual description for one or more images using an external API.

    Args:
        uris (Union[str, List[str]]): The URI or list of URIs pointing to the image(s) to describe.
        api_base_url (str): The base URL of the API providing the visual description service.
        api_key (str): The API key used for authentication with the API.
        model_name (str): The name of the model to use for generating the description.
        system_prompt (str, optional): A prompt to establish the system context for the conversation. Defaults to None.
        user_prompt (str, optional): Additional user input or instructions to customize the visual description. Defaults to None.

    Returns:
        str: The visual description extracted from the API response.

    Raises:
        TypeError: If `uris` is not a string or a list of strings.
        ValueError: If no image URIs are provided.
    """
    if isinstance(uris, str):
        uris = [uris]
    elif not isinstance(uris, list):
        raise TypeError("uris must be either a string or list of strings")

    if not uris:
        raise ValueError("At least one image URI must be provided")

    messages = [{"role": "system", "content": system_prompt}]

    if user_prompt:
        messages.append({"role": "user", "content": user_prompt})

    # Load and attach images
    image_contents = []
    for uri in uris:
        image_contents.append(
            {
                "type": "image_url",
                "image_url": load_image_data(uri),
            }
        )

    # Combine all image contents into single user message
    messages.append({"role": "user", "content": image_contents})

    # Delegate API call to helper function
    return query_chat_completion(api_base_url, api_key, model_name, messages)


def visual_describer_factory(
    api_key: str,
    api_base_url: str,
    model_name: str = "gpt-4.1-mini",
    system_prompt: str = None,
) -> Callable[[Union[str, List[str]], str], str]:
    """
    Factory function to create a visual description function with provided configuration.

    Args:
        api_key (str): The API key for authentication.
        api_base_url (str): The base URL of the API providing the visual description service.
        model_name (str, optional): Name of the model. Defaults to 'gpt-4.1-mini'.
        system_prompt (str, optional): A prompt to set the system context. Defaults to None.

    Returns:
        Callable[[Union[str, List[str]], str], str]: A function that accepts image URIs and user prompt to generate a visual description.
    """

    def visual_describer(uris: Union[str, List[str]], user_prompt: str = "") -> str:
        """
        Generates a visual description for one or more images using an external API.

        Args:
            uris (Union[str, List[str]]): The URI or list of URIs pointing to the image(s) to describe.
            user_prompt (str): Additional user input or instructions to customize the visual description. Defaults to "".

        Returns:
            dict: A dictionary containing the visual description as part of the API response.

        Raises:
            TypeError: If `uris` is not a string or a list of strings.
            ValueError: If no image URIs are provided.
            RuntimeError: If the API request fails with an HTTP error.
        """
        return _get_visual_description(
            uris=uris,
            user_prompt=user_prompt,
            api_key=api_key,
            api_base_url=api_base_url,
            model_name=model_name,
            system_prompt=system_prompt,
        )

    # Copy the docstring from the original function
    visual_describer.__doc__ = _get_visual_description.__doc__

    return visual_describer


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    system_prompt = "You are professional biologist with specialty in image analysis. Please describe the image in detail."

    visual_describer = visual_describer_factory(
        api_key=os.getenv("API_KEY"),
        api_base_url=os.getenv("BASE_URL"),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
        system_prompt=system_prompt,
    )

    # test if it works with toolregistry
    visual_describer = Tool.from_function(
        visual_describer,
        name="visual_describer",
    )

    print(visual_describer.get_json_schema())

    # test if it works
    print(
        visual_describer.callable(
            uris="https://epi-rsc.rsc-cdn.org/globalassets/05-journals-books-databases/our-journals/00-journal-pages-heros/Chemical-biology-HERO.jpg"
        )
    )
