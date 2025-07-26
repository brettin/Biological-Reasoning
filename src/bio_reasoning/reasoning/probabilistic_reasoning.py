import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry

from ..layers.a.parametric_memory import parametric_memory_factory
from .basics import ReasoningMode


class ProbabilisticReasoningMode(ReasoningMode):
    """
    Probabilistic reasoning mode for statistical analysis and uncertainty quantification.
    Focuses on biological variability, statistical modeling, and probabilistic inference.
    """

    def __init__(self):
        # Initialize tool registries for each layer
        layer_a = ToolRegistry(name="Layer A - Probabilistic")
        layer_b = ToolRegistry(name="Layer B - Probabilistic")
        layer_c = ToolRegistry(name="Layer C - Probabilistic")

        system_prompt = (
            "You are a Probabilistic Reasoning Expert. "
            "Given the user's question and relevant statistical or population data, your task is to:\n"
            "1. Identify sources of biological variability (e.g., mutation rates, stochastic gene expression).\n"
            "2. Formulate a probabilistic model (e.g., Bayesian network, Markov process) as needed.\n"
            "3. Calculate or retrieve probabilities, confidence intervals, or likelihoods relevant to the question.\n"
            "4. Interpret these probabilities to inform decision-making or prediction, and discuss uncertainty."
        )

        # Load environment variables
        load_dotenv()

        # ============ Layer A - Parametric Memory ============
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1"),
            system_prompt="You are an expert in biostatistics and probabilistic modeling. Provide detailed analysis of biological variability and statistical inference.",
        )
        layer_a.register(parametric_memory)

        # ============ Layer B - Specialized Models ============
        # TODO: Add specialized tools for probabilistic analysis
        # Examples: statistical modeling, Bayesian inference, uncertainty quantification

        # ============ Layer C - External Data Sources ============
        # TODO: Add external data sources for probabilistic analysis
        # Examples: population databases, statistical repositories, genomic variation databases

        # Define keywords for this reasoning mode
        keywords = [
            "probability", "statistical", "stochastic", "random", "variability", "uncertainty",
            "distribution", "bayesian", "likelihood", "confidence", "variance", "noise",
            "population", "frequency", "risk", "chance"
        ]

        # Initialize the reasoning mode
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
            name="Probabilistic Reasoning Expert",
            keywords=keywords,
            name_canonical="probabilistic",
        )


if __name__ == "__main__":
    probabilistic_reasoning = ProbabilisticReasoningMode()
    print(probabilistic_reasoning.layers)
