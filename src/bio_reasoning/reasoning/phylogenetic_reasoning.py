import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class PhylogeneticReasoningMode(ReasoningMode):
    """
    Phylogenetic reasoning mode for evolutionary analysis and tree construction.
    Focuses on homologous sequences, phylogenetic trees, and evolutionary relationships.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Phylogenetic")
        layer_b = ToolRegistry(name="Layer B - Phylogenetic")
        layer_c = ToolRegistry(name="Layer C - Phylogenetic")

        system_prompt = (
            "You are a Phylogenetic Reasoning Expert. "
            "Given the user's question and any provided sequence or species data, your task is to:\n"
            "1. Gather homologous sequences or taxa relevant to the query.\n"
            "2. Perform multiple sequence alignment or retrieve an existing alignment.\n"
            "3. Construct or retrieve a phylogenetic tree.\n"
            "4. Interpret branching order, clade support, and divergence times to answer why and how the trait or gene evolved.\n"
            "5. Clearly explain which species share common ancestry and what that implies for the user's question."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in phylogenetics and evolutionary biology. Provide detailed analysis of evolutionary relationships and phylogenetic data.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for phylogenetic analysis
        # Examples: sequence alignment tools, phylogenetic tree construction, molecular clock analysis

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for phylogenetic analysis
        # Examples: NCBI databases, phylogenetic databases, sequence repositories

        # Define keywords for this reasoning mode
        keywords = [
            "phylogeny", "phylogenetic", "evolution", "evolutionary", "tree", "clade", "ancestor",
            "ancestral", "divergence", "speciation", "homolog", "ortholog", "paralog", "sequence alignment",
            "molecular clock", "common ancestor", "branching", "monophyletic", "paraphyletic"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Phylogenetic Reasoning Expert",
            description="Analyzes evolutionary relationships, phylogenetic trees, and ancestral connections",
            keywords=keywords,
            name_canonical="phylogenetic",
        )


if __name__ == "__main__":
    phylogenetic_reasoning = PhylogeneticReasoningMode()
    print(phylogenetic_reasoning.layers)
