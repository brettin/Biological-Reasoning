from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
import openai
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
    SYSTEM_MESSAGES,
    REASONING_MODES,
)
from bio_reasoning.utils import call_model_with_retry
from bio_reasoning.layers.layer_a import LayerA, InMemoryKnowledgeStore
from bio_reasoning.layers.layer_b import LayerB, GenomicSequenceAnalyzer, ImagingAnalyzer
from bio_reasoning.layers.layer_c import LayerC, OpenTargetsRepository, PubMedRepository, BioRxivRepository

class ReasoningMode(ABC):
    """Abstract base class for biological reasoning modes."""
    
    def __init__(self):
        # Initialize Layer A
        self.layer_a = LayerA("BiologicalKnowledgeStore")
        self.layer_a.add_knowledge_store(InMemoryKnowledgeStore())

        # Initialize Layer B
        self.layer_b = LayerB("SpecializedAnalysis")
        self.layer_b.add_analyzer(GenomicSequenceAnalyzer())
        self.layer_b.add_analyzer(ImagingAnalyzer())

        # Initialize Layer C
        self.layer_c = LayerC("InformationSynthesis")
        self.layer_c.add_repository(OpenTargetsRepository())
        self.layer_c.add_repository(PubMedRepository())
        self.layer_c.add_repository(BioRxivRepository())
    
    @abstractmethod
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a biological query using this reasoning mode."""
        pass

    def get_prompt(self, query: str, data: str = "") -> str:
        """Get the reasoning prompt for this mode."""
        mode_name = self.__class__.__name__.lower().replace("reasoning", "")
        return REASONING_PROMPTS[mode_name].format(question=query, data=data)

class PhylogeneticReasoning(ReasoningMode):
    """Reasoning based on evolutionary relationships."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process phylogenetic reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Analyze sequences using Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get evolutionary data from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} phylogenetic analysis")
        )
        
        return {
            "reasoning_mode": "phylogenetic",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class TeleonomicReasoning(ReasoningMode):
    """Reasoning based on function and purpose."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process teleonomic reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get functional data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} function")
        )
        
        return {
            "reasoning_mode": "teleonomic",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class MechanisticReasoning(ReasoningMode):
    """Reasoning based on causal mechanisms."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process mechanistic reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get mechanistic data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} mechanism")
        )
        
        return {
            "reasoning_mode": "mechanistic",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class TradeoffReasoning(ReasoningMode):
    """Reasoning based on biological trade-offs."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process trade-off reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get trade-off data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} trade-off")
        )
        
        return {
            "reasoning_mode": "tradeoff",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class SystemsReasoning(ReasoningMode):
    """Reasoning based on systems biology principles."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process systems biology reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get systems data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} systems biology")
        )
        
        return {
            "reasoning_mode": "systems",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class SpatialReasoning(ReasoningMode):
    """Reasoning based on spatial organization."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process spatial reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get spatial data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} spatial")
        )
        
        return {
            "reasoning_mode": "spatial",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class TemporalReasoning(ReasoningMode):
    """Reasoning based on temporal dynamics."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process temporal reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get temporal data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} temporal dynamics")
        )
        
        return {
            "reasoning_mode": "temporal",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class HomeostaticReasoning(ReasoningMode):
    """Reasoning based on homeostasis and feedback loops."""
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process homeostatic reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get homeostatic data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} homeostasis")
        )
        
        return {
            "reasoning_mode": "homeostatic",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class DevelopmentalReasoning(ReasoningMode):
    """Reasoning based on developmental biology."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform developmental reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get developmental data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} development")
        )
        
        return {
            "reasoning_mode": "developmental",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class ComparativeReasoning(ReasoningMode):
    """Reasoning based on comparative biology."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform comparative reasoning."""
        # Get basic knowledge from Layer A
        layer_a_result = self.layer_a.execute(self.layer_a.prepare_input(query))
        
        # Get comparative data from Layer B
        layer_b_result = self.layer_b.execute(self.layer_b.prepare_input(query))
        
        # Get supporting literature from Layer C
        layer_c_result = self.layer_c.execute(
            self.layer_c.prepare_input(f"{query} comparative")
        )
        
        return {
            "reasoning_mode": "comparative",
            "layer_a": layer_a_result,
            "layer_b": layer_b_result,
            "layer_c": layer_c_result,
        }

class ReasoningModeSelector:
    """Selects the appropriate reasoning mode for a biological query."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._initialize_model()
        self._initialize_layers()

    def _initialize_model(self):
        """Initialize the model connection."""
        self.client = openai.OpenAI(base_url=MODEL_BASE_URL, api_key=MODEL_API_KEY)

    def _initialize_layers(self):
        """Initialize the layers needed for reasoning."""
        # Initialize Layer A
        self.layer_a = LayerA("BiologicalKnowledgeStore")
        self.layer_a.add_knowledge_store(InMemoryKnowledgeStore())

        # Initialize Layer B
        self.layer_b = LayerB("SpecializedAnalysis")
        self.layer_b.add_analyzer(GenomicSequenceAnalyzer())
        self.layer_b.add_analyzer(ImagingAnalyzer())

        # Initialize Layer C
        self.layer_c = LayerC("IntegrationLayer")
        self.layer_c.add_repository(OpenTargetsRepository())
        self.layer_c.add_repository(PubMedRepository())
        self.layer_c.add_repository(BioRxivRepository())

    def select_mode(self, query: str) -> str:
        """Select the most appropriate reasoning mode for a query."""
        try:
            # Format the available modes with their descriptions
            mode_descriptions = []
            for mode, desc in REASONING_MODES.items():
                mode_descriptions.append(f"- {mode}: {desc}")

            messages = [
                {"role": "system", "content": SYSTEM_MESSAGES["reasoning_mode"]},
                {
                    "role": "user",
                    "content": f"Query: {query}\n\nAvailable modes with descriptions:\n"
                    + "\n".join(mode_descriptions)
                    + "\n\nRemember to respond with ONLY the mode name, nothing else.",
                },
            ]
            print(f"Messages: {messages}")
            print(f"Using model: {self.model_name}")
            print(f"Using base URL: {self.client.base_url}")
            print(f"Using API key: {self.client.api_key[:4]}...")  # Only show first 4 chars of API key
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            response_text = response.choices[0].message.content.strip().lower()
            print(f"Raw response: {response_text}")

            # Check if the response is exactly one of the valid modes
            if response_text in REASONING_MODES:
                return response_text
            else:
                print(f"Could not find {response_text} in {REASONING_MODES}")
                print("Returning teleonomic")
                return "teleonomic"
        except Exception as e:
            print(f"Error determining reasoning mode: {e}")
            import traceback
            traceback.print_exc()
            return "teleonomic"

# Additional reasoning modes can be added here following the same pattern 
# 