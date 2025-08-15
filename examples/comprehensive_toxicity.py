#!/usr/bin/env python3
"""
Comprehensive toxicity analysis example using BioR5 instantiation pattern.

This demonstrates the complete toxicology workflow:
1. Instantiate MechanisticReasoningMode with toxicology specialization
2. TX-Gemma predictions for multiple endpoints
3. Literature analysis and mechanistic reasoning
4. Integrated risk assessment

Usage:
    conda activate bio_reason
    python examples/comprehensive_toxicity.py [smiles_string]
    
Examples:
    python examples/comprehensive_toxicity.py "c1ccccc1"  # benzene
    python examples/comprehensive_toxicity.py "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"  # caffeine
    python examples/comprehensive_toxicity.py "CC(=O)OC1=CC=CC=C1C(=O)O"  # aspirin
    python examples/comprehensive_toxicity.py "CN1C(=O)CN=C(C2=CCCCC2)c2cc(Cl)ccc21"  # clonazepam
"""

import sys
import os
import time
from typing import Dict, List

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cicada.core import PromptBuilder
from bio_reasoning.coordinator import Coordinator, Configuration
from bio_reasoning.reasoning.registry import create_reasoning_mode
from loguru import logger


def comprehensive_toxicity_analysis(smiles: str, molecule_name: str = None):
    """
    Comprehensive toxicity analysis using instantiation pattern.
    
    Args:
        smiles: SMILES string of the molecule
        molecule_name: Optional molecule name for better context
    """
    
    script_start = time.time()
    logger.info(f"=== COMPREHENSIVE TOXICITY ANALYSIS ===")
    logger.info(f"SMILES: {smiles}")
    if molecule_name:
        logger.info(f"Molecule: {molecule_name}")
    
    # Configure for your setup
    config = Configuration(
        api_key=os.getenv("API_KEY", "REPLACE WITH YOUR API KEY"),
        api_base_url=os.getenv("BASE_URL", "REPLACE WITH YOUR BASE URL"),
        model_name=os.getenv("MODEL_NAME", "REPLACE WITH YOUR MODEL NAME"),
        stream=False  # Use non-streaming for cleaner output
    )
    
    # Create coordinator
    coordinator = Coordinator(config=config)
    
    # Use instantiation pattern: toxicology → MechanisticReasoningMode + toxicology tools/prompts
    user_query = f"Analyze the comprehensive toxicity of {molecule_name or 'the molecule'} with SMILES: {smiles}"
    
    mode_start = time.time()
    coordinator.reasoning_mode = create_reasoning_mode("toxicology", user_query)
    mode_elapsed = time.time() - mode_start
    logger.info(f"Toxicology mode instantiated in {mode_elapsed:.3f}s")
    logger.info(f"Mode: {coordinator.reasoning_mode.name}")
    try:
        tools_count = len(coordinator.reasoning_mode.layers._tools) if hasattr(coordinator.reasoning_mode.layers, '_tools') else "Unknown"
        logger.info(f"Tools available: {tools_count}")
    except:
        logger.info("Tools available: Unable to determine count")
    
    # Build comprehensive analysis query
    pb = PromptBuilder()
    pb.add_user_message(f"""
    Perform a comprehensive toxicity analysis for the molecule with SMILES: {smiles}
    {f'(Molecule name: {molecule_name})' if molecule_name else ''}
    
    **Analysis Protocol:**
    
    1. **Molecular Identification & Structure Analysis**
       - Identify the molecule and confirm the name
       - Analyze key structural features and toxicophores
       - Note any structural alerts for toxicity
    
    2. **TX-Gemma Toxicity Predictions**
       - Use txgemma_predictor for multiple endpoints:
         * Mutagenicity (Ames test)
         * hERG channel blocking (cardiotoxicity) 
         * Blood-brain barrier permeability
         * General toxicity assessment
       - Report predictions with confidence assessment
    
    3. **Mechanistic Toxicity Analysis**
       - Apply your mechanistic reasoning expertise to predict:
         * Primary toxicity mechanisms
         * Target organs/systems
         * Metabolic pathways leading to toxicity
         * Dose-response considerations
    
    4. **Literature Integration**
       - Synthesize known experimental data
       - Compare with similar compounds
       - Note any species differences in toxicity
    
    5. **Integrated Risk Assessment**
       - Overall toxicity profile
       - Confidence levels for each endpoint
       - Recommendations for further testing
       - Risk mitigation strategies
    
    **Output Format:**
    Please structure your analysis with clear sections and provide specific, actionable conclusions.
    """)
    
    # Execute comprehensive analysis
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE TOXICITY ANALYSIS")
    print(f"{'='*80}")
    print(f"Molecule: {molecule_name or 'Unknown'}")
    print(f"SMILES: {smiles}")
    print(f"Reasoning Mode: {coordinator.reasoning_mode.name}")
    print(f"Analysis Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}")
    
    analysis_start = time.time()
    response = coordinator.query(pb.messages)
    analysis_elapsed = time.time() - analysis_start
    
    total_elapsed = time.time() - script_start
    
    print(response)
    
    print(f"\n{'='*80}")
    print(f"ANALYSIS SUMMARY")
    print(f"{'='*80}")
    print(f"⏱️  Timing:")
    print(f"   Mode Setup:     {mode_elapsed:.3f}s")
    print(f"   Analysis:       {analysis_elapsed:.3f}s") 
    print(f"   Total:          {total_elapsed:.3f}s")
    print(f"🧠  Reasoning Mode: {coordinator.reasoning_mode.name}")
    try:
        tools_count = len(coordinator.reasoning_mode.layers._tools) if hasattr(coordinator.reasoning_mode.layers, '_tools') else "Unknown"
        print(f"🔬  Tools Used:     {tools_count}")
    except:
        print(f"🔬  Tools Used:     Available")
    print(f"📊  Analysis Type:  Comprehensive Toxicology Assessment")
    

def run_toxicity_battery(molecules: List[Dict[str, str]]):
    """
    Run toxicity analysis on a battery of test molecules.
    
    Args:
        molecules: List of dicts with 'smiles' and 'name' keys
    """
    logger.info(f"=== TOXICITY BATTERY ANALYSIS ===")
    logger.info(f"Testing {len(molecules)} molecules")
    
    for i, mol in enumerate(molecules, 1):
        print(f"\n\n{'#'*100}")
        print(f"MOLECULE {i}/{len(molecules)}: {mol['name']}")
        print(f"{'#'*100}")
        
        try:
            comprehensive_toxicity_analysis(mol['smiles'], mol['name'])
        except Exception as e:
            logger.error(f"Error analyzing {mol['name']}: {e}")
            continue
        
        if i < len(molecules):
            print(f"\n{'.'*50} Moving to next molecule {'.'*50}")


if __name__ == "__main__":
    # Test molecules with varying toxicity profiles
    test_molecules = [
        {"smiles": "c1ccccc1", "name": "Benzene"},
        {"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "name": "Caffeine"},
        {"smiles": "CC(=O)OC1=CC=CC=C1C(=O)O", "name": "Aspirin"},
        {"smiles": "CN1C(=O)CN=C(C2=CCCCC2)c2cc(Cl)ccc21", "name": "Clonazepam"},
        {"smiles": "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O", "name": "Ibuprofen"}
    ]
    
    if len(sys.argv) > 1:
        # Single molecule analysis
        smiles = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else None
        
        if smiles == "--battery":
            # Run full battery
            run_toxicity_battery(test_molecules)
        else:
            comprehensive_toxicity_analysis(smiles, name)
    else:
        # Default demo
        print("No SMILES provided, running comprehensive toxicity analysis on benzene")
        print("\nUsage options:")
        print("  python examples/comprehensive_toxicity.py 'SMILES_STRING' ['MOLECULE_NAME']")
        print("  python examples/comprehensive_toxicity.py --battery  # Run full test battery")
        print("\nExample molecules:")
        for mol in test_molecules:
            print(f"  {mol['name']:12} : {mol['smiles']}")
        print()
        
        # Run benzene example
        comprehensive_toxicity_analysis("c1ccccc1", "Benzene")
