import os

from dotenv import load_dotenv
from toolregistry import ToolRegistry
from toolregistry.hub import WebSearchGoogle

from ..layers.a.parametric_memory import parametric_memory_factory
from ..layers.b import visual_describer_factory
from .basics import ReasoningMode


class ExampleReasoningMode(ReasoningMode):
    """
    An example of a specific reasoning mode that might use certain tools. Show case the process of building a reasoning mode. We essentially need to define the tools for each layers, and the system prompt.
    """

    def __init__(self):
        # `name` is necessary to avoid name collisions and to coincide with the system prompt.
        layer_a = ToolRegistry(name="Layer A")
        layer_b = ToolRegistry(name="Layer B")
        layer_c = ToolRegistry(name="Layer C")
        system_prompt = (
            # this is just an example. It could really be anything. The prompts.py file has some prompts defined in the previous implementation. We can fix and migrate them here.
            "In example reasoning mode, you are provided with a collections of tools. Tools are labeled with a prefix from layer_a, layer_b, or layer_c. "
            "Layer A is the parametric memory of a general large language model (LLM). "
            "Layer B provides access to a visual describer model. "
            "Layer C provides access to Google Web Search. "
        )

        # Load environment variables from .env file, useful to the following factories. You can hardcode the values if you want to avoid this step, but highly not recommended.
        load_dotenv()

        # ============ define layer a ============
        # layer A is the parametric memory of a general large language model (LLM), capturing broadly applicable knowledge pre-trained or fine-tuned into its weights.
        parametric_memory = parametric_memory_factory(
            api_key=os.getenv("API_KEY", "default_api_key"),
            api_base_url=os.getenv("BASE_URL", "https://default-base-url.com"),
            model_name=os.getenv("MODEL_NAME", "default_model_name"),
            system_prompt="You are an expert in biology. You are given a question and you need to answer it with the best of your knowledge.",
        )

        # bind the tool to the layer. You should call this method for each tool you want to register.
        layer_a.register(parametric_memory)

        # ============ define layer b ============
        # layer B is about specialized models. Visual describer is an example of a specialized model.
        system_prompt = "You are professional biologist with specialty in image analysis. Please describe the image in detail."

        visual_describer = visual_describer_factory(
            api_key=os.getenv("API_KEY", "sk-xxxxxx"),
            api_base_url=os.getenv("BASE_URL", "https://api.openai.com/v1"),
            model_name=os.getenv("MODEL_NAME", "gpt-4.1-mini"),
            system_prompt=system_prompt,
        )

        layer_b.register(visual_describer)

        # ============ define layer c ============
        # layer C is about external data sources. Web search is an example of an external data source.

        # toolregistry.hub provides a small curated list of tools. We use the web search tool from there.
        layer_c.register_from_class(WebSearchGoogle())

        # ============ define the reasoning mode ============
        # use keyword arguments to pass the layers to the reasoning mode, instead of positional arguments, to avoid mistakes.
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt,
        )


if __name__ == "__main__":
    teleonomic_reasoning = ExampleReasoningMode()
    print(teleonomic_reasoning.layers)
