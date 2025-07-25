"""Factory functions and triage system for biological reasoning modes."""

import re
from typing import Dict, Type, Optional

from .basics import ReasoningMode
from .phylogenetic_reasoning import PhylogeneticReasoningMode
from .teleonomic_reasoning import TeleonomicReasoningMode
from .tradeoff_reasoning import TradeoffReasoningMode
from .mechanistic_reasoning import MechanisticReasoningMode
from .systems_reasoning import SystemsReasoningMode
from .probabilistic_reasoning import ProbabilisticReasoningMode
from .spatial_reasoning import SpatialReasoningMode
from .temporal_reasoning import TemporalReasoningMode
from .homeostatic_reasoning import HomeostaticReasoningMode
from .developmental_reasoning import DevelopmentalReasoningMode
from .comparative_reasoning import ComparativeReasoningMode
from .example_reasoning import ExampleReasoningMode


# Registry of available reasoning modes
REASONING_MODE_REGISTRY: Dict[str, Type[ReasoningMode]] = {
    "phylogenetic": PhylogeneticReasoningMode,
    "teleonomic": TeleonomicReasoningMode,
    "tradeoff": TradeoffReasoningMode,
    "mechanistic": MechanisticReasoningMode,
    "systems": SystemsReasoningMode,
    "probabilistic": ProbabilisticReasoningMode,
    "spatial": SpatialReasoningMode,
    "temporal": TemporalReasoningMode,
    "homeostatic": HomeostaticReasoningMode,
    "developmental": DevelopmentalReasoningMode,
    "comparative": ComparativeReasoningMode,
    "example": ExampleReasoningMode,
}


def create_reasoning_mode(mode_name: str) -> ReasoningMode:
    """
    Factory function to create a reasoning mode instance.
    
    Args:
        mode_name: Name of the reasoning mode (must be in REASONING_MODE_REGISTRY)
    
    Returns:
        A ReasoningMode instance of the specified type
        
    Raises:
        ValueError: If the mode_name is not recognized
    """
    if mode_name not in REASONING_MODE_REGISTRY:
        available_modes = list(REASONING_MODE_REGISTRY.keys())
        raise ValueError(f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}")
    
    reasoning_class = REASONING_MODE_REGISTRY[mode_name]
    return reasoning_class()


def get_available_modes() -> list[str]:
    """
    Get a list of all available reasoning mode names.
    
    Returns:
        List of available reasoning mode names
    """
    return list(REASONING_MODE_REGISTRY.keys())


# Triage keywords for each reasoning mode
TRIAGE_KEYWORDS = {
    "phylogenetic": [
        "phylogeny", "phylogenetic", "evolution", "evolutionary", "tree", "clade", "ancestor", 
        "ancestral", "divergence", "speciation", "homolog", "ortholog", "paralog", "sequence alignment",
        "molecular clock", "common ancestor", "branching", "monophyletic", "paraphyletic"
    ],
    "teleonomic": [
        "function", "adaptive", "adaptation", "fitness", "advantage", "benefit", "purpose", 
        "survival", "reproduction", "natural selection", "selective pressure", "evolutionary advantage",
        "why evolved", "what for", "in order to", "functional significance"
    ],
    "tradeoff": [
        "tradeoff", "trade-off", "cost", "benefit", "allocation", "resource", "constraint", 
        "optimization", "balance", "competing", "conflict", "compromise", "energy budget",
        "life history", "pareto", "optimal"
    ],
    "mechanistic": [
        "mechanism", "molecular", "pathway", "signaling", "cascade", "interaction", "binding",
        "enzyme", "protein", "gene expression", "regulation", "transcription", "translation",
        "how does", "step by step", "process", "causal chain", "biochemical"
    ],
    "systems": [
        "network", "system", "systems biology", "emergent", "feedback", "loop", "circuit",
        "module", "motif", "topology", "connectivity", "robustness", "dynamics", "oscillation",
        "bistability", "multi-scale", "integration"
    ],
    "probabilistic": [
        "probability", "statistical", "stochastic", "random", "variability", "uncertainty",
        "distribution", "bayesian", "likelihood", "confidence", "variance", "noise",
        "population", "frequency", "risk", "chance"
    ],
    "spatial": [
        "spatial", "location", "position", "geometry", "structure", "3d", "localization",
        "diffusion", "gradient", "pattern", "morphology", "shape", "arrangement", "organization",
        "tissue", "cellular", "molecular structure"
    ],
    "temporal": [
        "time", "temporal", "dynamics", "kinetics", "rate", "timing", "sequence", "order",
        "phase", "cycle", "rhythm", "circadian", "oscillation", "delay", "duration",
        "time course", "chronology", "development over time"
    ],
    "homeostatic": [
        "homeostasis", "regulation", "control", "feedback", "setpoint", "maintain", "stability",
        "physiological", "sensor", "effector", "negative feedback", "positive feedback",
        "equilibrium", "steady state", "perturbation"
    ],
    "developmental": [
        "development", "developmental", "embryo", "morphogenesis", "differentiation", "induction",
        "lineage", "fate", "specification", "determination", "organogenesis", "gastrulation",
        "neurulation", "segmentation", "axis formation", "gene regulatory network"
    ],
    "comparative": [
        "comparative", "comparison", "model organism", "species", "cross-species", "homology",
        "analogy", "conservation", "divergence", "similarity", "difference", "ortholog",
        "mouse", "fly", "worm", "yeast", "zebrafish", "across species"
    ]
}


def triage_reasoning_mode(user_question: str, context: str = "") -> str:
    """
    Automatically determine the most appropriate reasoning mode based on user input.
    
    Args:
        user_question: The user's question or task description
        context: Additional context that might help with triage (optional)
    
    Returns:
        The name of the recommended reasoning mode
    """
    # Combine question and context for analysis
    text_to_analyze = f"{user_question} {context}".lower()
    
    # Score each reasoning mode based on keyword matches
    mode_scores = {}
    
    for mode_name, keywords in TRIAGE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = len(re.findall(pattern, text_to_analyze))
            score += matches
        
        mode_scores[mode_name] = score
    
    # Find the mode with the highest score
    if not mode_scores or max(mode_scores.values()) == 0:
        # If no keywords match, default to mechanistic reasoning
        return "mechanistic"
    
    # Return the mode with the highest score
    best_mode = max(mode_scores, key=mode_scores.get)
    return best_mode


def triage_with_confidence(user_question: str, context: str = "") -> tuple[str, float]:
    """
    Determine the most appropriate reasoning mode with a confidence score.
    
    Args:
        user_question: The user's question or task description
        context: Additional context that might help with triage (optional)
    
    Returns:
        Tuple of (recommended_mode, confidence_score)
        confidence_score is between 0 and 1
    """
    # Combine question and context for analysis
    text_to_analyze = f"{user_question} {context}".lower()
    
    # Score each reasoning mode based on keyword matches
    mode_scores = {}
    total_keywords_found = 0
    
    for mode_name, keywords in TRIAGE_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            matches = len(re.findall(pattern, text_to_analyze))
            score += matches
            total_keywords_found += matches
        
        mode_scores[mode_name] = score
    
    # Find the mode with the highest score
    if not mode_scores or max(mode_scores.values()) == 0:
        # If no keywords match, default to mechanistic reasoning with low confidence
        return "mechanistic", 0.1
    
    best_mode = max(mode_scores, key=mode_scores.get)
    best_score = mode_scores[best_mode]
    
    # Calculate confidence based on the proportion of keywords that matched the best mode
    # and how much it dominates other modes
    if total_keywords_found == 0:
        confidence = 0.1
    else:
        # Base confidence on the proportion of total matches
        base_confidence = best_score / total_keywords_found
        
        # Boost confidence if this mode clearly dominates
        second_best_score = sorted(mode_scores.values(), reverse=True)[1] if len(mode_scores) > 1 else 0
        if best_score > second_best_score * 2:
            base_confidence = min(1.0, base_confidence * 1.5)
        
        confidence = min(1.0, base_confidence)
    
    return best_mode, confidence


def get_mode_description(mode_name: str) -> str:
    """
    Get a description of what a reasoning mode is designed for.
    
    Args:
        mode_name: Name of the reasoning mode
        
    Returns:
        Description of the reasoning mode's purpose
        
    Raises:
        ValueError: If the mode_name is not recognized
    """
    descriptions = {
        "phylogenetic": "Analyzes evolutionary relationships, phylogenetic trees, and ancestral connections",
        "teleonomic": "Examines adaptive functions, fitness advantages, and evolutionary purposes",
        "tradeoff": "Studies competing biological traits, resource allocation, and optimization",
        "mechanistic": "Investigates molecular mechanisms, pathways, and step-by-step processes",
        "systems": "Analyzes biological networks, emergent properties, and system-level behaviors",
        "probabilistic": "Handles statistical analysis, uncertainty quantification, and stochastic processes",
        "spatial": "Examines spatial patterns, geometric relationships, and structural organization",
        "temporal": "Studies time-dependent processes, dynamics, and temporal sequences",
        "homeostatic": "Analyzes regulatory mechanisms, feedback control, and physiological stability",
        "developmental": "Investigates developmental processes, morphogenesis, and gene regulation",
        "comparative": "Performs cross-species analysis, model organism studies, and evolutionary comparisons",
        "example": "Demonstrates the general reasoning framework with basic biological analysis"
    }
    
    if mode_name not in descriptions:
        available_modes = list(descriptions.keys())
        raise ValueError(f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}")
    
    return descriptions[mode_name]


# Legacy support - keep the old function name for backward compatibility
create_reasoning_mode_from_prompt = create_reasoning_mode