from typing import List, Optional, Union

from cicada.core import MultiModalModel

from .utils import load_image_data


class VisualDescriber:
    """A class that describes images using OpenAI's vision model.

    Attributes:
        model: The OpenAI client instance.
        system_prompt: The prompt that guides how images should be described.
        supported_schemes: Tuple of supported URI schemes.
    """

    def __init__(self, model: MultiModalModel, system_prompt: str):
        """Initializes the visual describer with an OpenAI client and system prompt.

        Args:
            model: An OpenAI client instance configured with API key.
            system_prompt: The prompt that guides the image description process.
        """
        self.model = model
        self.system_prompt = system_prompt

    def describe(
        self, uris: Union[str, List[str]], user_prompt: Optional[str] = None
    ) -> str:
        """Generates descriptions for one or more images using OpenAI's vision model.

        Args:
            uris: Either a single image URI (string) or list of URIs.
            user_prompt: Optional text prompt to guide the description.

        Returns:
            Generated description from the vision model.

        Raises:
            ValueError: If no image URIs are provided.
            TypeError: If uris is neither string nor list.
        """
        # Normalize input to always be a list
        if isinstance(uris, str):
            uris = [uris]
        elif not isinstance(uris, list):
            raise TypeError("uris must be either a string or list of strings")

        if not uris:
            raise ValueError("At least one image URI must be provided")

        messages = [{"role": "system", "content": self.system_prompt}]

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

        # Call model (assuming this matches your actual API interface)
        result = self.model.query(messages=messages)
        return result["content"]


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()

    model = MultiModalModel(
        api_key=os.getenv("API_KEY"),
        api_base_url=os.getenv("BASE_URL"),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
    )
    system_prompt = "You are professional biologist with specialty in image analysis. Please describe the image in detail."

    visual_describer = VisualDescriber(model=model, system_prompt=system_prompt)
    print(
        visual_describer.describe(
            [
                "https://epi-rsc.rsc-cdn.org/globalassets/05-journals-books-databases/our-journals/00-journal-pages-heros/Chemical-biology-HERO.jpg"
            ]
        )
    )
