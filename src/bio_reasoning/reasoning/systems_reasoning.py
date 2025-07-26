import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class SystemsReasoningMode(ReasoningMode):
    """
    Systems biology reasoning mode for network analysis and emergent properties.
    Focuses on biological networks, feedback loops, and system-level behaviors.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Systems")
        layer_b = ToolRegistry(name="Layer B - Systems")
        layer_c = ToolRegistry(name="Layer C - Systems")

        system_prompt = (
            "You are a Systems Biology Reasoning Expert. "
            "Given the user's question and any network or multi-omic data, your task is to:\n"
            "1. Identify the network components (genes, proteins, metabolites) and their interactions.\n"
            "2. Determine which feedback loops or network motifs drive the emergent behavior.\n"
            "3. If appropriate, simulate or qualitatively analyze dynamic behavior (e.g., oscillation, bistability).\n"
            "4. Explain how the system-level properties arise from the interplay of parts."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in systems biology and network analysis. Provide detailed analysis of biological networks and emergent system properties.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for systems biology analysis
        # Examples: network analysis tools, pathway simulation, multi-omics integration

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for systems biology
        # Examples: STRING database, BioCyc, KEGG, Reactome, omics databases

        # Define keywords for this reasoning mode
        keywords = [
            "network", "system", "systems biology", "emergent", "feedback", "loop", "circuit",
            "module", "motif", "topology", "connectivity", "robustness", "dynamics", "oscillation",
            "bistability", "multi-scale", "integration"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Systems Biology Reasoning Expert",
            description="Analyzes biological networks, emergent properties, and system-level behaviors",
            keywords=keywords,
            name_canonical="systems",
        )


if __name__ == "__main__":
    systems_reasoning = SystemsReasoningMode()
    print(systems_reasoning.layers)
