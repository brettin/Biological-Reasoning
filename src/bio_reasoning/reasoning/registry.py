"""Simplified ReasoningModeRegistry for biological reasoning modes."""

import os
import re
from typing import Dict, List, Optional, Tuple, Type

from dotenv import load_dotenv
from loguru import logger

from .basics import ReasoningMode
from .modes import (
    ComparativeReasoningMode,
    DevelopmentalReasoningMode,
    HomeostaticReasoningMode,
    MechanisticReasoningMode,
    PhylogeneticReasoningMode,
    ProbabilisticReasoningMode,
    SpatialReasoningMode,
    SystemsReasoningMode,
    TeleonomicReasoningMode,
    TemporalReasoningMode,
    TradeoffReasoningMode,
)


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
        }

        for name, mode_class in builtin_modes.items():
            self._modes[name] = mode_class

    def get_available_modes(self) -> Dict[str, Type[ReasoningMode]]:
        """Get all available reasoning modes."""
        return self._modes.copy()

    def create_mode(self, mode_name: str, user_query: Optional[str] = None) -> ReasoningMode:
        """
        Create an instance of a reasoning mode.

        Args:
            mode_name: Name of the reasoning mode
            user_query: Optional user query for instantiation pattern customization

        Returns:
            A ReasoningMode instance

        Raises:
            ValueError: If the mode is not registered
        """
        # Handle instantiation patterns (specializations of base modes)
        if mode_name == "toxicology":
            return self._create_toxicology_mode(user_query)
        
        if mode_name not in self._modes:
            available_modes = list(self._modes.keys()) + ["toxicology"]  # Include instantiation patterns
            raise ValueError(
                f"Unknown reasoning mode: {mode_name}. Available modes: {available_modes}"
            )

        # Use cached instance if available (only for base modes, not instantiations)
        if mode_name in self._mode_cache and user_query is None:
            return self._mode_cache[mode_name]

        # Create and cache new instance
        mode_class = self._modes[mode_name]
        instance = mode_class()
        
        # Only cache base modes (instantiations are customized and shouldn't be cached)
        if user_query is None:
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

    def triage(
        self,
        query: str,
        context: str = "",
        threshold: float = None,
        num_choices: int = 2
    ):
        """
        Intelligently select reasoning mode(s) using hybrid approach.

        This method combines keyword-based and LLM-based triage for optimal results.
        Can return single best mode or multiple candidates based on parameters.

        Args:
            query: User's question or task description
            context: Additional context information
            threshold: Minimum confidence threshold for candidates (None for single mode)
            num_choices: Maximum number of candidates to return (default: 2)

        Returns:
            If threshold is None: Tuple of (selected_mode, confidence_score, reasoning_explanation)
            If threshold is provided: List of tuples (mode_name, confidence_score, reasoning_explanation)
        """
        # If threshold is provided, return multiple candidates
        if threshold is not None:
            return self.triage_multiple(query, context, threshold, num_choices)
        
        # Original single-mode logic
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

    def triage_multiple(
        self,
        query: str,
        context: str = "",
        threshold: float = 0.3,
        num_choices: int = 2
    ) -> List[Tuple[str, float, str]]:
        """
        Select multiple candidate reasoning modes with confidence scores.

        Args:
            query: User's question or task description
            context: Additional context information
            threshold: Minimum confidence threshold for candidates (0.0-1.0)
            num_choices: Maximum number of candidates to return

        Returns:
            List of tuples (mode_name, confidence_score, reasoning_explanation)
            sorted by confidence score in descending order.
            Result length may be less than num_choices if fewer modes meet threshold.
        """
        # Get keyword-based rankings
        keyword_rankings = self._triage_keyword_multiple(query, context)
        
        # Get LLM-based rankings
        llm_rankings = self._triage_llm_multiple(query, context, num_choices)
        
        # Combine and score all candidates
        combined_scores = {}
        
        # Process keyword rankings
        for mode, score in keyword_rankings:
            if mode not in combined_scores:
                combined_scores[mode] = {'keyword': 0, 'llm': 0, 'explanations': []}
            combined_scores[mode]['keyword'] = score
            combined_scores[mode]['explanations'].append(f"Keyword score: {score:.2f}")
        
        # Process LLM rankings
        for mode, score, explanation in llm_rankings:
            if mode not in combined_scores:
                combined_scores[mode] = {'keyword': 0, 'llm': 0, 'explanations': []}
            combined_scores[mode]['llm'] = score
            combined_scores[mode]['explanations'].append(f"LLM: {explanation}")
        
        # Calculate final scores and create candidates
        candidates = []
        for mode, scores in combined_scores.items():
            keyword_score = scores['keyword']
            llm_score = scores['llm']
            
            # Hybrid scoring: weighted average with agreement bonus
            if keyword_score > 0 and llm_score > 0:
                # Both methods have scores - weighted average with agreement bonus
                final_score = (keyword_score * 0.4 + llm_score * 0.6) * 1.2
                reasoning = f"Hybrid: keyword={keyword_score:.2f}, LLM={llm_score:.2f}"
            elif llm_score > 0:
                # Only LLM has score
                final_score = llm_score * 0.8
                reasoning = f"LLM only: {llm_score:.2f}"
            else:
                # Only keyword has score
                final_score = keyword_score * 0.6
                reasoning = f"Keyword only: {keyword_score:.2f}"
            
            # Ensure score doesn't exceed 1.0
            final_score = min(1.0, final_score)
            
            # Add detailed explanation
            detailed_reasoning = reasoning + "; " + "; ".join(scores['explanations'])
            
            candidates.append((mode, final_score, detailed_reasoning))
        
        # Filter by threshold and sort by confidence
        filtered_candidates = [
            (mode, score, reasoning)
            for mode, score, reasoning in candidates
            if score >= threshold
        ]
        
        # Sort by confidence score (descending) and limit to num_choices
        filtered_candidates.sort(key=lambda x: x[1], reverse=True)
        
        return filtered_candidates[:num_choices]

    def _create_toxicology_mode(self, user_query: Optional[str] = None) -> ReasoningMode:
        """
        Create a toxicology-specialized reasoning mode using instantiation pattern.
        
        This demonstrates the BioR5 instantiation principle:
        - Start with MechanisticReasoningMode (base mode)
        - Augment with toxicology-specific tools
        - Customize system prompt based on user query
        
        Args:
            user_query: User's toxicology question to customize the system prompt
            
        Returns:
            MechanisticReasoningMode instance specialized for toxicology
        """
        try:
            from .toxicology_instantiation import create_toxicology_mode
            return create_toxicology_mode(user_query)
        except ImportError as e:
            logger.warning(f"Could not import toxicology instantiation: {e}")
            # Fallback to base mechanistic mode
            base_mode = self.create_mode("mechanistic")
            base_mode.name = "Mechanistic Toxicology Expert (Basic)"
            base_mode.name_canonical = "toxicology"
            return base_mode

    def _triage_keyword(self, query: str, context: str = "") -> Tuple[str, float]:
        """
        Keyword-based triage implementation.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            Tuple of (selected_mode, confidence_score)
        """
        rankings = self._triage_keyword_multiple(query, context)
        if rankings:
            return rankings[0]
        return "mechanistic", 0.1

    def _triage_keyword_multiple(self, query: str, context: str = "") -> List[Tuple[str, float]]:
        """
        Keyword-based triage implementation returning multiple candidates.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            List of tuples (mode_name, confidence_score) sorted by confidence
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

        # Calculate confidence scores for all modes
        candidates = []
        
        if total_keywords_found == 0:
            # If no keywords match, return mechanistic with low confidence
            return [("mechanistic", 0.1)]

        for mode_name, raw_score in mode_scores.items():
            if raw_score > 0:
                # Base confidence on the proportion of total matches
                base_confidence = raw_score / total_keywords_found
                
                # Boost confidence if this mode has significantly more matches
                other_scores = [s for m, s in mode_scores.items() if m != mode_name]
                max_other_score = max(other_scores) if other_scores else 0
                
                if raw_score > max_other_score * 1.5:
                    base_confidence = min(1.0, base_confidence * 1.3)
                
                confidence = min(1.0, base_confidence)
                candidates.append((mode_name, confidence))

        # Sort by confidence score (descending)
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        return candidates if candidates else [("mechanistic", 0.1)]

    def _triage_llm(self, query: str, context: str = "") -> Tuple[str, float, str]:
        """
        LLM-based triage implementation.

        Args:
            query: User's question or task description
            context: Additional context information

        Returns:
            Tuple of (selected_mode, confidence_score, reasoning_explanation)
        """
        rankings = self._triage_llm_multiple(query, context, 1)
        if rankings:
            return rankings[0]
        
        # Fallback to keyword-based triage
        fallback_mode, fallback_confidence = self._triage_keyword(query, context)
        return fallback_mode, 0.2, f"LLM triage failed, used keyword fallback: {fallback_mode}"

    def _triage_llm_multiple(self, query: str, context: str = "", num_choices: int = 3) -> List[Tuple[str, float, str]]:
        """
        LLM-based triage implementation returning multiple candidates.

        Args:
            query: User's question or task description
            context: Additional context information
            num_choices: Number of candidate modes to return

        Returns:
            List of tuples (mode_name, confidence_score, reasoning_explanation)
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

            triage_prompt = f"""You are an expert biological reasoning mode selector. Analyze the user's question and select the top {num_choices} most appropriate reasoning modes.

Available reasoning modes:
{chr(10).join(modes_info)}

User Question: "{query}"
Additional Context: "{context}"

Respond in JSON format with an array of the top {num_choices} candidates:
{{
    "candidates": [
        {{
            "mode": "mode_name",
            "confidence": 0.95,
            "reasoning": "Explanation of why this mode was selected."
        }},
        {{
            "mode": "mode_name",
            "confidence": 0.75,
            "reasoning": "Explanation of why this mode was selected."
        }}
    ]
}}

Each confidence should be between 0 and 1. Order candidates by confidence (highest first)."""

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
                "max_tokens": 800,
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
            candidates_data = parsed_response.get("candidates", [])
            
            candidates = []
            for candidate in candidates_data:
                mode = candidate.get("mode", "mechanistic").lower()
                confidence = float(candidate.get("confidence", 0.5))
                reasoning = candidate.get("reasoning", "LLM analysis completed")
                
                # Validate the selected mode
                if mode in self._modes:
                    candidates.append((mode, confidence, reasoning))
            
            # If we got valid candidates, return them
            if candidates:
                return candidates
            
            # If no valid candidates, fall back to single mode format
            if "selected_mode" in parsed_response:
                selected_mode = parsed_response.get("selected_mode", "mechanistic").lower()
                confidence = float(parsed_response.get("confidence", 0.5))
                reasoning = parsed_response.get("reasoning", "LLM analysis completed")
                
                if selected_mode in self._modes:
                    return [(selected_mode, confidence, reasoning)]

        except Exception as e:
            logger.warning(f"LLM triage failed: {str(e)}")

        # Fallback to keyword-based triage
        keyword_rankings = self._triage_keyword_multiple(query, context)
        fallback_candidates = []
        for mode, confidence in keyword_rankings[:num_choices]:
            fallback_candidates.append((
                mode,
                confidence * 0.5,  # Reduce confidence for fallback
                f"LLM triage failed, used keyword fallback"
            ))
        
        return fallback_candidates if fallback_candidates else [("mechanistic", 0.1, "Complete fallback")]


# Create a global registry instance
registry = ReasoningModeRegistry()


# Convenience functions that use the global registry
def create_reasoning_mode(mode_name: str, user_query: Optional[str] = None) -> ReasoningMode:
    """Create a reasoning mode instance using the global registry."""
    return registry.create_mode(mode_name, user_query)


def get_available_modes() -> list[str]:
    """Get list of available reasoning mode names."""
    return list(registry.get_available_modes().keys())


def triage_reasoning_mode(
    query: str,
    context: str = "",
    threshold: float = None,
    num_choices: int = 2
):
    """
    Triage to select reasoning mode(s).
    
    Args:
        query: User's question or task description
        context: Additional context information
        threshold: If provided, returns multiple candidates above this threshold
        num_choices: Maximum number of candidates when threshold is used
    
    Returns:
        If threshold is None: str (single mode name)
        If threshold is provided: List[Tuple[str, float, str]] (multiple candidates)
    """
    result = registry.triage(query, context, threshold, num_choices)
    if threshold is None:
        # Return just the mode name for backward compatibility
        return result[0]
    else:
        # Return the full list of candidates
        return result


def triage_with_confidence(
    query: str,
    context: str = "",
    threshold: float = None,
    num_choices: int = 2
):
    """
    Triage with confidence score(s).
    
    Args:
        query: User's question or task description
        context: Additional context information
        threshold: If provided, returns multiple candidates above this threshold
        num_choices: Maximum number of candidates when threshold is used
    
    Returns:
        If threshold is None: Tuple[str, float] (mode, confidence)
        If threshold is provided: List[Tuple[str, float, str]] (multiple candidates)
    """
    result = registry.triage(query, context, threshold, num_choices)
    if threshold is None:
        # Return mode and confidence for backward compatibility
        return result[0], result[1]
    else:
        # Return the full list of candidates
        return result


def get_mode_info(mode_name: str) -> Dict[str, any]:
    """Get information about a reasoning mode."""
    return registry.get_mode_info(mode_name)


if __name__ == "__main__":
    # Demo the simplified registry
    print("🧬 Simplified Bio-Reasoning Registry Demo")
    print("=" * 50)

    # Test single triage
    query = "How did natural selection shape bird flight evolution?"
    mode, confidence, reasoning = registry.triage(query)
    print(f"Query: {query}")
    print(f"Selected Mode: {mode}")
    print(f"Confidence: {confidence:.2f}")
    print(f"Reasoning: {reasoning}")
    print()

    # Test multiple triage
    print("Multiple Candidate Triage:")
    candidates = triage_reasoning_mode(query, threshold=0.2, num_choices=3)
    for i, (mode, conf, reason) in enumerate(candidates, 1):
        print(f"  {i}. {mode} (confidence: {conf:.2f}) - {reason}")
    print()

    # Test mode creation
    reasoning_mode = create_reasoning_mode(mode)
    print(f"Created mode: {reasoning_mode.name}")

    # Test available modes
    print(f"Available modes: {len(get_available_modes())}")
    print(f"Modes: {', '.join(get_available_modes())}")
    print("Registry successfully initialized!")