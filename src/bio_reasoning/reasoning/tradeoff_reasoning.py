import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class TradeoffReasoningMode(ReasoningMode):
    """
    Trade-off reasoning mode for analyzing competing biological traits and resource allocation.
    Focuses on cost-benefit analysis, resource allocation, and evolutionary trade-offs.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Tradeoff")
        layer_b = ToolRegistry(name="Layer B - Tradeoff")
        layer_c = ToolRegistry(name="Layer C - Tradeoff")

        system_prompt = (
            "You are a Trade-off Reasoning Expert. "
            "Given the user's question and any quantitative or qualitative data, your task is to:\n"
            "1. Identify the two (or more) competing biological traits or functions.\n"
            "2. Describe how resources (energy, time, materials) are allocated between them.\n"
            "3. If data are available, quantify the relationship (e.g., correlation, cost-benefit curve).\n"
            "4. Explain why an optimal intermediate balance exists, and discuss evolutionary or physiological implications."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in evolutionary trade-offs and resource allocation. Provide detailed analysis of competing biological traits and their optimization.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for trade-off analysis
        # Examples: optimization modeling, cost-benefit analysis, resource allocation simulation

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for trade-off analysis
        # Examples: life history databases, physiological data, evolutionary ecology literature

        # Define keywords for this reasoning mode
        keywords = [
            "tradeoff", "trade-off", "cost", "benefit", "allocation", "resource", "constraint",
            "optimization", "balance", "competing", "conflict", "compromise", "energy budget",
            "life history", "pareto", "optimal"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Trade-off Reasoning Expert",
            description="Studies competing biological traits, resource allocation, and optimization",
            keywords=keywords,
            name_canonical="tradeoff",
        )


if __name__ == "__main__":
    tradeoff_reasoning = TradeoffReasoningMode()
    print(tradeoff_reasoning.layers)
