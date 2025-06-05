import os
from cicada.core import MultiModalModel
from dotenv import load_dotenv
from toolregistry import ToolRegistry
from toolregistry.hub import WebSearchGoogle

from .layers.a import ParametricMemory
from .layers.b import VisualDescriber


class ReasoningMode:
    """
    Base class that encapsulate general reasoning mode elements and methods
    """

    def __init__(
        self, layer_a: ToolRegistry, layer_b: ToolRegistry, layer_c: ToolRegistry
    ):
        self._merged_layers = ToolRegistry()
        self._merged_layers.merge(layer_a)
        self._merged_layers.merge(layer_b)
        self._merged_layers.merge(layer_c)

    @property
    def layers(self) -> ToolRegistry:
        return self._merged_layers


class ExampleReasoningMode(ReasoningMode):
    """
    An example of a specific reasoning mode that might use certain tools.
    """

    def __init__(self):
        layer_a = ToolRegistry(name="Layer A")
        layer_b = ToolRegistry(name="Layer B")
        layer_c = ToolRegistry(name="Layer C")

        load_dotenv()
        # register layer A tools
        model = MultiModalModel(
            api_key=os.getenv("API_KEY"),
            api_base_url=os.getenv("BASE_URL"),
            model_name=os.getenv("MODEL_NAME"),
        )
        layer_a.register_from_class(
            ParametricMemory(
                model=model,
                system_prompt="You are an expert in biology. You are given a question and you need to answer it with the best of your knowledge.",
            )
        )
        # register layer B tools
        system_prompt = "You are professional biologist with specialty in image analysis. Please describe the image in detail."

        layer_b.register_from_class(
            VisualDescriber(model=model, system_prompt=system_prompt)
        )

        # register layer C tools
        layer_c.register_from_class(WebSearchGoogle())

        super().__init__(layer_a, layer_b, layer_c)


if __name__ == "__main__":
    teleonomic_reasoning = ExampleReasoningMode()
    print(teleonomic_reasoning.layers)
