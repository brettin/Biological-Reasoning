"""
Reasoning mode instantiation functions following BioR5 architecture.

This module provides functions to create specialized instances of existing
reasoning modes through configuration augmentation, not inheritance.

The key pattern: 'toxicology' → create_toxicology_mechanistic_mode() → 
augmented MechanisticReasoningMode with toxicology-specific content from 
configs/toxicology_mode.py
"""

import os
import time
from dotenv import load_dotenv
from toolregistry import ToolRegistry
from loguru import logger

from .mechanistic_reasoning import MechanisticReasoningMode
from .configs.toxicology_mode import (
    TOXICOLOGY_SYSTEM_PROMPT,
    TOXICOLOGY_TOOLS,
    TOXICOLOGY_KEYWORDS,
    TOXICOLOGY_PARAMETRIC_CONFIG
)
from ..layers.a.parametric_memory import parametric_memory_factory
from ..layers.c.pubmed import pubmed_search_toxicity
from ..layers.c.toxcast import toxcast_endpoints
from ..layers.c.chembl import chembl_mechanism
from ..layers.c.pubchem import pubchem_summary


def create_toxicology_mechanistic_mode(
    api_key: str = "brettin",
    api_base_url: str = "http://localhost:44497/v1",
    model_name: str = "gpto3",
) -> MechanisticReasoningMode:
    """
    Create a toxicology-specialized instance of MechanisticReasoningMode.
    
    This follows the BioR5 instantiation pattern - we augment an existing
    reasoning mode rather than creating a new class.
    
    Configuration mapping:
    'toxicology' → configs/toxicology_mode.py → {
        TOXICOLOGY_SYSTEM_PROMPT: augments base mechanistic prompt
        TOXICOLOGY_TOOLS: replaces Layer C tools  
        TOXICOLOGY_PARAMETRIC_CONFIG: specializes Layer A
        TOXICOLOGY_KEYWORDS: extends keywords
    }
    
    Args:
        api_key: API key for the model
        api_base_url: Base URL for the model API  
        model_name: Name of the model to use
        
    Returns:
        MechanisticReasoningMode instance specialized for toxicology
    """
    start_time = time.time()
    logger.debug("Starting toxicology mode instantiation")
    
    # Load environment variables
    load_dotenv()
    
    # Create base mechanistic reasoning mode
    base_start = time.time()
    base_mode = MechanisticReasoningMode()
    logger.debug(f"Base MechanisticReasoningMode created in {time.time() - base_start:.3f}s")
    
    # === AUGMENT SYSTEM PROMPT ===
    prompt_start = time.time()
    logger.debug("Augmenting system prompt with toxicology specialization")
    augmented_prompt = base_mode.sys_prompt + "\n\n" + TOXICOLOGY_SYSTEM_PROMPT
    base_mode.sys_prompt = augmented_prompt
    logger.debug(f"System prompt augmented in {time.time() - prompt_start:.3f}s")
    
    # === AUGMENT TOOLS ===
    tools_start = time.time()
    logger.debug("Replacing Layer C tools with toxicology-specific tools")
    base_mode.layer_c = ToolRegistry(name="Layer C - Toxicology Mechanistic")
    
    # Register toxicology-specific tools from config
    tool_map = {
        "pubmed_search_toxicity": pubmed_search_toxicity,
        "toxcast_endpoints": toxcast_endpoints,
        "chembl_mechanism": chembl_mechanism,
        "pubchem_summary": pubchem_summary,
    }
    
    tools_registered = 0
    for tool_name in TOXICOLOGY_TOOLS:
        if tool_name in tool_map:
            base_mode.layer_c.register(tool_map[tool_name])
            tools_registered += 1
    logger.debug(f"Registered {tools_registered} Layer C tools in {time.time() - tools_start:.3f}s")
    
    # === AUGMENT LAYER A (PARAMETRIC MEMORY) ===
    memory_start = time.time()
    logger.debug("Creating specialized parametric memory for toxicology")
    base_mode.layer_a = ToolRegistry(name="Layer A - Toxicology Mechanistic")
    
    toxicology_parametric_memory = parametric_memory_factory(
        api_key=api_key,
        api_base_url=api_base_url,
        model_name=model_name,
        system_prompt=TOXICOLOGY_PARAMETRIC_CONFIG["system_prompt"],
    )
    base_mode.layer_a.register(toxicology_parametric_memory)
    logger.debug(f"Parametric memory specialized in {time.time() - memory_start:.3f}s")
    
    # === AUGMENT METADATA ===
    meta_start = time.time()
    logger.debug("Updating mode metadata and keywords")
    base_mode.name = "Toxicology-Specialized Mechanistic Reasoning Expert"
    base_mode.description = (
        "Mechanistic reasoning specialized for molecular toxicity assessment, "
        "adverse outcome pathways, and toxicological mechanisms"
    )
    
    # Extend keywords with toxicology terms from config
    base_mode.keywords.extend(TOXICOLOGY_KEYWORDS)
    base_mode.name_canonical = "mechanistic_toxicology"
    logger.debug(f"Metadata updated in {time.time() - meta_start:.3f}s")
    
    total_elapsed = time.time() - start_time
    logger.debug(f"Toxicology instantiation complete in {total_elapsed:.3f}s total")
    return base_mode


def create_specialized_mode(base_mode_name: str, specialization: str, **config):
    """
    Generic function for creating specialized reasoning mode instances.
    
    This demonstrates the pattern for future specializations:
    base_mode_name + specialization → specialized configuration → augmented mode
    
    Args:
        base_mode_name: Name of base reasoning mode to specialize
        specialization: Name of specialization configuration
        **config: Additional configuration parameters
        
    Returns:
        Specialized reasoning mode instance
    """
    if base_mode_name == "mechanistic" and specialization == "toxicology":
        return create_toxicology_mechanistic_mode(**config)
    else:
        raise ValueError(f"Unsupported specialization: {base_mode_name}+{specialization}")


if __name__ == "__main__":
    # Test the instantiation
    tox_mode = create_toxicology_mechanistic_mode()
    print(f"Created: {tox_mode.name}")
    print(f"Type: {type(tox_mode).__name__}")
    print(f"Description: {tox_mode.description}")
    print(f"Keywords: {len(tox_mode.keywords)} total")
    print(f"Layer A tools: {len(tox_mode.layer_a._tools)}")
    print(f"Layer C tools: {len(tox_mode.layer_c._tools)}")
    print(f"Total tools: {len(tox_mode.layers._tools)}")