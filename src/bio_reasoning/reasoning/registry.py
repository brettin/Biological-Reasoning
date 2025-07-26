"""Simplified ReasoningModeRegistry for biological reasoning modes."""

import os
import re
from typing import Dict, Tuple, Type

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


class ReasoningModeRegistry:
    """
    Simple registry for managing biological reasoning modes with intelligent triage.

    This registry maintains a collection of reasoning modes and provides
    hybrid triage functionality to map user queries to the most appropriate mode.
    """

    def __init__(self):
        """Initialize the registry with built-in reasoning modes."""
        self._modes: Dict[str, Type[ReasoningMode]] = {}
        self._mode_cache: Dict[str, ReasoningMode] = {}
        self._register_builtin_modes()

    def _register_builtin_modes(self) -> None:
        """Register all built-in reasoning modes."""
        builtin_modes = {
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

        for name, mode_class in builtin_modes.items():
            self._modes[name] = mode_class

    def get_available_modes(self) -> Dict[str, Type[ReasoningMode]]:
        """Get all available reasoning modes."""
        return self._modes.copy()

    def create_mode(self, mode_name: str) -> ReasoningMode:
        """
        Create an instance of a reasoning mode.

        Args:
            mode_name: Name of the reasoning mode

        Returns:
            A ReasoningMode instance

        Raises:
            ValueError: If the mode is not registered
        """
        if mode_name not in self._modes:
            available_modes = list(self._modes.keys())
            raise ValueError(
                f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}"
            )

        # Use cached instance if available
        if mode_name in self._mode_cache:
            return self._mode_cache[mode_name]

        # Create and cache new instance
        mode_class = self._modes[mode_name]
        instance = mode_class()
        self._mode_cache[mode_name] = instance
        return instance

    def get_mode_info(self, mode_name: str) -> Dict[str, any]:
        """
        Get information about a reasoning mode.

        Args:
            mode_name: Name of the reasoning mode

        Returns:
            Dictionary containing mode information
        """
        if mode_name not in self._modes:
            raise ValueError(f"Unknown reasoning mode: {mode_name}")

        # Get instance and call describe method
        instance = self.create_mode(mode_name)
        return instance.describe()

    def triage(self, query: str, context: str = "") -> Tuple[str, float, str]:
        """
        Intelligently select the most appropriate reasoning mode using hybrid approach.

        This method combines keyword-based and LLM-based triage for optimal results.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            Tuple of (selected_mode, confidence_score, reasoning_explanation)
        """
        # Get keyword-based result
        keyword_mode, keyword_confidence = self._triage_keyword(query, context)

        # Get LLM-based result
        llm_mode, llm_confidence, llm_reasoning = self._triage_llm(query, context)

        # Hybrid decision logic
        if keyword_mode == llm_mode:
            # Both methods agree - use higher confidence
            confidence = max(keyword_confidence, llm_confidence)
            reasoning = f"Both keyword and LLM methods selected {keyword_mode}"
            return keyword_mode, confidence, reasoning

        elif llm_confidence > 0.7:
            # LLM has high confidence - prefer LLM
            confidence = llm_confidence * 0.9  # Slight penalty for disagreement
            reasoning = f"LLM selected {llm_mode} (high confidence), keyword suggested {keyword_mode}"
            return llm_mode, confidence, reasoning

        else:
            # LLM has low confidence - prefer keyword
            confidence = keyword_confidence * 0.8  # Penalty for disagreement
            reasoning = f"Keyword selected {keyword_mode}, LLM suggested {llm_mode} (low confidence)"
            return keyword_mode, confidence, reasoning

    def _triage_keyword(self, query: str, context: str = "") -> Tuple[str, float]:
        """
        Keyword-based triage implementation.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            Tuple of (selected_mode, confidence_score)
        """
        # Combine question and context for analysis
        text_to_analyze = f"{query} {context}".lower()

        # Get keywords from reasoning mode instances
        mode_keywords = {}
        for mode_name in self._modes.keys():
            try:
                instance = self.create_mode(mode_name)
                keywords = getattr(instance, "keywords", [])
                mode_keywords[mode_name] = keywords
            except Exception:
                mode_keywords[mode_name] = []

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
            # If no keywords match, default to mechanistic reasoning
            return "mechanistic", 0.1

        best_mode = max(mode_scores, key=mode_scores.get)
        best_score = mode_scores[best_mode]

        # Calculate confidence
        if total_keywords_found == 0:
            confidence = 0.1
        else:
            # Base confidence on the proportion of total matches
            base_confidence = best_score / total_keywords_found

            # Boost confidence if this mode clearly dominates
            second_best_score = (
                sorted(mode_scores.values(), reverse=True)[1]
                if len(mode_scores) > 1
                else 0
            )
            if best_score > second_best_score * 2:
                base_confidence = min(1.0, base_confidence * 1.5)

            confidence = min(1.0, base_confidence)

        return best_mode, confidence

    def _triage_llm(self, query: str, context: str = "") -> Tuple[str, float, str]:
        """
        LLM-based triage implementation.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            Tuple of (selected_mode, confidence_score, reasoning_explanation)
        """
        try:
            # Load environment variables
            load_dotenv()
            api_key = os.getenv("API_KEY", "sk-xxxxxx")
            api_base_url = os.getenv("BASE_URL", "https://api.openai.com/v1")
            model_name = os.getenv("MODEL_NAME", "gpt-4")

            # Get mode descriptions
            mode_descriptions = {}
            for mode_name in self._modes.keys():
                try:
                    info = self.get_mode_info(mode_name)
                    mode_descriptions[mode_name] = info.get(
                        "description", f"Reasoning for {mode_name}"
                    )
                except Exception:
                    mode_descriptions[mode_name] = f"Reasoning for {mode_name}"

            # Construct the triage prompt
            modes_info = []
            for mode_name, description in mode_descriptions.items():
                modes_info.append(f"**{mode_name.upper()}**: {description}")

            triage_prompt = f"""You are an expert biological reasoning mode selector. Analyze the user's question and select the most appropriate reasoning mode.

Available reasoning modes:
{chr(10).join(modes_info)}

User Question: "{query}"
Additional Context: "{context}"

Respond in JSON format:
{{
    "selected_mode": "mode_name",
    "confidence": 0.95,
    "reasoning": "Explanation of why this mode was selected."
}}

The confidence should be between 0 and 1."""

            # Import here to handle missing dependencies
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
                "temperature": 0.1,
                "max_tokens": 500,
            }

            response = requests.post(
                f"{api_base_url}/chat/completions",
                headers=headers,
                json=data,
                timeout=30,
            )
            response.raise_for_status()

            result = response.json()
            llm_response = result["choices"][0]["message"]["content"]

            # Parse the JSON response
            parsed_response = json.loads(llm_response)
            selected_mode = parsed_response.get("selected_mode", "mechanistic").lower()
            confidence = float(parsed_response.get("confidence", 0.5))
            reasoning = parsed_response.get("reasoning", "LLM analysis completed")

            # Validate the selected mode
            if selected_mode not in self._modes:
                # Fallback to keyword-based triage
                fallback_mode, fallback_confidence = self._triage_keyword(
                    query, context
                )
                return (
                    fallback_mode,
                    0.3,
                    f"LLM selected invalid mode, used keyword fallback: {fallback_mode}",
                )

            return selected_mode, confidence, reasoning

        except Exception as e:
            # Fallback to keyword-based triage if LLM call fails
            fallback_mode, fallback_confidence = self._triage_keyword(query, context)
            return (
                fallback_mode,
                0.2,
                f"LLM triage failed ({str(e)}), used keyword fallback: {fallback_mode}",
            )


# Create a global registry instance
registry = ReasoningModeRegistry()


# Convenience functions that use the global registry
def create_reasoning_mode(mode_name: str) -> ReasoningMode:
    """Create a reasoning mode instance using the global registry."""
    return registry.create_mode(mode_name)


def get_available_modes() -> list[str]:
    """Get list of available reasoning mode names."""
    return list(registry.get_available_modes().keys())


def triage_reasoning_mode(query: str, context: str = "") -> str:
    """Triage to select the best reasoning mode."""
    mode, _, _ = registry.triage(query, context)
    return mode


def triage_with_confidence(query: str, context: str = "") -> Tuple[str, float]:
    """Triage with confidence score."""
    mode, confidence, _ = registry.triage(query, context)
    return mode, confidence


def get_mode_info(mode_name: str) -> Dict[str, any]:
    """Get information about a reasoning mode."""
    return registry.get_mode_info(mode_name)


if __name__ == "__main__":
    # Demo the simplified registry
    print("🧬 Simplified Bio-Reasoning Registry Demo")
    print("=" * 50)

    # Test triage
    query = "How did natural selection shape bird flight evolution?"
    mode, confidence, reasoning = registry.triage(query)
    print(f"Query: {query}")
    print(f"Selected Mode: {mode}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Reasoning: {reasoning}")
    print()

    # Test mode creation
    reasoning_mode = create_reasoning_mode(mode)
    print(f"Created mode: {reasoning_mode.name}")

    # Test available modes
    print(f"Available modes: {len(get_available_modes())}")
    print("Registry successfully initialized!")