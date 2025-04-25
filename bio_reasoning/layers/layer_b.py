from typing import Dict, Any, Optional
import openai
from abc import ABC, abstractmethod
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
    SYSTEM_MESSAGES,
)


class SpecializedModel(ABC):
    """Base class for specialized biological analysis models."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the model connection."""
        # Configure the client to use the local model endpoint
        print("Initializing SpecializedModel connection in layer_b with {MODEL_BASE_URL}, {MODEL_API_KEY}, {MODEL_NAME}")
        self.client = openai.OpenAI(
            base_url=MODEL_BASE_URL,
            api_key=MODEL_API_KEY)

    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze biological data using the specialized model."""
        pass


class GenomicSequenceAnalyzer(SpecializedModel):
    """Specialized model for genomic sequence analysis."""

    def analyze(self, sequence: str) -> Dict[str, Any]:
        """Analyze a genomic sequence."""
        try:
            # In a real implementation, this would use specialized sequence analysis algorithms
            # For now, we'll use the language model to simulate analysis
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGES["sequence_analysis"]},
                    {"role": "user", "content": f"Analyze this sequence: {sequence}"},
                ],
            )

            return {
                "sequence": sequence,
                "analysis": response.choices[0].message.content,
                "features": {
                    "length": len(sequence),
                    "gc_content": self._calculate_gc_content(sequence),
                },
            }
        except Exception as e:
            print(f"Error analyzing sequence: {e}")
            return {}

    def _calculate_gc_content(self, sequence: str) -> float:
        """Calculate GC content of a sequence."""
        gc_count = sequence.upper().count("G") + sequence.upper().count("C")
        return gc_count / len(sequence) if sequence else 0.0


class ImagingAnalyzer(SpecializedModel):
    """Specialized model for biological image analysis."""

    def analyze(self, image_data: Any) -> Dict[str, Any]:
        """Analyze biological images."""
        try:
            # In a real implementation, this would use computer vision algorithms
            # For now, we'll use the language model to simulate analysis
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGES["image_analysis"]},
                    {"role": "user", "content": "Analyze this biological image"},
                ],
            )

            return {
                "analysis": response.choices[0].message.content,
                "features": {"image_type": "biological", "analysis_type": "simulated"},
            }
        except Exception as e:
            print(f"Error analyzing image: {e}")
            return {}
