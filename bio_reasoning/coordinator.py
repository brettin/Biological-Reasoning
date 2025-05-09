from typing import Dict, Any, Optional
from bio_reasoning.layers.layer_a import LayerA, InMemoryKnowledgeStore
from bio_reasoning.layers.layer_b import LayerB, GenomicSequenceAnalyzer, ImagingAnalyzer
from bio_reasoning.layers.layer_c import (
    LayerC,
    OpenTargetsRepository,
    PubMedRepository,
    BioRxivRepository,
)
from bio_reasoning.reasoning.reasoning_modes import ReasoningModeSelector
from bio_reasoning.config import MODEL_NAME


class Coordinator:
    """Coordinates the execution of different layers in the biological reasoning system."""

    def __init__(self):
        # Initialize Layer A with knowledge store
        self.layer_a = LayerA("BiologicalKnowledgeStore")
        self.layer_a.add_knowledge_store(InMemoryKnowledgeStore())

        # Initialize Layer B with specialized analyzers
        self.layer_b = LayerB("SpecializedAnalysis")
        self.layer_b.add_analyzer(GenomicSequenceAnalyzer())
        self.layer_b.add_analyzer(ImagingAnalyzer())

        # Initialize Layer C with repositories
        self.layer_c = LayerC("IntegrationLayer")
        self.layer_c.add_repository(OpenTargetsRepository())
        self.layer_c.add_repository(PubMedRepository())
        self.layer_c.add_repository(BioRxivRepository())

        # Initialize reasoning mode selector
        self.reasoning_mode_selector = ReasoningModeSelector()

    def process_query(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a biological query through the system."""
        try:
            # Determine reasoning mode
            reasoning_mode = self.reasoning_mode_selector.select_mode(query)
            print(f"Selected reasoning mode: {reasoning_mode}")

            # Execute layers based on reasoning mode
            layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query, context))
            layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query, context))
            layer_c_result = self.layer_c.execute(self.layer_c.prepare_input(query, context))

            # Combine results
            return {
                "query": query,
                "reasoning_mode": reasoning_mode,
                "layer_a": layer_a_result,
                "layer_b": layer_b_result,
                "layer_c": layer_c_result,
            }
        except Exception as e:
            print(f"Error processing query: {e}")
            return {}
