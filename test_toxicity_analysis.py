#!/usr/bin/env python3
"""
Test script for molecular toxicity analysis using Layer C external knowledge tools.

This script demonstrates how to use the biological reasoning system to analyze
molecular toxicity by querying external databases and literature.
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


def test_toxicity_analysis(test_molecule: dict) -> None:
    """
    Test the toxicity analysis system with a given molecule.
    
    Args:
        test_molecule: Dictionary containing molecule information
    """
    test_logger.info(f"🧪 Starting toxicity analysis for: {test_molecule['name']}")
    
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
            "Analyze the provided molecule for toxicity using external knowledge sources."
        )
    )
    coordinator.reasoning_mode = ToxicityReasoningMode()
    
    # Create analysis prompt
    analysis_prompt = f"""
    Please analyze the following molecule for toxicity using BOTH your parametric knowledge AND external knowledge sources:

    Molecule Name: {test_molecule['name']}
    Molecular Structure (SMILES): {test_molecule['smiles']}
    Description: {test_molecule['description']}

    Please provide a comprehensive analysis including:

    1. **Parametric Knowledge Analysis** (Layer A):
       - Use your general knowledge about molecular toxicity principles
       - Analyze the chemical structure and predict potential toxicity mechanisms
       - Provide insights about structure-activity relationships
       - Discuss general toxicity pathways and molecular interactions

    2. **Chemical Properties** (PubChem):
       - Search for specific chemical information and properties
       - Get molecular weight, formula, and available toxicity data
       - Compare with your parametric knowledge

    3. **Literature Review** (PubMed):
       - Search for recent toxicity studies and mechanistic research
       - Look for validation or contradiction of your parametric insights
       - Find specific experimental data and clinical evidence

    4. **Bioactivity Data** (ChEMBL):
       - Search for bioactivity information and target interactions
       - Check for toxicity-related assays and mechanistic data
       - Integrate with your understanding of molecular interactions

    5. **EPA Screening Data** (ToxCast):
       - Check EPA toxicity screening results and mechanistic endpoints
       - Review high-throughput screening data
       - Compare with predicted mechanisms from parametric knowledge

    6. **Comprehensive Assessment**:
       - Synthesize ALL findings (parametric + external data)
       - Highlight where external data confirms or challenges your parametric knowledge
       - Provide mechanistic understanding integrating both sources
       - Give risk assessment and recommendations

    IMPORTANT: Start with your parametric knowledge to establish a foundation, then enhance and validate it with external data sources.
    """
    
    test_logger.info("🚀 Starting analysis...")
    
    try:
        response = coordinator.query([{"role": "user", "content": analysis_prompt}], stream=True)
        print(f"\n{'='*60}")
        print(f"TOXICITY ANALYSIS RESULTS FOR {test_molecule['name'].upper()}")
        print(f"{'='*60}")
        print(response)
        print(f"{'='*60}")
        
    except Exception as e:
        test_logger.error(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main function to run toxicity analysis tests."""
    test_logger.info("🧬 Starting Molecular Toxicity Analysis System")
    
    # Test molecules
    test_molecules = [
        {
            "name": "Benzene",
            "smiles": "c1ccccc1",
            "description": "Aromatic hydrocarbon, known carcinogen"
        },
        {
            "name": "Methanol",
            "smiles": "CO",
            "description": "Simple alcohol, toxic when ingested"
        }
    ]
    
    # Test with the first molecule
    test_toxicity_analysis(test_molecules[0])
    
    test_logger.info("✅ Toxicity analysis test completed")


if __name__ == "__main__":
    main() 