import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class TeleonomicReasoningMode(ReasoningMode):
    """
    Teleonomic (adaptive-function) reasoning mode for analyzing biological functions.
    Focuses on fitness advantages, adaptive explanations, and evolutionary functions.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Teleonomic")
        layer_b = ToolRegistry(name="Layer B - Teleonomic")
        layer_c = ToolRegistry(name="Layer C - Teleonomic")

        system_prompt = (
            "You are an Adaptive-Function (Teleonomic) Reasoning Expert. "
            "Given the user's question and the trait or organism in question, your task is to:\n"
            "1. Identify the biological feature and hypothesize its function in terms of fitness advantage.\n"
            "2. Draw on known case studies or analogous adaptations to frame a plausible 'in-order-to' explanation.\n"
            "3. Cite evidence (literature or databases) supporting that the trait enhances survival or reproduction.\n"
            "4. Note any alternative hypotheses or trade-offs that might challenge the adaptive explanation."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in evolutionary biology and adaptive functions. Provide detailed analysis of biological traits and their adaptive significance.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for teleonomic analysis
        # Examples: fitness modeling, comparative trait analysis, adaptation prediction

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for teleonomic analysis
        # Examples: trait databases, evolutionary literature, comparative genomics databases

        # Define keywords for this reasoning mode
        keywords = [
            "function",
            "adaptive",
            "adaptation",
            "fitness",
            "advantage",
            "benefit",
            "purpose",
            "survival",
            "reproduction",
            "natural selection",
            "selective pressure",
            "evolutionary advantage",
            "why evolved",
            "what for",
            "in order to",
            "functional significance",
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Teleonomic Reasoning Expert",
            description="Examines adaptive functions, fitness advantages, and evolutionary purposes",
            keywords=keywords,
            name_canonical="teleonomic",
        )


if __name__ == "__main__":
    teleonomic_reasoning = TeleonomicReasoningMode()
    print(teleonomic_reasoning.layers)
