import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class HomeostaticReasoningMode(ReasoningMode):
    """
    Homeostatic reasoning mode for analyzing regulatory mechanisms and feedback control.
    Focuses on physiological regulation, feedback loops, and homeostatic maintenance.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Homeostatic")
        layer_b = ToolRegistry(name="Layer B - Homeostatic")
        layer_c = ToolRegistry(name="Layer C - Homeostatic")

        system_prompt = (
            "You are a Homeostatic Reasoning Expert. "
            "Given the user's question and any physiological variables, your task is to:\n"
            "1. Identify the controlled variable and its setpoint or normal range.\n"
            "2. Describe the sensors, control centers, and effectors that form the feedback loop.\n"
            "3. Explain how negative (or positive) feedback maintains stability.\n"
            "4. Discuss what happens when the loop fails or is perturbed."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in physiology and homeostatic regulation. Provide detailed analysis of regulatory mechanisms and feedback control systems.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for homeostatic analysis
        # Examples: control system modeling, feedback analysis, physiological simulation

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for homeostatic analysis
        # Examples: physiological databases, regulatory pathway databases, clinical data

        # Define keywords for this reasoning mode
        keywords = [
            "homeostasis", "regulation", "control", "feedback", "setpoint", "maintain", "stability",
            "physiological", "sensor", "effector", "negative feedback", "positive feedback",
            "equilibrium", "steady state", "perturbation"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Homeostatic Reasoning Expert",
            description="Analyzes regulatory mechanisms, feedback control, and physiological stability",
            keywords=keywords,
            name_canonical="homeostatic",
        )


if __name__ == "__main__":
    homeostatic_reasoning = HomeostaticReasoningMode()
    print(homeostatic_reasoning.layers)
