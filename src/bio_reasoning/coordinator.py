from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Sequence

from cicada.core import MultiModalModel, PromptBuilder
from loguru import logger
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from .reasoning.example_reasoning import ExampleReasoningMode, ReasoningMode
from .reasoning.prompts import create_reasoning_mode_from_prompt, REASONING_PROMPTS

import json


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
        self._reasoning_modes: List[ReasoningMode] = []
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
        self._reasoning_modes = [reasoning_mode] if reasoning_mode else []

    def construct_system_prompt(self, messages=None, user_question_override=None) -> str:
        """Construct system prompt combining default and reasoning mode prompts, filling in [USER_QUESTION]."""
        combined_prompt = self.system_prompt + "\n\n"
        
        # Extract user question from messages or use override
        user_question = ""
        if user_question_override:
            user_question = user_question_override
        elif messages:
            # Find the first user message
            for m in messages:
                if m.get("role") == "user":
                    user_question = m.get("content", "")
                    break
        
        # Add comprehensive introduction about reasoning composition
        if self._reasoning_modes:
            reasoning_names = [mode.name for mode in self._reasoning_modes]
            combined_prompt += f"You are a composition of many forms of reasoning. These include {', '.join(reasoning_names)}.\n\n"
            
            # Add each reasoning mode with its full description
            combined_prompt += "Each reasoning form provides specialized expertise:\n\n"
            for mode in self._reasoning_modes:
                # Extract the reasoning type from the mode name (e.g., "Spatial Reasoning Expert" -> "spatial")
                reasoning_type = mode.name.lower().replace(" reasoning expert", "")
                
                # Fill in [USER_QUESTION] in the sys_prompt
                sys_prompt_filled = mode.sys_prompt.replace("[USER_QUESTION]", user_question)
                
                combined_prompt += f'"{reasoning_type}": """{sys_prompt_filled}"""\n\n'
        
        return combined_prompt

    def query(
        self,
        messages: Sequence[ChatCompletionMessage | dict[str, str]],
        stream: bool = False,
        user_question_override: str = None,
    ) -> str:
        # prepend system prompt to messages.
        system_content = self.construct_system_prompt(messages, user_question_override)
        messages = [
            {
                "role": "system",
                "content": system_content,
            }
        ] + list(messages)
        for i, message in enumerate(messages):
            logger.debug(f"Message {i}: {message}")
        response = self._core.query(
            messages=messages,
            tools=self._get_combined_tools(),
            stream=stream,
        )
        return response["content"]

    def _get_combined_tools(self):
        """Get combined tools from all reasoning modes."""
        if not self._reasoning_modes:
            return None
        
        # For now, use the first reasoning mode's tools (backward compatibility)
        # TODO: Implement proper tool merging from multiple reasoning modes
        return self._reasoning_modes[0].layers if self._reasoning_modes else None

    def add_reasoning_mode(self, reasoning_mode: ReasoningMode) -> None:
        """Add a reasoning mode to the active set."""
        self._reasoning_modes.append(reasoning_mode)
        # Update single reasoning mode for backward compatibility
        if not self._reasoning_mode:
            self._reasoning_mode = reasoning_mode

    def set_reasoning_modes(self, reasoning_modes: List[ReasoningMode]) -> None:
        """Set the complete set of reasoning modes."""
        self._reasoning_modes = reasoning_modes
        # Update single reasoning mode for backward compatibility
        self._reasoning_mode = reasoning_modes[0] if reasoning_modes else None


if __name__ == "__main__":
    import os
    import sys

    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env file

    config = Configuration(
        api_key=os.getenv("API_KEY", "sk-xxxxxxxxx"),
        api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
        model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
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

    # Check for command line arguments for reasoning modes
    user_question_override = None
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reasoning-modes":
            # Parse reasoning modes from command line
            if len(sys.argv) > 2:
                mode_names_raw = sys.argv[2]
                logger.debug(f"Raw mode names argument: '{mode_names_raw}'")
                mode_names = [name.strip() for name in mode_names_raw.split(",")]
                logger.info(f"Using reasoning modes: {mode_names}")
                # Create reasoning modes from prompts.py
                reasoning_modes = []
                for mode_name in mode_names:
                    try:
                        mode = create_reasoning_mode_from_prompt(mode_name)
                        reasoning_modes.append(mode)
                    except ValueError as e:
                        logger.warning(f"Skipping unknown reasoning mode '{mode_name}': {e}")
                coordinator.set_reasoning_modes(reasoning_modes)
            else:
                # Default to all reasoning modes from prompts.py
                logger.info("Using all available reasoning modes from prompts.py")
                reasoning_modes = []
                for mode_name in REASONING_PROMPTS.keys():
                    mode = create_reasoning_mode_from_prompt(mode_name)
                    reasoning_modes.append(mode)
                coordinator.set_reasoning_modes(reasoning_modes)
        elif sys.argv[1] == "--user-question":
            # Parse user question from command line
            if len(sys.argv) > 2:
                user_question_override = sys.argv[2]
                logger.info(f"Using user question override: '{user_question_override}'")
            else:
                logger.warning("--user-question specified but no question provided")
    else:
        # Default behavior - use all reasoning modes from prompts.py
        logger.info("Using all available reasoning modes from prompts.py")
        reasoning_modes = []
        for mode_name in REASONING_PROMPTS.keys():
            mode = create_reasoning_mode_from_prompt(mode_name)
            reasoning_modes.append(mode)
        coordinator.set_reasoning_modes(reasoning_modes)

    pb = PromptBuilder()
    pb.add_user_message("what tools do you have access to?")
    pb.add_user_message(
        "What is this image about? https://epi-rsc.rsc-cdn.org/globalassets/05-journals-books-databases/our-journals/00-journal-pages-heros/Chemical-biology-HERO.jpg"
    )
    pb.add_user_message(
        "if any tool fails, report back to me with the error message and the tool name."
    )
    for message in pb.messages:
        logger.debug(json.dumps(message, indent=4))
    
    # Show the constructed system prompt without making the API call
    system_prompt = coordinator.construct_system_prompt(pb.messages, user_question_override)
    logger.info("=== CONSTRUCTED SYSTEM PROMPT ===")
    logger.info(system_prompt)
    logger.info("=== END SYSTEM PROMPT ===")
    
    #coordinator.query(pb.messages, stream=True)
