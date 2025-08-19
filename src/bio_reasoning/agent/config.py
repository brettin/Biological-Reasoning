"""Configuration classes for the bio-reasoning agent module."""

import os
from dataclasses import asdict, dataclass, replace
from typing import Any, Dict, Optional
from dotenv import load_dotenv


@dataclass
class AgentConfig:
    """Configuration for the bio-reasoning agent.
    
    This class encapsulates all the configuration needed to initialize
    and run a bio-reasoning agent, including API credentials, model settings,
    and behavior parameters.
    
    Attributes:
        api_key: API key for the LLM service
        api_base_url: Base URL for the LLM API endpoint
        model_name: Name of the model to use
        stream: Whether to use streaming responses
        temperature: Sampling temperature for response generation
        max_tokens: Maximum number of tokens in response
        timeout: Request timeout in seconds
    """
    
    api_key: str
    api_base_url: str
    model_name: str
    stream: bool = True
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 30

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary format.
        
        Returns:
            Dictionary representation of the configuration.
        """
        return asdict(self)

    def __str__(self) -> str:
        """String representation of the configuration.
        
        Returns:
            String representation hiding sensitive information.
        """
        safe_dict = self.to_dict()
        # Hide sensitive information
        if 'api_key' in safe_dict:
            safe_dict['api_key'] = f"{safe_dict['api_key'][:8]}..." if len(safe_dict['api_key']) > 8 else "***"
        return str(safe_dict)

    def __repr__(self) -> str:
        """Representation of the configuration."""
        return self.__str__()

    def __getitem__(self, key: str) -> Any:
        """Enable dictionary-style access for unpacking.
        
        This allows using **config to unpack the configuration object.
        
        Args:
            key: The configuration key to access
            
        Returns:
            The value associated with the key
        """
        return getattr(self, key)

    def validate(self) -> None:
        """Validate the configuration parameters.
        
        Raises:
            ValueError: If any configuration parameter is invalid
        """
        if not self.api_key:
            raise ValueError("api_key cannot be empty")
        if not self.api_base_url:
            raise ValueError("api_base_url cannot be empty")
        if not self.model_name:
            raise ValueError("model_name cannot be empty")
        if self.temperature < 0 or self.temperature > 2:
            raise ValueError("temperature must be between 0 and 2")
        if self.max_tokens <= 0:
            raise ValueError("max_tokens must be positive")
        if self.timeout <= 0:
            raise ValueError("timeout must be positive")
    
    def with_overrides(self, **kwargs) -> 'AgentConfig':
        """Create a new AgentConfig with specified overrides.
        
        Args:
            **kwargs: Configuration parameters to override
            
        Returns:
            New AgentConfig instance with overridden values
        """
        return replace(self, **kwargs)


@dataclass 
class LLMEndpoint:
    """Configuration for a single LLM endpoint."""
    name: str
    api_key: str
    api_base_url: str
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 4096
    timeout: int = 30
    stream: bool = True
    
    def to_agent_config(self) -> AgentConfig:
        """Convert to AgentConfig format for backward compatibility."""
        return AgentConfig(
            api_key=self.api_key,
            api_base_url=self.api_base_url,
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            timeout=self.timeout,
            stream=self.stream
        )