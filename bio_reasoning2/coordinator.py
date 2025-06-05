from dataclasses import asdict, dataclass
from pprint import pprint
from typing import Any, Dict, List

from cicada.core import MultiModalModel, PromptBuilder
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from .reasoning_modes import ExampleReasoningMode, ReasoningMode


@dataclass
class Configuration:
    api_key: str
    api_base_url: str
    model_name: str
    stream: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


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
        self._core = MultiModalModel(**config.to_dict())
        self._reasoning_mode: ReasoningMode = None
        self.system_prompt = system_prompt

    def set_reasoning_mode(self, reasoning_mode: ReasoningMode) -> None:
        self._reasoning_mode = reasoning_mode

    def query(self, messages: List[ChatCompletionMessage], stream: bool = False) -> str:
        # prepend system prompt
        messages = [{"role": "system", "content": self.system_prompt}] + messages

        response = self._core.query(
            messages=messages,
            tools=self._reasoning_mode.layers if self._reasoning_mode else None,
            stream=stream,
        )
        return response["content"]


if __name__ == "__main__":
    import os

    import dotenv

    dotenv.load_dotenv()  # Load environment variables from .env file

    config = Configuration(
        api_key=os.getenv("API_KEY"),
        api_base_url=os.getenv("BASE_URL"),
        model_name=os.getenv("MODEL_NAME"),
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
    coordinator.set_reasoning_mode(ExampleReasoningMode())

    pb = PromptBuilder()
    pb.add_user_message("what tools do you have access to?")
    pb.add_user_message(
        "What is this image about? https://epi-rsc.rsc-cdn.org/globalassets/05-journals-books-databases/our-journals/00-journal-pages-heros/Chemical-biology-HERO.jpg"
    )
    pb.add_user_message(
        "if any tool fails, report back to me with the error message and the tool name."
    )
    coordinator.query(pb.messages, stream=True)
