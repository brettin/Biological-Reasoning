import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class TemporalReasoningMode(ReasoningMode):
    """
    Temporal reasoning mode for analyzing time-dependent processes and dynamics.
    Focuses on temporal sequences, rates, and dynamic behaviors in biological systems.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Temporal")
        layer_b = ToolRegistry(name="Layer B - Temporal")
        layer_c = ToolRegistry(name="Layer C - Temporal")

        system_prompt = (
            "You are a Temporal Reasoning Expert. "
            "Given the user's question and any time-series data or process descriptions, your task is to:\n"
            "1. Identify the sequence of events, phases, or cycles involved.\n"
            "2. Quantify or describe rates, delays, and durations.\n"
            "3. If appropriate, model the dynamics (e.g., using ODEs or time-series analysis).\n"
            "4. Explain how timing and order produce the observed behavior or phenotype."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in temporal dynamics and biological processes. Provide detailed analysis of time-dependent biological phenomena and their dynamics.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for temporal analysis
        # Examples: time-series analysis, dynamic modeling, temporal pattern recognition

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for temporal analysis
        # Examples: time-course databases, circadian databases, developmental timing data

        # Define keywords for this reasoning mode
        keywords = [
            "time", "temporal", "dynamics", "kinetics", "rate", "timing", "sequence", "order",
            "phase", "cycle", "rhythm", "circadian", "oscillation", "delay", "duration",
            "time course", "chronology", "development over time"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Temporal Reasoning Expert",
            description="Studies time-dependent processes, dynamics, and temporal sequences",
            keywords=keywords,
            name_canonical="temporal",
        )


if __name__ == "__main__":
    temporal_reasoning = TemporalReasoningMode()
    print(temporal_reasoning.layers)
