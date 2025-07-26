from typing import List, Optional

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
        name: str = "Generic Reasoning Mode",
        description: str = "",
        keywords: Optional[List[str]] = None,
        name_canonical: Optional[str] = None,
    ):
        self.sys_prompt = sys_prompt
        self.name = name
        self.description = (
            description or f"Specialized biological reasoning for {name.lower()}"
        )
        self.layer_a = layer_a
        self.layer_b = layer_b
        self.layer_c = layer_c
        self.keywords = keywords or []
        self.name_canonical = name_canonical or name.lower().replace(" ", "_")

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

    def describe(self) -> dict:
        """
        Provide comprehensive information about this reasoning mode.

        Returns:
            Dictionary containing mode information including name, description,
            keywords, system prompt, and other metadata.
        """
        return {
            "name": self.name,
            "canonical_name": self.name_canonical,
            "description": self.description,
            "keywords": self.keywords,
            "system_prompt": self.sys_prompt,
            "layer_count": 3,  # Always has 3 layers (A, B, C)
            "tools_available": len(self.layers.tools)
            if hasattr(self.layers, "tools")
            else 0,
        }

    def __repr__(self) -> str:
        """String representation of the reasoning mode."""
        return f"ReasoningMode(name='{self.name}', canonical='{self.name_canonical}', keywords={len(self.keywords)})"
