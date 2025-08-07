"""
Toxicity Reasoning Mode

This reasoning mode is designed for molecular toxicity analysis using
Layer C external knowledge tools.
"""

import logging
from typing import Dict, Any

from toolregistry import ToolRegistry

from ..layers.a import parametric_memory_factory
from ..layers.c import (
    pubmed_search_factory,
    pubchem_search_factory,
    chembl_search_factory,
    toxcast_search_factory,
)
from .basics import ReasoningMode

# Set up logging
logger = logging.getLogger(__name__)


class ToxicityReasoningMode(ReasoningMode):
    """
    Reasoning mode for molecular toxicity analysis using external databases.
    
    This mode focuses on Layer C tools to gather comprehensive toxicity
    information from scientific literature and databases.
    """
    
    def __init__(self):
        """Initialize the toxicity reasoning mode with appropriate tools."""
        logger.info("🧬 Initializing ToxicityReasoningMode")
        
        # System prompt for toxicity analysis
        system_prompt = (
            "You are a Molecular Toxicity Analysis Expert. Your role is to analyze "
            "molecules for potential toxicity using BOTH your parametric knowledge AND external knowledge sources.\n\n"
            "Available tools:\n"
            "- Parametric Memory: Your general knowledge about molecular toxicity, chemical properties, and structure-activity relationships\n"
            "- PubMed Search: Search scientific literature for toxicity studies\n"
            "- PubChem Search: Get chemical properties and toxicity information\n"
            "- ChEMBL Search: Access bioactivity and toxicity data\n"
            "- ToxCast Search: EPA toxicity screening data\n\n"
            "When analyzing a molecule:\n"
            "1. FIRST, use your parametric memory to provide general insights about the molecule's structure, expected properties, and potential toxicity mechanisms\n"
            "2. THEN, search PubChem for specific chemical information and toxicity data\n"
            "3. Search PubMed for recent toxicity literature and mechanistic studies\n"
            "4. Check ChEMBL for bioactivity data and target interactions\n"
            "5. Search ToxCast for EPA screening results\n"
            "6. FINALLY, synthesize ALL findings (parametric + external) into a comprehensive toxicity assessment\n\n"
            "IMPORTANT: Always start with your parametric knowledge to establish a foundation, then enhance it with external data. "
            "Provide mechanistic insights when possible and cite your sources."
        )
        
        # Create tool registries for each layer
        layer_a = ToolRegistry()
        layer_b = ToolRegistry()  # Empty for now, will add Tx-Gemma later
        layer_c = ToolRegistry()
        
        # Register Layer A: Parametric Memory (using gpto3 model)
        logger.info("🔧 Registering Layer A tools (parametric memory)")
        parametric_memory = parametric_memory_factory(
            api_key="brettin",
            api_base_url="http://localhost:44497/v1",
            model_name="gpto3",
            system_prompt="You are an expert in molecular biology and toxicology. Provide accurate, scientific information about molecular toxicity, chemical properties, and structure-activity relationships."
        )
        layer_a.register(parametric_memory)
        
        # Register Layer C: External Knowledge Tools
        logger.info("🔧 Registering Layer C tools (external knowledge)")
        
        # PubMed literature search
        layer_c.register(pubmed_search_factory())
        
        # PubChem chemical database
        layer_c.register(pubchem_search_factory())
        
        # ChEMBL bioactivity database
        layer_c.register(chembl_search_factory())
        
        # ToxCast/Tox21 EPA database
        layer_c.register(toxcast_search_factory())
        
        # Initialize the base class
        super().__init__(
            layer_a=layer_a,
            layer_b=layer_b,
            layer_c=layer_c,
            sys_prompt=system_prompt
        )
        
        logger.info("✅ ToxicityReasoningMode initialized successfully")
        logger.info(f"📋 Available tools: {list(self.layers.list_tools())}")
    
    def get_tool_descriptions(self) -> Dict[str, str]:
        """
        Get descriptions of available tools for the reasoning mode.
        
        Returns:
            Dictionary mapping tool names to descriptions
        """
        return {
            "parametric_memory": (
                "General knowledge about molecular toxicity, chemical properties, "
                "and structure-activity relationships"
            ),
            "pubmed_search": (
                "Search PubMed for scientific literature on toxicity studies, "
                "mechanisms, and recent research findings"
            ),
            "pubchem_search": (
                "Access PubChem database for chemical properties, molecular weight, "
                "formula, and available toxicity information"
            ),
            "chembl_search": (
                "Search ChEMBL database for bioactivity data, target interactions, "
                "and toxicity-related bioassays"
            ),
            "toxcast_search": (
                "Access EPA ToxCast/Tox21 databases for high-throughput toxicity "
                "screening data and mechanistic information"
            )
        } 