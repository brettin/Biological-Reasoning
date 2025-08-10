"""General agent module.

This module provides a simple abstraction for LLM interactions.
It wraps cicada.core.MultiModalModel with basic initialization and query functionality.
Tools are handled by the underlying MultiModalModel.
"""

import os

from .agent import GeneralAgent
from .config import AgentConfig

__all__ = ["GeneralAgent", "AgentConfig", "create_agent", "create_agent_from_env"]


def create_agent(
    api_key: str,
    api_base_url: str,
    model_name: str,
    system_prompt: str = "You are a helpful assistant.",
    **kwargs,
) -> GeneralAgent:
    """Create a general agent with the specified configuration.

    Args:
        api_key: API key for the LLM service
        api_base_url: Base URL for the LLM API endpoint
        model_name: Name of the model to use
        system_prompt: System prompt for the agent
        **kwargs: Additional configuration parameters

    Returns:
        Configured GeneralAgent instance
    """
    config = AgentConfig(
        api_key=api_key, api_base_url=api_base_url, model_name=model_name, **kwargs
    )

    return GeneralAgent(config=config, system_prompt=system_prompt)


def create_agent_from_env(
    system_prompt: str = "You are a helpful assistant.",
    api_key_env: str = "API_KEY",
    base_url_env: str = "BASE_URL",
    model_name_env: str = "MODEL_NAME",
    **kwargs,
) -> GeneralAgent:
    """Create a general agent from environment variables.

    Args:
        system_prompt: System prompt for the agent
        api_key_env: Environment variable name for API key
        base_url_env: Environment variable name for base URL
        model_name_env: Environment variable name for model name
        **kwargs: Additional configuration parameters

    Returns:
        Configured GeneralAgent instance

    Raises:
        ValueError: If required environment variables are not set
    """
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"Environment variable {api_key_env} is not set")

    api_base_url = os.getenv(base_url_env)
    if not api_base_url:
        raise ValueError(f"Environment variable {base_url_env} is not set")

    model_name = os.getenv(model_name_env)
    if not model_name:
        raise ValueError(f"Environment variable {model_name_env} is not set")

    return create_agent(
        api_key=api_key,
        api_base_url=api_base_url,
        model_name=model_name,
        system_prompt=system_prompt,
        **kwargs,
    )
