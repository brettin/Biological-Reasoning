"""
Layer A is the parametric memory of a general large language model (LLM), capturing broadly applicable knowledge pre-trained or fine-tuned into its weights.
"""

from .parametric_memory import parametric_memory_factory

__all__ = [
    "parametric_memory_factory",
]
