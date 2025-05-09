from typing import Dict, Any, Optional, List
import openai
from abc import ABC, abstractmethod
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
    SYSTEM_MESSAGES,
)
from bio_reasoning.utils import call_model_with_retry
from .base import Layer


class SpecializedAnalyzer(ABC):
    """Abstract base class for different types of specialized analyzers.
    
    This is an internal implementation detail of LayerB and should not be exposed
    outside of this module.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name

    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze biological data using the specialized model."""
        pass


class GenomicSequenceAnalyzer(SpecializedAnalyzer):
    """A specialized analyzer for genomic sequence analysis."""

    def analyze(self, sequence: str) -> Dict[str, Any]:
        """Analyze a genomic sequence."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["sequence_analysis"]},
            {"role": "user", "content": f"Analyze this sequence: {sequence}"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "sequence": sequence,
                "analysis": result["content"],
                "features": {
                    "length": len(sequence),
                    "gc_content": self._calculate_gc_content(sequence),
                },
            }
        else:
            print(f"Error analyzing sequence: {result['content']}")
            return {}

    def _calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content of a sequence."""
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return gc_count / len(sequence) if sequence else 0.0


class ImagingAnalyzer(SpecializedAnalyzer):
    """A specialized analyzer for biological image analysis."""

    def analyze(self, image_data: Any) -> Dict[str, Any]:
        """Analyze biological images."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["image_analysis"]},
            {"role": "user", "content": "Analyze this biological image"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "analysis": result["content"],
                "features": {"image_type": "biological", "analysis_type": "simulated"},
            }
        else:
            print(f"Error analyzing image: {result['content']}")
            return {}


class LayerB(Layer):
    """Layer B: Specialized biological analysis models.
    
    This layer manages multiple specialized analyzers internally and provides a unified
    interface for biological data analysis.
    """

    def __init__(self, name: str, model_name: str = MODEL_NAME):
        super().__init__(name)
        self.model_name = model_name
        self._analyzers: List[SpecializedAnalyzer] = []

    def add_analyzer(self, analyzer: SpecializedAnalyzer) -> None:
        """Add a new analyzer to the layer."""
        self._analyzers.append(analyzer)

    def prepare_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare the input for analysis."""
        return {
            "query": query,
            "context": context or {},
            "model_name": self.model_name
        }

    def execute(self, prepared_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute analysis using all registered analyzers."""
        try:
            # Run analysis through all analyzers
            all_analyses = {}
            for analyzer in self._analyzers:
                result = analyzer.analyze(prepared_input["query"])
                if result:
                    analyzer_name = analyzer.__class__.__name__.lower()
                    all_analyses[analyzer_name] = result

            # Instead of making another API call, synthesize the results
            synthesis = "Analysis results:\n"
            for analyzer_name, result in all_analyses.items():
                synthesis += f"\n{analyzer_name}:\n{result.get('analysis', 'No analysis available')}\n"

            return {
                "query": prepared_input["query"],
                "processed_query": synthesis,
                "analyses": all_analyses,
            }
        except Exception as e:
            print(f"Error performing analysis: {e}")
            return {}

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the analysis output."""
        return isinstance(output, dict) and "query" in output and "processed_query" in output

    def format_results(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Format the analysis results."""
        return {
            "query": output["query"],
            "processed_query": output["processed_query"],
            "analyses": output["analyses"],
            "source": self.name
        }
