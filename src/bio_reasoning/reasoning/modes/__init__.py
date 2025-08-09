"""
Biological reasoning modes for specialized analysis.

This module contains 11 concrete reasoning modes that provide specialized
biological analysis capabilities for different types of questions and contexts.
"""

from .comparative_reasoning import ComparativeReasoningMode
from .developmental_reasoning import DevelopmentalReasoningMode
from .homeostatic_reasoning import HomeostaticReasoningMode
from .mechanistic_reasoning import MechanisticReasoningMode
from .phylogenetic_reasoning import PhylogeneticReasoningMode
from .probabilistic_reasoning import ProbabilisticReasoningMode
from .spatial_reasoning import SpatialReasoningMode
from .systems_reasoning import SystemsReasoningMode
from .teleonomic_reasoning import TeleonomicReasoningMode
from .temporal_reasoning import TemporalReasoningMode
from .tradeoff_reasoning import TradeoffReasoningMode

__all__ = [
    "ComparativeReasoningMode",
    "DevelopmentalReasoningMode", 
    "HomeostaticReasoningMode",
    "MechanisticReasoningMode",
    "PhylogeneticReasoningMode",
    "ProbabilisticReasoningMode",
    "SpatialReasoningMode",
    "SystemsReasoningMode",
    "TeleonomicReasoningMode",
    "TemporalReasoningMode",
    "TradeoffReasoningMode",
]