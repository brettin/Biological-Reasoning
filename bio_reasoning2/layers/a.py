"""
Layer A is the parametric memory of a general large language model (LLM), capturing broadly applicable knowledge pre-trained or fine-tuned into its weights."""

import openai


class ParametricMemory:
    """A knowledge distillation process around a LLM that stores and retrieves information.

    Attributes:
        model: The language model used for knowledge distillation.
        system_prompt: The prompt used to guide the knowledge distillation process.
    """

    # TODO: set up async support, but current version is okay as well, as toolregistry handles parallel execution of tools
    def __init__(self, *, model: openai.OpenAI, system_prompt: str):
        """Initializes the parametric memory with a model and system prompt.

        Args:
            model: A language model instance capable of text generation.
            system_prompt: The knowledge distillation prompt that guides how information
                should be processed and stored.
        """
        self.model = model
        self.system_prompt = system_prompt

    def answer(self, *, user_prompt: str) -> str:
        """Generates a distilled response based on the user's prompt.

        Args:
            user_prompt: The user's question or topic to be processed.

        Returns:
            The model's distilled response to the user prompt.
        """
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        resp = self.model.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )
        return resp.choices[0].message.content


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    model = openai.OpenAI(
        api_key=os.getenv("API_KEY"),
        base_url=os.getenv("BASE_URL"),
    )

    parametric_memory_gpt_4_1 = ParametricMemory(
        model=model,
        system_prompt="You are an expert in biology. You are given a question and you need to answer it with the best of your knowledge.",
    )
    print(
        parametric_memory_gpt_4_1.answer(
            user_prompt="What is the function of mitochondria?"
        )
    )
