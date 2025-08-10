"""General agent implementation using cicada.core.MultiModalModel."""

from typing import Any, Dict, List, Optional, Sequence, Union

from cicada.core import MultiModalModel
from loguru import logger
from openai.types.chat.chat_completion_message import ChatCompletionMessage

from .config import AgentConfig


class GeneralAgent:
    """A general agent that wraps cicada.core.MultiModalModel.
    
    This agent provides a simple abstraction over the raw MultiModalModel,
    with just initialization and query functionality. Tools are handled
    by the underlying MultiModalModel.
    """

    def __init__(
        self,
        config: AgentConfig,
        system_prompt: str = "You are a helpful assistant.",
    ) -> None:
        """Initialize the general agent.
        
        Args:
            config: Agent configuration containing API settings
            system_prompt: Default system prompt for the agent
        """
        # Validate configuration
        config.validate()
        
        self.config = config
        self.system_prompt = system_prompt
        
        # Initialize the core MultiModalModel
        self._core = MultiModalModel(**config.to_dict())
        
        logger.info(f"Initialized GeneralAgent with model: {config.model_name}")

    def query(
        self,
        messages: Sequence[Union[ChatCompletionMessage, Dict[str, str]]],
        stream: Optional[bool] = None,
        system_prompt_override: Optional[str] = None,
        **kwargs
    ) -> str:
        """Query the agent with a sequence of messages.
        
        Args:
            messages: Sequence of chat messages
            stream: Whether to stream the response (overrides config default)
            system_prompt_override: Override the default system prompt
            **kwargs: Additional parameters to pass to the underlying model
            
        Returns:
            The agent's response content
        """
        # Prepare system message
        system_content = system_prompt_override or self.system_prompt
        prepared_messages = [
            {"role": "system", "content": system_content}
        ] + list(messages)
        
        # Log the conversation
        for i, message in enumerate(prepared_messages):
            logger.debug(f"Message {i}: {message}")
        
        # Determine streaming setting
        use_stream = stream if stream is not None else self.config.stream
        
        try:
            # Query the underlying model
            response = self._core.query(
                messages=prepared_messages,
                stream=use_stream,
                **kwargs
            )
            
            # Extract content from response
            content = self._extract_content(response)
            
            return content
            
        except Exception as e:
            logger.error(f"Error during agent query: {e}")
            raise

    def _extract_content(self, response: Any) -> str:
        """Extract content from the model response.
        
        Args:
            response: Raw response from the underlying model
            
        Returns:
            Extracted content string
        """
        if isinstance(response, dict):
            return response.get("content", str(response))
        elif hasattr(response, "content"):
            return response.content
        else:
            return str(response)

    def __repr__(self) -> str:
        """String representation of the agent."""
        return f"GeneralAgent(model='{self.config.model_name}')"