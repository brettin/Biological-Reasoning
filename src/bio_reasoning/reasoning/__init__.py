"""
Reasoning Mode defines 1) the available tools and 2) the system prompt for the LLM in this specific mode. System prompt could contain instruction on which order to use the tools, or which tool to use first, etc. Tools are presented as a ToolRegistry instance, which will handle the tool selection and execution.

The concrete reasoning modes are organized in the `modes` submodule for better structure.
Use: `from bio_reasoning.reasoning.modes import MechanisticReasoningMode`
"""

from .basics import ReasoningMode
from .example_reasoning import ExampleReasoningMode

# Import registry functions for convenience
from .registry import (
    create_reasoning_mode,
    get_available_modes,
    triage_reasoning_mode,
    triage_with_confidence,
    get_mode_info,
)

__all__ = [
    "ReasoningMode",
    "ExampleReasoningMode",  # this should be removed after we have a real reasoning mode, this is just a demo
    # Registry functions
    "create_reasoning_mode",
    "get_available_modes",
    "triage_reasoning_mode",
    "triage_with_confidence",
    "get_mode_info",
]