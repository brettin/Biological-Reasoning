from typing import Dict, Any, Optional
import openai
from bio_reasoning.layers.layer_a import BiologicalKnowledgeStore
from bio_reasoning.layers.layer_b import GenomicSequenceAnalyzer, ImagingAnalyzer
from bio_reasoning.layers.layer_c import (
    TargetDiseaseRepository,
    ProteinFunctionRepository,
    PubMedRepository,
    BioRxivRepository,
)
from bio_reasoning.reasoning.reasoning_modes import (
    PhylogeneticReasoning,
    TeleonomicReasoning,
    MechanisticReasoning,
)
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
    SYSTEM_MESSAGES,
    REASONING_MODES,
)


class BiologicalReasoningCoordinator:
    """Main coordinator for the biological reasoning system."""

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._initialize_components()
        self._initialize_model()

    def _initialize_components(self):
        """Initialize all system components."""
        self.layer_a = BiologicalKnowledgeStore()
        self.layer_b_genomic = GenomicSequenceAnalyzer()
        self.layer_b_imaging = ImagingAnalyzer()

        # Initialize repositories
        self.target_disease_repo = TargetDiseaseRepository()
        self.protein_function_repo = ProteinFunctionRepository()
        self.pubmed_repo = PubMedRepository()
        self.biorxiv_repo = BioRxivRepository()

        # Initialize reasoning modes
        self.reasoning_modes = {
            "phylogenetic": PhylogeneticReasoning(),
            "teleonomic": TeleonomicReasoning(),
            "mechanistic": MechanisticReasoning(),
        }

    def _initialize_model(self):
        """Initialize the language model connection."""
        # Configure the client to use the local model endpoint
        self.client = openai.OpenAI(base_url=MODEL_BASE_URL, api_key=MODEL_API_KEY)

    def determine_reasoning_mode(self, query: str) -> str:
        """Determine the most appropriate reasoning mode for a query."""
        try:
            # Format the available modes with their descriptions
            mode_descriptions = []
            for mode, desc in REASONING_MODES.items():
                if mode in self.reasoning_modes:
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
            print(
                f"Using API key: {self.client.api_key[:4]}..."
            )  # Only show first 4 chars of API key
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
            )
            response_text = response.choices[0].message.content.strip().lower()
            print(f"Raw response: {response_text}")

            # Check if the response is exactly one of the valid modes
            if response_text in self.reasoning_modes.keys():
                return response_text
            else:
                print(f"could not find {response_text} in {self.reasoning_modes}")
                print("Returning teleonomic")
                return "teleonomic"
        except Exception as e:
            print(f"Error determining reasoning mode: {e}")
            import traceback

            traceback.print_exc()
            return "teleonomic"

    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a biological query through the system."""
        try:
            # Determine the appropriate reasoning mode
            reasoning_mode = self.determine_reasoning_mode(query)

            # Get the reasoning mode instance
            reasoner = self.reasoning_modes[reasoning_mode]

            # Perform reasoning
            result = reasoner.reason(query)

            # Log the process
            self._log_process(query, reasoning_mode, result)

            return {"query": query, "reasoning_mode": reasoning_mode, "result": result}
        except Exception as e:
            print(f"Error processing query: {e}")
            return {"error": str(e), "query": query}

    def _log_process(self, query: str, reasoning_mode: str, result: Dict[str, Any]):
        """Log the reasoning process."""
        print(f"\nProcessing Query: {query}")
        print(f"Selected Reasoning Mode: {reasoning_mode}")
        # print(f"Result: {result}\n")
