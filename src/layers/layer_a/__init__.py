"""Layer A: Parametric Memory implementation."""

from src.layers.layer_a.base import ParametricMemory, BiologicalKnowledgeStore

# Import distllm implementation if available
try:
    from src.layers.layer_a.distllm_impl import DistllmParametricMemory
    __all__ = ['ParametricMemory', 'BiologicalKnowledgeStore', 'DistllmParametricMemory']
except ImportError:
    __all__ = ['ParametricMemory', 'BiologicalKnowledgeStore']

from src.layers.layer_a.base import ParametricMemory
from src.layers.layer_a.base import BiologicalKnowledgeStore
from src.layers.layer_a.distllm_impl import DistllmParametricMemory

__all__ = ['ParametricMemory', 'BiologicalKnowledgeStore', 'DistllmParametricMemory']

