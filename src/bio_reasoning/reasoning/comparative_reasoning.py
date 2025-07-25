import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class ComparativeReasoningMode(ReasoningMode):
    """
    Comparative reasoning mode for cross-species analysis and evolutionary comparisons.
    Focuses on comparative biology, model organisms, and evolutionary conservation.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Comparative")
        layer_b = ToolRegistry(name="Layer B - Comparative")
        layer_c = ToolRegistry(name="Layer C - Comparative")

        system_prompt = (
            "You are a Comparative Biology Reasoning Expert. "
            "Given the user's question and any cross-species data, your task is to:\n"
            "1. Identify relevant model organisms or systems analogous to the one under study.\n"
            "2. Map homologous or analogous features (genes, structures, behaviors) between species.\n"
            "3. Draw inferences or generate hypotheses by analogy, noting conserved versus divergent aspects.\n"
            "4. Cite comparative studies that support or refine the analogy."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in comparative biology and evolutionary analysis. Provide detailed analysis of cross-species comparisons and evolutionary relationships.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for comparative analysis
        # Examples: comparative genomics, ortholog prediction, evolutionary analysis

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for comparative analysis
        # Examples: comparative databases, model organism databases, ortholog databases

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Comparative Biology Reasoning Expert",
        )


if __name__ == "__main__":
    comparative_reasoning = ComparativeReasoningMode()
    print(comparative_reasoning.layers)
