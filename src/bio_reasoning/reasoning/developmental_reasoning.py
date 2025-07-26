import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class DevelopmentalReasoningMode(ReasoningMode):
    """
    Developmental reasoning mode for analyzing developmental processes and morphogenesis.
    Focuses on developmental sequences, gene regulation, and tissue formation.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Developmental")
        layer_b = ToolRegistry(name="Layer B - Developmental")
        layer_c = ToolRegistry(name="Layer C - Developmental")

        system_prompt = (
            "You are a Developmental Biology Reasoning Expert. "
            "Given the user's question and any gene-expression or lineage data, your task is to:\n"
            "1. Trace the sequence of developmental events (induction, differentiation, morphogenesis).\n"
            "2. Identify key regulatory genes or signals and their spatial-temporal expression.\n"
            "3. Explain how cell-cell interactions and gradients drive tissue formation.\n"
            "4. Relate these processes to the question (e.g., mutant phenotype, organogenesis)."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in developmental biology and morphogenesis. Provide detailed analysis of developmental processes and gene regulatory networks.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for developmental analysis
        # Examples: gene expression analysis, lineage tracing, morphogenesis modeling

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for developmental analysis
        # Examples: developmental databases, gene expression atlases, model organism databases

        # Define keywords for this reasoning mode
        keywords = [
            "development",
            "developmental",
            "embryo",
            "morphogenesis",
            "differentiation",
            "induction",
            "lineage",
            "fate",
            "specification",
            "determination",
            "organogenesis",
            "gastrulation",
            "neurulation",
            "segmentation",
            "axis formation",
            "gene regulatory network",
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Developmental Biology Reasoning Expert",
            keywords=keywords,
            name_canonical="developmental",
        )


if __name__ == "__main__":
    developmental_reasoning = DevelopmentalReasoningMode()
    print(developmental_reasoning.layers)
