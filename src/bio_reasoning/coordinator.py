from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Sequence

from cicada.core import MultiModalModel, PromptBuilder
from loguru import logger
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from .reasoning.example_reasoning import ExampleReasoningMode, ReasoningMode


@dataclass
class Configuration:
    api_key: str
    api_base_url: str
    model_name: str
    stream: bool = True

    def to_dict(self) -> Dict[str, Any]:
        dict_repr = asdict(self)
        return dict_repr

    def __str__(self) -> str:
        """
        This is a hack to make the Configuration object printable.
        """
        return str(self.to_dict())

    def __repr__(self) -> str:
        """
        This is a hack to make the Configuration object printable.
        """
        return self.__str__()

    # what's the method to override for **config unpacking?
    def __getitem__(self, key: str) -> Any:
        """
        This is a hack to make the Configuration object unpackable.
        For example, we can use **config to unpack the Configuration object.
        """
        return getattr(self, key)


class Coordinator:
    """
    This is the orchestrator of layers.
    """

    def __init__(
        self,
        *,
        config: Configuration,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        logger.debug(config)
        self._core = MultiModalModel(**config.to_dict())
        self._reasoning_mode: Optional[ReasoningMode] = None
        self.system_prompt = system_prompt

    # TODO: we may need a method called determine_reasoning_mode. It could be simply a llm query to score the query against definition of each reasoning mode, then select the one with the highest score. But we need a collection of reasoning modes to test and develop this method.

    @property
    def reasoning_mode(self) -> ReasoningMode:
        if self._reasoning_mode is None:
            raise ValueError("Reasoning mode is not set.")
        return self._reasoning_mode

    @reasoning_mode.setter
    def reasoning_mode(self, reasoning_mode: ReasoningMode) -> None:
        """
        Set the reasoning mode for the coordinator.
        This will update the system prompt and the tools available to the coordinator.
        """
        self._reasoning_mode = reasoning_mode

    def query(
        self,
        messages: Sequence[ChatCompletionMessage | dict[str, str]],
        stream: bool = False,
    ) -> str:
        # prepend system prompt to messages.
        # if a reasoning mode is set, use reasoning mode's system prompt if available.
        # otherwise, use the default system prompt as a fallback.
        messages = [
            {
                "role": "system",
                "content": self.reasoning_mode.sys_prompt
                if self.reasoning_mode
                else self.system_prompt,
            }
        ] + list(messages)

        response = self._core.query(
            messages=messages,
            tools=self.reasoning_mode.layers if self.reasoning_mode else None,
            stream=stream,
        )
        return response["content"]


if __name__ == "__main__":
    import os

    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env file

    config = Configuration(
        api_key=os.getenv("API_KEY", "sk-xxxxxxxxx"),
        api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
    )
    coordinator = Coordinator(
        config=config,
        system_prompt=(
            "You are a coordinator of a team of experts and tools. "
            " You are provided with a collections of tools. Tools are labeled with a prefix from layer_a, layer_b, or layer_c. "
            "Layer A is the parametric memory of a general large language model (LLM), capturing broadly applicable knowledge pre-trained or fine-tuned into its weights. Layer B consists of bespoke foundation models specialized for non-textual or multimodal data (e.g. genomic sequences, protein structures, images) that interface with the LLM. Layer C encompasses external knowledge sources - APIs, databases, and knowledge graphs - to provide access to large, dynamic, or regulated datasets that cannot reside fully within models. "
            # "You may be provided with URLs to images, use the tools to analyze them. "
            "You are given a question and you need to answer it by commanding the tools available to you."
        ),
    )

    # set example
    coordinator.reasoning_mode = ExampleReasoningMode()

    pb = PromptBuilder()
    pb.add_user_message("what tools do you have access to?")
    pb.add_user_message(
        "What is this image about? https://epi-rsc.rsc-cdn.org/globalassets/05-journals-books-databases/our-journals/00-journal-pages-heros/Chemical-biology-HERO.jpg"
    )
    pb.add_user_message(
        "if any tool fails, report back to me with the error message and the tool name."
    )
    coordinator.query(pb.messages, stream=True)
