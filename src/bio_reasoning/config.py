"""Central configuration management for the BioR5 framework.

This module provides centralized configuration management with support for
multiple LLM endpoints, environment variable handling, and graceful fallbacks.
"""

import os
from typing import Dict, Optional, List
from loguru import logger
from dotenv import load_dotenv

from .agent.config import AgentConfig, LLMEndpoint


class ConfigurationError(Exception):
    """Raised when there are configuration-related errors."""
    pass


class CentralConfig:
    """Centralized configuration for all LLM endpoints."""
    
    def __init__(self):
        """Initialize configuration by loading from environment variables."""
        # Load environment variables
        load_dotenv()
        
        self.endpoints: Dict[str, LLMEndpoint] = {}
        self._load_endpoints()
    
    def _load_endpoints(self) -> None:
        """Load endpoint configurations from environment variables."""
        # Load primary endpoint (required)
        self.endpoints["primary"] = self._load_primary_endpoint()
        
        # Load optional endpoints
        if self._has_txgemma_config():
            self.endpoints["txgemma"] = self._load_txgemma_endpoint()
        
        if self._has_registry_config():
            self.endpoints["registry"] = self._load_registry_endpoint()
    
    def _load_primary_endpoint(self) -> LLMEndpoint:
        """Load primary LLM endpoint configuration."""
        # Use BIO_ prefixed variables first, fall back to legacy names
        api_key = (
            os.getenv("BIO_PRIMARY_API_KEY") or 
            os.getenv("API_KEY") or
            os.getenv("MODEL_API_KEY")
        )
        api_base_url = (
            os.getenv("BIO_PRIMARY_BASE_URL") or 
            os.getenv("BASE_URL") or
            os.getenv("MODEL_BASE_URL")
        )
        model_name = (
            os.getenv("BIO_PRIMARY_MODEL_NAME") or 
            os.getenv("MODEL_NAME") or
            os.getenv("MODEL_NAME")
        )
        
        if not api_key:
            raise ConfigurationError(
                "Primary LLM API key not found. Please set BIO_PRIMARY_API_KEY "
                "(or legacy API_KEY) environment variable."
            )
        if not api_base_url:
            raise ConfigurationError(
                "Primary LLM base URL not found. Please set BIO_PRIMARY_BASE_URL "
                "(or legacy BASE_URL) environment variable."
            )
        if not model_name:
            raise ConfigurationError(
                "Primary LLM model name not found. Please set BIO_PRIMARY_MODEL_NAME "
                "(or legacy MODEL_NAME) environment variable."
            )
        
        return LLMEndpoint(
            name="primary",
            api_key=api_key,
            api_base_url=api_base_url,
            model_name=model_name,
            temperature=float(os.getenv("BIO_PRIMARY_TEMPERATURE", "0.7")),
            max_tokens=int(os.getenv("BIO_PRIMARY_MAX_TOKENS", "4096")),
            timeout=int(os.getenv("BIO_PRIMARY_TIMEOUT", "30")),
            stream=os.getenv("BIO_PRIMARY_STREAM", "true").lower() == "true"
        )
    
    def _has_txgemma_config(self) -> bool:
        """Check if TX-Gemma configuration is available."""
        return bool(
            os.getenv("BIO_TXGEMMA_API_KEY") or 
            os.getenv("TXGEMMA_API_KEY")
        )
    
    def _load_txgemma_endpoint(self) -> LLMEndpoint:
        """Load TX-Gemma endpoint configuration."""
        api_key = (
            os.getenv("BIO_TXGEMMA_API_KEY") or 
            os.getenv("TXGEMMA_API_KEY", "EMPTY")
        )
        api_base_url = (
            os.getenv("BIO_TXGEMMA_BASE_URL") or 
            os.getenv("TXGEMMA_BASE_URL", "http://localhost:8000/v1")
        )
        model_name = (
            os.getenv("BIO_TXGEMMA_MODEL_NAME") or 
            os.getenv("TXGEMMA_MODEL_NAME", "google/txgemma-27b-chat")
        )
        
        return LLMEndpoint(
            name="txgemma",
            api_key=api_key,
            api_base_url=api_base_url,
            model_name=model_name,
            temperature=float(os.getenv("BIO_TXGEMMA_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("BIO_TXGEMMA_MAX_TOKENS", "2048")),
            timeout=int(os.getenv("BIO_TXGEMMA_TIMEOUT", "60")),
            stream=os.getenv("BIO_TXGEMMA_STREAM", "false").lower() == "true"
        )
    
    def _has_registry_config(self) -> bool:
        """Check if registry configuration is available."""
        return bool(
            os.getenv("BIO_REGISTRY_API_KEY") or
            os.getenv("BIO_REGISTRY_MODEL_NAME")
        )
    
    def _load_registry_endpoint(self) -> LLMEndpoint:
        """Load registry endpoint configuration."""
        # Registry can reuse primary credentials if not specified
        primary = self.endpoints["primary"]
        
        api_key = (
            os.getenv("BIO_REGISTRY_API_KEY") or 
            primary.api_key
        )
        api_base_url = (
            os.getenv("BIO_REGISTRY_BASE_URL") or 
            primary.api_base_url
        )
        model_name = (
            os.getenv("BIO_REGISTRY_MODEL_NAME") or 
            "gpt-4-turbo"  # Default to faster model for triage
        )
        
        return LLMEndpoint(
            name="registry",
            api_key=api_key,
            api_base_url=api_base_url,
            model_name=model_name,
            temperature=float(os.getenv("BIO_REGISTRY_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("BIO_REGISTRY_MAX_TOKENS", "800")),
            timeout=int(os.getenv("BIO_REGISTRY_TIMEOUT", "30")),
            stream=os.getenv("BIO_REGISTRY_STREAM", "false").lower() == "true"
        )
    
    def has_endpoint(self, endpoint_name: str) -> bool:
        """Check if an endpoint is configured and available."""
        return endpoint_name in self.endpoints
    
    def get_agent_config(self, endpoint_name: str = "primary") -> AgentConfig:
        """Get AgentConfig for a specific endpoint.
        
        Args:
            endpoint_name: Name of the endpoint ("primary", "txgemma", "registry")
            
        Returns:
            AgentConfig for the specified endpoint
            
        Raises:
            ConfigurationError: If endpoint is not configured
        """
        if endpoint_name not in self.endpoints:
            if endpoint_name == "primary":
                raise ConfigurationError(f"Primary endpoint not configured")
            else:
                # For optional endpoints, fall back to primary
                logger.warning(
                    f"Endpoint '{endpoint_name}' not configured, falling back to primary LLM"
                )
                return self.get_agent_config("primary")
        
        return self.endpoints[endpoint_name].to_agent_config()
    
    def get_endpoint(self, endpoint_name: str) -> Optional[LLMEndpoint]:
        """Get LLMEndpoint configuration.
        
        Args:
            endpoint_name: Name of the endpoint
            
        Returns:
            LLMEndpoint or None if not configured
        """
        return self.endpoints.get(endpoint_name)
    
    def list_endpoints(self) -> List[str]:
        """List all configured endpoint names."""
        return list(self.endpoints.keys())
    
    def is_valid(self) -> bool:
        """Check if the configuration is valid."""
        try:
            # Primary endpoint is required
            primary_config = self.get_agent_config("primary")
            primary_config.validate()
            return True
        except (ConfigurationError, ValueError):
            return False
    
    def get_missing_configs(self) -> List[str]:
        """Get list of missing required configuration items."""
        missing = []
        
        if not os.getenv("BIO_PRIMARY_API_KEY") and not os.getenv("API_KEY"):
            missing.append("BIO_PRIMARY_API_KEY or API_KEY")
        if not os.getenv("BIO_PRIMARY_BASE_URL") and not os.getenv("BASE_URL"):
            missing.append("BIO_PRIMARY_BASE_URL or BASE_URL")
        if not os.getenv("BIO_PRIMARY_MODEL_NAME") and not os.getenv("MODEL_NAME"):
            missing.append("BIO_PRIMARY_MODEL_NAME or MODEL_NAME")
            
        return missing


class ConfigManager:
    """Singleton configuration manager for the BioR5 framework."""
    
    _instance: Optional['ConfigManager'] = None
    _config: Optional[CentralConfig] = None
    
    def __new__(cls) -> 'ConfigManager':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_config(cls) -> CentralConfig:
        """Get the central configuration instance.
        
        Returns:
            CentralConfig instance
            
        Raises:
            ConfigurationError: If configuration cannot be loaded
        """
        if cls._config is None:
            cls._config = CentralConfig()
            logger.info(f"Loaded configuration with endpoints: {cls._config.list_endpoints()}")
        return cls._config
    
    @classmethod
    def reset(cls) -> None:
        """Reset the configuration (useful for testing)."""
        cls._instance = None
        cls._config = None


# Convenience functions for backward compatibility
def get_config() -> CentralConfig:
    """Get the central configuration instance."""
    return ConfigManager.get_config()


def get_agent_config(endpoint: str = "primary") -> AgentConfig:
    """Get AgentConfig for a specific endpoint."""
    return ConfigManager.get_config().get_agent_config(endpoint)

