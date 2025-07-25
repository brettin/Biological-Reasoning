import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class SpatialReasoningMode(ReasoningMode):
    """
    Spatial reasoning mode for analyzing spatial patterns and geometric relationships.
    Focuses on spatial organization, localization, and geometric constraints in biology.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Spatial")
        layer_b = ToolRegistry(name="Layer B - Spatial")
        layer_c = ToolRegistry(name="Layer C - Spatial")

        system_prompt = (
            "You are a Spatial Reasoning Expert. "
            "Given the user's question and any images, structures, or spatial patterns, your task is to:\n"
            "1. Identify the relevant spatial scale (molecular, cellular, tissue, ecological).\n"
            "2. Explain how geometry, localization, or diffusion shape the phenomenon.\n"
            "3. If provided an image or 3D structure, describe key spatial features and their functional roles.\n"
            "4. Relate spatial organization to the user's specific question."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in spatial biology and structural analysis. Provide detailed analysis of spatial patterns and geometric relationships in biological systems.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for spatial analysis
        # Examples: image analysis, 3D structure analysis, spatial pattern recognition

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for spatial analysis
        # Examples: PDB, microscopy databases, spatial omics databases

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Spatial Reasoning Expert",
        )


if __name__ == "__main__":
    spatial_reasoning = SpatialReasoningMode()
    print(spatial_reasoning.layers)
