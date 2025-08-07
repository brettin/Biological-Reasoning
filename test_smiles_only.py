#!/usr/bin/env python3
"""
Test script to demonstrate toxicity analysis with only a SMILES string.
"""

import os
import logging
from dotenv import load_dotenv

from src.bio_reasoning.coordinator import Coordinator, Configuration
from src.bio_reasoning.reasoning import ToxicityReasoningMode

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
test_logger = logging.getLogger(__name__)


def test_smiles_only_analysis(smiles: str) -> None:
    """
    Test the toxicity analysis system with only a SMILES string.
    
    Args:
        smiles: SMILES string of the molecule
    """
    test_logger.info(f"🧪 Starting SMILES-only analysis for: {smiles}")
    
    # Configure the system
    config = Configuration(
        api_key=os.getenv("API_KEY", "brettin"),
        api_base_url=os.getenv("BASE_URL", "http://localhost:44497/v1"),
        model_name=os.getenv("MODEL_NAME", "gpto3"),
        stream=True
    )
    
    test_logger.info(f"🔧 Configuration: {config.model_name} at {config.api_base_url}")
    
    # Create coordinator with toxicity reasoning mode
    coordinator = Coordinator(
        config=config,
        system_prompt=(
            "You are a comprehensive molecular toxicity analysis system. "
            "Analyze the provided molecule for toxicity using both parametric knowledge and external data sources."
        )
    )
    coordinator.reasoning_mode = ToxicityReasoningMode()
    
    # Create analysis prompt with only SMILES
    analysis_prompt = f"""
    Please analyze the following molecule for toxicity using BOTH your parametric knowledge AND external knowledge sources:

    Molecular Structure (SMILES): {smiles}

    IMPORTANT: You only have the SMILES string. You will need to:
    1. Use your parametric knowledge to analyze the structure and predict properties
    2. Use PubChem search with SMILES to get chemical information
    3. Use PubMed search with structural terms (e.g., "aromatic hydrocarbon toxicity")
    4. Use ChEMBL search with SMILES for bioactivity data
    5. Use ToxCast search with structural descriptors

    Please provide a comprehensive analysis including:

    1. **Parametric Knowledge Analysis** (Layer A):
       - Analyze the SMILES structure and predict molecular properties
       - Identify structural features and potential toxicity mechanisms
       - Predict metabolic pathways and reactive intermediates

    2. **Chemical Properties** (PubChem):
       - Search using SMILES to get specific chemical information
       - Get molecular weight, formula, and available toxicity data

    3. **Literature Review** (PubMed):
       - Search using structural terms and toxicity keywords
       - Look for studies on similar compounds or structural classes

    4. **Bioactivity Data** (ChEMBL):
       - Search using SMILES for bioactivity information
       - Check for toxicity-related assays

    5. **EPA Screening Data** (ToxCast):
       - Search using structural descriptors
       - Review high-throughput screening data

    6. **Comprehensive Assessment**:
       - Synthesize ALL findings (parametric + external data)
       - Provide mechanistic understanding
       - Give risk assessment and recommendations

    Start with your parametric knowledge to establish a foundation, then enhance it with external data sources.
    """
    
    test_logger.info("🚀 Starting SMILES-only analysis...")
    
    try:
        response = coordinator.query([{"role": "user", "content": analysis_prompt}], stream=True)
        print(f"\n{'='*60}")
        print(f"SMILES-ONLY ANALYSIS RESULTS FOR {smiles}")
        print(f"{'='*60}")
        print(response)
        print(f"{'='*60}")
        
    except Exception as e:
        test_logger.error(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function to run SMILES-only analysis tests."""
    test_logger.info("🧬 Starting SMILES-Only Molecular Toxicity Analysis System")
    
    # Test with benzene SMILES only
    benzene_smiles = "c1ccccc1"
    unknown_smiles = "N1C2C=CC(=CC=2C2CCCCC=21)C(=O)NCC(CO)O"
    test_smiles_only_analysis(unknown_smiles)
    
    test_logger.info("✅ SMILES-only analysis test completed")


if __name__ == "__main__":
    main() 