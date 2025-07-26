import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class MechanisticReasoningMode(ReasoningMode):
    """
    Mechanistic reasoning mode for molecular and cellular mechanism analysis.
    Focuses on causal chains, molecular interactions, and step-by-step processes.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Mechanistic")
        layer_b = ToolRegistry(name="Layer B - Mechanistic")
        layer_c = ToolRegistry(name="Layer C - Mechanistic")

        system_prompt = (
            "You are a Mechanistic Reasoning Expert. "
            "Given the user's question and relevant molecular or cellular entities, your task is to:\n"
            "1. Decompose the phenomenon into its component molecules, interactions, or steps.\n"
            "2. Map out the causal chain (e.g., receptor → signal transduction → effector).\n"
            "3. Describe each step in detail, citing known reactions, structures, or regulatory mechanisms.\n"
            "4. Conclude by synthesizing how these steps produce the observed outcome."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in molecular and cellular biology. Provide detailed mechanistic explanations of biological processes at the molecular level.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for mechanistic analysis
        # Examples: molecular structure analysis, pathway modeling, protein interaction prediction

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for mechanistic analysis
        # Examples: PDB, UniProt, KEGG pathways, Reactome

        # Define keywords for this reasoning mode
        keywords = [
            "mechanism", "molecular", "pathway", "signaling", "cascade", "interaction", "binding",
            "enzyme", "protein", "gene expression", "regulation", "transcription", "translation",
            "how does", "step by step", "process", "causal chain", "biochemical"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Mechanistic Reasoning Expert",
            description="Investigates molecular mechanisms, pathways, and step-by-step processes",
            keywords=keywords,
            name_canonical="mechanistic",
        )


if __name__ == "__main__":
    mechanistic_reasoning = MechanisticReasoningMode()
    print(mechanistic_reasoning.layers)
