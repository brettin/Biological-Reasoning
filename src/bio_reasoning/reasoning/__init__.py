"""
Reasoning Mode defines 1) the available tools and 2) the system prompt for the LLM in this specific mode. System prompt could contain instruction on which order to use the tools, or which tool to use first, etc. Tools are presented as a ToolRegistry instance, which will handle the tool selection and execution.
"""

from .basics import ReasoningMode
from .example_reasoning import ExampleReasoningMode

__all__ = [
    "ReasoningMode",
    "ExampleReasoningMode",  # this should be removed after we have a real reasoning mode, this is just a demo
]