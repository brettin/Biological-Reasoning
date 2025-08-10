from toolregistry import ToolRegistry


class ReasoningMode:
    """
    Base class that encapsulate general reasoning mode elements and methods
    """

    def __init__(
        self,
        *,
        layer_a: ToolRegistry,
        layer_b: ToolRegistry,
        layer_c: ToolRegistry,
        sys_prompt: str,
    ):
        self.sys_prompt = sys_prompt
        self.layer_a = layer_a
        self.layer_b = layer_b
        self.layer_c = layer_c

    @property
    def layers(self) -> ToolRegistry:
        """
        Present the merged layers as a single ToolRegistry instance.
        This allows the user to access all the tools in the reasoning mode.
        """
        _merged_layers = ToolRegistry()  # This is a single ToolRegistry instance that will hold all the tools from all the layers.
        _merged_layers.merge(self.layer_a)
        _merged_layers.merge(self.layer_b)
        _merged_layers.merge(self.layer_c)

        return _merged_layers
