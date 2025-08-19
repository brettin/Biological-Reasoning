"""
Toxicology instantiation pattern for the BioR5 framework.

This module demonstrates the instantiation pattern:
- Start with an existing reasoning mode (MechanisticReasoningMode)
- Augment it with toxicology-specific tools
- Append toxicology-specific instructions based on user queries

Usage:
    from bio_reasoning.reasoning.toxicology_instantiation import create_toxicology_mode
    toxicology_mode = create_toxicology_mode(user_query="Analyze benzene toxicity")
"""

from typing import Optional

from loguru import logger
from toolregistry import ToolRegistry

from .modes.mechanistic_reasoning import MechanisticReasoningMode
from ..layers.b.txgemma_predictor import get_txgemma_predictor
from ..config import ConfigManager


def create_toxicology_mode(user_query: Optional[str] = None) -> MechanisticReasoningMode:
    """
    Create a toxicology-specialized reasoning mode using instantiation pattern.
    
    Args:
        user_query: User's toxicology question to customize the system prompt
        
    Returns:
        MechanisticReasoningMode instance augmented with toxicology capabilities
    """
    # Step 1: Instantiate base reasoning mode
    base_mode = MechanisticReasoningMode()
    
    # Step 2: Augment Layer B with TX-Gemma predictor using centralized config
    try:
        config = ConfigManager.get_config()
        
        # Try to get TX-Gemma predictor (handles fallback automatically)
        txgemma_predictor = get_txgemma_predictor()
        
        if txgemma_predictor:
            base_mode.layer_b.register(txgemma_predictor)
            if config.has_endpoint("txgemma"):
                logger.info("✅ TX-Gemma predictor added to toxicology mode")
            else:
                logger.info("✅ Primary LLM predictor added to toxicology mode (TX-Gemma fallback)")
        else:
            logger.warning("⚠️ No predictor available for toxicology mode")
            
    except Exception as e:
        logger.warning(f"Could not add predictor to toxicology mode: {e}")
    
    # Step 3: Augment Layer C with toxicology databases
    try:
        from ..layers.c.pubchem_toxicity import pubchem_toxicity_factory
        from ..layers.c.toxcast_endpoints import toxcast_endpoints_factory
        from ..layers.c.chembl_mechanisms import chembl_mechanisms_factory
        
        # PubChem toxicity data
        pubchem_search = pubchem_toxicity_factory()
        base_mode.layer_c.register(pubchem_search, name="pubchem_toxicity")
        
        # ToxCast endpoints
        toxcast_search = toxcast_endpoints_factory()
        base_mode.layer_c.register(toxcast_search, name="toxcast_endpoints")
        
        # ChEMBL mechanism data
        chembl_search = chembl_mechanisms_factory()
        base_mode.layer_c.register(chembl_search, name="chembl_mechanisms")
        
        print("✅ Layer C tools loaded: PubChem, ToxCast, ChEMBL")
        
    except Exception as e:
        print(f"Warning: Could not load some Layer C tools: {e}")
        # TODO: Add PubMed toxicology literature search when available
    
    # Step 4: Append toxicology-specific instructions to system prompt
    toxicology_instructions = _generate_toxicology_instructions(user_query)
    base_mode.sys_prompt += "\n\n" + toxicology_instructions
    
    # Step 5: Update mode metadata for toxicology
    base_mode.name = "Mechanistic Toxicology Expert"
    base_mode.description = "Mechanistic reasoning specialized for molecular toxicity analysis"
    base_mode.keywords.extend([
        "toxicity", "toxic", "mutagenic", "carcinogenic", "hepatotoxic",
        "ADMET", "safety", "hERG", "Ames test", "LD50", "adverse effects"
    ])
    base_mode.name_canonical = "toxicology"
    
    return base_mode


def _generate_toxicology_instructions(user_query: Optional[str] = None) -> str:
    """
    Generate toxicology-specific instructions based on user query.
    
    Args:
        user_query: User's question to customize instructions
        
    Returns:
        Toxicology-specific system prompt instructions
    """
    base_instructions = """
=== TOXICOLOGY SPECIALIZATION ===

You are now operating in TOXICOLOGY mode. Your mechanistic reasoning is specialized for:

**Core Toxicology Analysis Framework:**
1. **Molecular Identification**: Identify the compound and key structural alerts for toxicity
2. **TX-Gemma Predictions**: Use txgemma_predictor for specific endpoints (mutagenicity, hERG, etc.)
3. **Mechanistic Analysis**: Apply your mechanistic reasoning to toxicity pathways
4. **Literature Integration**: Synthesize experimental data with predicted mechanisms
5. **Risk Assessment**: Provide integrated toxicity profile with confidence levels

**Available Toxicology Tools:**
- txgemma_predictor: Specialized AI model for toxicity endpoint prediction
- parametric_memory: Your knowledge of toxicology mechanisms and pathways
- pubchem_toxicity: PubChem database for molecular properties and experimental data
- toxcast_endpoints: EPA ToxCast high-throughput toxicity screening data
- chembl_mechanisms: ChEMBL database for mechanism of action and bioactivity data

**Analysis Priority:**
1. Experimental data > AI predictions > computational estimates
2. Human data > animal data > in vitro data > in silico predictions
3. Peer-reviewed literature > databases > computational models

**Output Format:**
Always structure toxicology analyses as:
- **Compound Identification**: Name, SMILES, key structural features
- **Toxicity Predictions**: TX-Gemma results with confidence
- **Mechanistic Pathways**: Detailed molecular mechanisms
- **Experimental Evidence**: Literature and database findings
- **Risk Assessment**: Integrated conclusion with uncertainty
"""
    
    # Add query-specific instructions
    if user_query:
        query_specific = _get_query_specific_instructions(user_query)
        if query_specific:
            base_instructions += f"\n**Query-Specific Focus:**\n{query_specific}"
    
    return base_instructions


def _get_query_specific_instructions(user_query: str) -> str:
    """
    Generate specific instructions based on the user's query content.
    
    Args:
        user_query: User's toxicology question
        
    Returns:
        Query-specific instructions
    """
    query_lower = user_query.lower()
    
    instructions = []
    
    # Endpoint-specific instructions
    if any(term in query_lower for term in ["mutagenic", "mutation", "ames"]):
        instructions.append("- Focus on mutagenicity mechanisms (DNA damage, repair pathways)")
    
    if any(term in query_lower for term in ["herg", "cardiac", "arrhythmia"]):
        instructions.append("- Emphasize hERG channel blocking and cardiac safety")
    
    if any(term in query_lower for term in ["hepatotoxic", "liver", "hepatic"]):
        instructions.append("- Analyze hepatotoxicity pathways (CYP metabolism, oxidative stress)")
    
    if any(term in query_lower for term in ["carcinogenic", "cancer", "tumor"]):
        instructions.append("- Examine carcinogenicity mechanisms (DNA damage, oncogenes)")
    
    if any(term in query_lower for term in ["developmental", "teratogenic", "pregnancy"]):
        instructions.append("- Consider developmental toxicity and teratogenic potential")
    
    # Structure-specific instructions
    if "smiles" in query_lower:
        instructions.append("- Parse SMILES structure for toxicophores and structural alerts")
    
    if any(term in query_lower for term in ["mechanism", "pathway", "how"]):
        instructions.append("- Provide detailed mechanistic pathway analysis")
    
    if any(term in query_lower for term in ["compare", "comparison", "versus"]):
        instructions.append("- Include comparative toxicity analysis between compounds")
    
    return "\n".join(instructions) if instructions else ""


# Convenience function for registry integration
def create_toxicology_reasoning_mode(user_query: Optional[str] = None):
    """
    Create toxicology mode for registry integration.
    
    This function can be used by the registry system to create toxicology instances.
    """
    return create_toxicology_mode(user_query)


if __name__ == "__main__":
    # Test the instantiation pattern
    test_query = "Analyze the toxicity of benzene (SMILES: c1ccccc1)"
    toxicology_mode = create_toxicology_mode(test_query)
    
    print(f"Created mode: {toxicology_mode.name}")
    print(f"Canonical name: {toxicology_mode.name_canonical}")
    print(f"Description: {toxicology_mode.description}")
    print(f"Keywords: {toxicology_mode.keywords}")
    print(f"Available tools: {len(toxicology_mode.layers.tools)}")
    print("\nSystem prompt preview:")
    print(toxicology_mode.sys_prompt[:500] + "..." if len(toxicology_mode.sys_prompt) > 500 else toxicology_mode.sys_prompt)
