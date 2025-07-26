"""Factory functions and triage system for biological reasoning modes."""

import os
import re
from typing import Dict, Type

from dotenv import load_dotenv
from loguru import logger

from .basics import ReasoningMode
from .comparative_reasoning import ComparativeReasoningMode
from .developmental_reasoning import DevelopmentalReasoningMode
from .example_reasoning import ExampleReasoningMode
from .homeostatic_reasoning import HomeostaticReasoningMode
from .mechanistic_reasoning import MechanisticReasoningMode
from .phylogenetic_reasoning import PhylogeneticReasoningMode
from .probabilistic_reasoning import ProbabilisticReasoningMode
from .spatial_reasoning import SpatialReasoningMode
from .systems_reasoning import SystemsReasoningMode
from .teleonomic_reasoning import TeleonomicReasoningMode
from .temporal_reasoning import TemporalReasoningMode
from .tradeoff_reasoning import TradeoffReasoningMode

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
        raise ValueError(
            f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}"
        )

    reasoning_class = REASONING_MODE_REGISTRY[mode_name]
    return reasoning_class()


def get_available_modes() -> list[str]:
    """
    Get a list of all available reasoning mode names.

    Returns:
        List of available reasoning mode names
    """
    return list(REASONING_MODE_REGISTRY.keys())


def _get_mode_keywords() -> Dict[str, list[str]]:
    """
    Get keywords for all reasoning modes by instantiating them.

    Returns:
        Dictionary mapping mode names to their keywords
    """
    mode_keywords = {}

    for mode_name, mode_class in REASONING_MODE_REGISTRY.items():
        try:
            # Create a temporary instance to get keywords
            temp_instance = mode_class()
            keywords = getattr(temp_instance, "keywords", [])
            mode_keywords[mode_name] = keywords
        except Exception:
            # If instantiation fails, use empty list
            mode_keywords[mode_name] = []

    return mode_keywords


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

    # Get keywords from reasoning mode instances
    mode_keywords = _get_mode_keywords()

    # Score each reasoning mode based on keyword matches
    mode_scores = {}

    for mode_name, keywords in mode_keywords.items():
        score = 0
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
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

    # Get keywords from reasoning mode instances
    mode_keywords = _get_mode_keywords()

    # Score each reasoning mode based on keyword matches
    mode_scores = {}
    total_keywords_found = 0

    for mode_name, keywords in mode_keywords.items():
        score = 0
        for keyword in keywords:
            # Use word boundaries to avoid partial matches
            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"
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
        second_best_score = (
            sorted(mode_scores.values(), reverse=True)[1] if len(mode_scores) > 1 else 0
        )
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
        "example": "Demonstrates the general reasoning framework with basic biological analysis",
    }

    if mode_name not in descriptions:
        available_modes = list(descriptions.keys())
        raise ValueError(
            f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}"
        )

    return descriptions[mode_name]


def llm_triage_reasoning_mode(
    user_question: str,
    context: str = "",
    api_key: str = None,
    api_base_url: str = None,
    model_name: str = None,
) -> tuple[str, float, str]:
    """
    Use an LLM to determine the most appropriate reasoning mode based on user input.

    Args:
        user_question: The user's question or task description
        context: Additional context that might help with triage (optional)
        api_key: API key for the LLM service (optional, will use env var if not provided)
        api_base_url: Base URL for the LLM API (optional, will use env var if not provided)
        model_name: Name of the LLM model to use (optional, will use env var if not provided)

    Returns:
        Tuple of (recommended_mode, confidence_score, reasoning)
        confidence_score is between 0 and 1
        reasoning is the LLM's explanation for the choice
    """
    # Load environment variables if not provided
    load_dotenv()
    api_key = api_key or os.getenv("API_KEY", "sk-xxxxxx")
    api_base_url = api_base_url or os.getenv("BASE_URL", "https://api.openai.com/v1")
    model_name = model_name or os.getenv("MODEL_NAME", "gpt-4")

    # Get all available reasoning modes with their descriptions
    available_modes = {}
    for mode_name, mode_class in REASONING_MODE_REGISTRY.items():
        try:
            # Create a temporary instance to get the system prompt and keywords
            temp_instance = mode_class()
            available_modes[mode_name] = {
                "description": get_mode_description(mode_name),
                "system_prompt": temp_instance.sys_prompt,
                "keywords": getattr(temp_instance, "keywords", []),
            }
        except Exception:
            # Fallback if instantiation fails
            available_modes[mode_name] = {
                "description": get_mode_description(mode_name),
                "system_prompt": f"Expert in {mode_name} reasoning",
                "keywords": [],
            }

    # Construct the triage prompt
    modes_info = []
    for mode_name, info in available_modes.items():
        keywords_str = ", ".join(info["keywords"][:10])  # Limit to first 10 keywords
        modes_info.append(f"""
**{mode_name.upper()}**:
- Description: {info["description"]}
- Keywords: {keywords_str}
- System Prompt: {info["system_prompt"][:200]}...
""")

    triage_prompt = f"""You are an expert biological reasoning mode selector. Your task is to analyze a user's question and determine which reasoning mode would be most appropriate.

Available reasoning modes:
{"".join(modes_info)}

User Question: "{user_question}"
Additional Context: "{context}"

Please analyze the question and select the most appropriate reasoning mode. Consider:
1. The type of biological question being asked
2. The keywords and concepts mentioned
3. The level of analysis required (molecular, cellular, organismal, evolutionary, etc.)
4. The methodology that would be most suitable

Respond in the following JSON format:
{{
    "selected_mode": "mode_name",
    "confidence": 0.95,
    "reasoning": "Explanation of why this mode was selected, mentioning specific keywords or concepts that led to this choice."
}}

The confidence should be between 0 and 1, where 1 means you are completely certain this is the correct mode.
"""

    try:
        # Import here to avoid circular imports and handle missing dependencies
        import json

        import requests

        # Make API call to LLM
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        data = {
            "model": model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert biological reasoning mode selector. Always respond with valid JSON.",
                },
                {"role": "user", "content": triage_prompt},
            ],
            "temperature": 0.1,  # Low temperature for consistent results
            "max_tokens": 500,
        }

        response = requests.post(
            f"{api_base_url}/chat/completions", headers=headers, json=data, timeout=30
        )
        response.raise_for_status()

        result = response.json()
        llm_response = result["choices"][0]["message"]["content"]

        # Parse the JSON response
        try:
            parsed_response = json.loads(llm_response)
            logger.debug(f"LLM response: {parsed_response}")
            selected_mode = parsed_response.get("selected_mode", "mechanistic").lower()
            confidence = float(parsed_response.get("confidence", 0.5))
            reasoning = parsed_response.get("reasoning", "LLM analysis completed")

            # Validate the selected mode
            if selected_mode not in REASONING_MODE_REGISTRY:
                # Fallback to keyword-based triage
                selected_mode = triage_reasoning_mode(user_question, context)
                confidence = 0.3
                reasoning = f"LLM selected invalid mode, fell back to keyword-based triage: {selected_mode}"

            return selected_mode, confidence, reasoning

        except json.JSONDecodeError:
            # Fallback to keyword-based triage if JSON parsing fails
            selected_mode = triage_reasoning_mode(user_question, context)
            return (
                selected_mode,
                0.3,
                f"LLM response parsing failed, used keyword-based triage: {selected_mode}",
            )

    except Exception as e:
        # Fallback to keyword-based triage if LLM call fails
        selected_mode = triage_reasoning_mode(user_question, context)
        return (
            selected_mode,
            0.2,
            f"LLM triage failed ({str(e)}), used keyword-based triage: {selected_mode}",
        )


def get_reasoning_mode_info(mode_name: str) -> dict:
    """
    Get comprehensive information about a reasoning mode including keywords and system prompt.

    Args:
        mode_name: Name of the reasoning mode

    Returns:
        Dictionary containing mode information

    Raises:
        ValueError: If the mode_name is not recognized
    """
    if mode_name not in REASONING_MODE_REGISTRY:
        available_modes = list(REASONING_MODE_REGISTRY.keys())
        raise ValueError(
            f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}"
        )

    try:
        # Create a temporary instance to get all information
        temp_instance = REASONING_MODE_REGISTRY[mode_name]()
        return {
            "name": temp_instance.name,
            "description": get_mode_description(mode_name),
            "system_prompt": temp_instance.sys_prompt,
            "keywords": getattr(temp_instance, "keywords", []),
            "name_canonical": getattr(temp_instance, "name_canonical", mode_name),
        }
    except Exception as e:
        # Return basic information if instantiation fails
        return {
            "name": mode_name.title() + " Reasoning",
            "description": get_mode_description(mode_name),
            "system_prompt": f"Expert in {mode_name} reasoning",
            "keywords": [],
            "name_canonical": mode_name,
            "error": str(e),
        }


# Legacy support - keep the old function name for backward compatibility
create_reasoning_mode_from_prompt = create_reasoning_mode


if __name__ == "__main__":
    # LLM-based triage (preferred method)
    mode, confidence, reasoning = llm_triage_reasoning_mode(
        "How did natural selection shape bird flight evolution?"
    )
    # returns ("teleonomic", 0.97, "detailed reasoning explanation...")

    # Keyword-based triage (fallback option)
    mode = triage_reasoning_mode("What is the molecular mechanism?")
    # returns "mechanistic"

    # Create reasoning mode instance
    reasoning_mode = create_reasoning_mode(mode)