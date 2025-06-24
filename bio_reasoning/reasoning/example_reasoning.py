import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry
from toolregistry.hub import WebSearchGoogle

from ..layers.a.parametric_memory import parametric_memory_factory
from ..layers.b import visual_describer_factory
from .basics import ReasoningMode


class ExampleReasoningMode(ReasoningMode):
    """
    An example of a specific reasoning mode that might use certain tools.
    """

    def __init__(self):
        layer_a = ToolRegistry(name="Layer A")
        layer_b = ToolRegistry(name="Layer B")
        layer_c = ToolRegistry(name="Layer C")

        load_dotenv()

        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY"),
            api_base_url=os.getenv("BASE_URL"),
            model_name=os.getenv("MODEL_NAME"),
            system_prompt="You are an expert in biology. You are given a question and you need to answer it with the best of your knowledge.",
        )
        layer_a.register(parametric_memory)
        # register layer B tools
        system_prompt = "You are professional biologist with specialty in image analysis. Please describe the image in detail."

        visual_describer = visual_describer_factory(
            api_key=os.getenv("API_KEY"),
            api_base_url=os.getenv("BASE_URL"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
            system_prompt=system_prompt,
        )

        layer_b.register(visual_describer)

        # register layer C tools
        layer_c.register_from_class(WebSearchGoogle())

        super().__init__(layer_a, layer_b, layer_c)


if __name__ == "__main__":
    teleonomic_reasoning = ExampleReasoningMode()
    print(teleonomic_reasoning.layers)
