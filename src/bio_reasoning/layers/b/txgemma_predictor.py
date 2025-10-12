"""
TX-Gemma predictor factory for Layer B specialized toxicity prediction.

This module provides access to Google's TX-Gemma model for molecular toxicity prediction.
TX-Gemma is specifically trained for toxicity endpoints and uses specialized prompts.

The system supports 12 distinct parameter combinations covering 703 TDC endpoints.
See TDC_PARAMETER_COMBINATIONS.md for complete documentation.
"""

import json
import os
import re
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union
from collections import defaultdict

from ...utils import query_chat_completion
from ...config import ConfigManager


# Default path to TDC prompts file
DEFAULT_TDC_PROMPTS_PATH = "../test/tdc_prompts.json"

# Parameter mapping from TDC placeholders to function parameters
TDC_PARAMETER_MAPPING = {
    '{Drug SMILES}': 'smiles',
    '{Drug1 SMILES}': 'drug1_smiles',
    '{Drug2 SMILES}': 'drug2_smiles',
    '{Target amino acid sequence}': 'target_protein',
    '{Antibody heavy chain sequence}': 'antibody_heavy',
    '{Antibody light chain sequence}': 'antibody_light',
    '{Antigen sequence}': 'antigen_sequence',
    '{Peptide amino acid sequence}': 'peptide_sequence',
    '{Possible MHC pseudosequences}': 'mhc_pseudosequences',
    '{Epitope amino acid sequence}': 'epitope_sequence',
    '{TCR amino acid sequence}': 'tcr_sequence',
    '{Protein1 amino acid sequence}': 'protein1_sequence',
    '{Protein2 amino acid sequence}': 'protein2_sequence',
    '{miRNA sequence}': 'mirna_sequence',
    '{Cell line description}': 'cell_line',
    '{Catalyst SMILES}': 'catalyst_smiles',
    '{Product SMILES}': 'product_smiles',
    '{Reactant SMILES}': 'reactant_smiles',
    '{GuideSeq}': 'guideseq'
}


def load_tdc_prompts(prompts_path: Optional[str] = None) -> Dict[str, str]:
    """Load TDC prompts from JSON file."""
    if prompts_path is None:
        prompts_path = DEFAULT_TDC_PROMPTS_PATH
    
    try:
        # Try to find the prompts file relative to this module or workspace root
        if not Path(prompts_path).is_absolute():
            # Try relative to current working directory first
            if Path(prompts_path).exists():
                full_path = Path(prompts_path)
            else:
                # Try relative to the module directory
                module_dir = Path(__file__).parent.parent.parent.parent
                full_path = module_dir / prompts_path
        else:
            full_path = Path(prompts_path)
        
        if full_path.exists():
            print(f"Loading TDC prompts from {full_path}")
            with open(full_path, 'r') as f:
                return json.load(f)
        else:
            print(f"Warning: TDC prompts file not found at {full_path}")
            return {}
    except Exception as e:
        print(f"Warning: Failed to load TDC prompts from {prompts_path}: {e}")
        return {}


def extract_required_parameters(prompt: str) -> List[str]:
    """Extract all required parameter placeholders from a prompt."""
    # Regular expression pattern to match text between curly braces
    # e.g. "{Target amino acid sequence}" -> "Target amino acid sequence"
    pattern = r'\{([^}]+)\}'
    return re.findall(pattern, prompt)


def has_required_parameters(required_params: List[str], **kwargs) -> bool:
    """Check if all required parameters are provided in kwargs."""
    for required_param in required_params:
        # Find the corresponding parameter name in our mapping
        param_name = None
        for placeholder, mapped_name in TDC_PARAMETER_MAPPING.items():
            if placeholder == f"{{{required_param}}}":
                param_name = mapped_name
                break
        
        if param_name and param_name in kwargs and kwargs[param_name]:
            continue  # This parameter is provided
        else:
            # Required parameter is missing
            return False
    
    return True


def get_matching_prompts(**kwargs) -> Dict[str, str]:
    """
    Find all TDC prompts that match the provided parameters.
    
    Returns:
        Dictionary mapping endpoint names to their TDC keys
    """
    tdc_prompts = load_tdc_prompts()
    matching_prompts = {}
    
    for tdc_key, prompt in tdc_prompts.items():
        # Check if this prompt requires parameters we don't have
        required_params = extract_required_parameters(prompt)
        if has_required_parameters(required_params, **kwargs):
            endpoint_name = tdc_key.lower().replace("_", " ")
            matching_prompts[endpoint_name] = tdc_key
    
    return matching_prompts


def predict_toxicity(endpoint: str = "all", **kwargs) -> Union[str, Dict[str, str]]:
    """
    Predict toxicity using TX-Gemma based on provided parameters.
    
    Args:
        endpoint: Specific endpoint name OR "all" to run all matching prompts
        **kwargs: Named parameters that determine which prompts to use:
            # SMILES-based parameters (most common)
            - smiles: Use prompts requiring {Drug SMILES}
            
            # Dual SMILES parameters (drug combinations)
            - drug1_smiles: Use prompts requiring {Drug1 SMILES}
            - drug2_smiles: Use prompts requiring {Drug2 SMILES}
            - cell_line: Use prompts requiring {Cell line description}
            
            # Protein/peptide parameters
            - target_protein: Use prompts requiring {Target amino acid sequence}
            - peptide_sequence: Use prompts requiring {Peptide amino acid sequence}
            - mhc_pseudosequences: Use prompts requiring {Possible MHC pseudosequences}
            - epitope_sequence: Use prompts requiring {Epitope amino acid sequence}
            - tcr_sequence: Use prompts requiring {TCR amino acid sequence}
            - protein1_sequence: Use prompts requiring {Protein1 amino acid sequence}
            - protein2_sequence: Use prompts requiring {Protein2 amino acid sequence}
            
            # Antibody parameters
            - antibody_heavy: Use prompts requiring {Antibody heavy chain sequence}
            - antibody_light: Use prompts requiring {Antibody light chain sequence}
            
            # miRNA parameters
            - mirna_sequence: Use prompts requiring {miRNA sequence}
            
            # Antigen parameters
            - antigen_sequence: Use prompts requiring {Antigen sequence}
            
            # Chemical reaction parameters
            - catalyst_smiles: Use prompts requiring {Catalyst SMILES}
            - product_smiles: Use prompts requiring {Product SMILES}
            - reactant_smiles: Use prompts requiring {Reactant SMILES}
            
            # CRISPR parameters
            - guideseq: Use prompts requiring {GuideSeq}
    
    Returns:
        If endpoint is specific: String with prediction result
        If endpoint is "all": Dictionary with {endpoint_name: prediction_result}
    """

    print(f"Available endpoints: {get_available_endpoints()}")
    print(f"Predicting toxicity for {endpoint} with kwargs: {kwargs}")

    # Handle "all" endpoint case
    if endpoint.lower() == "all":
        return predict_all_matching_endpoints(**kwargs)
    
    # Handle specific endpoint case
    # Try TX-Gemma first
    txgemma = get_txgemma_predictor()
    if txgemma:
        try:
            return txgemma(endpoint, **kwargs)
        except Exception as e:
            print(f"TX-Gemma prediction failed for {endpoint}: {str(e)}")
            raise e
    
    # Fallback to primary LLM with toxicity-focused prompt
    try:
        config = ConfigManager.get_config()
        primary_config = config.get_agent_config("primary")
        
        fallback_prompt = f"""
You are a toxicology expert. Predict the {endpoint} for the provided parameters.

Parameters: {kwargs}

Please provide:
1. Your prediction (Toxic/Non-toxic or specific values if applicable)
2. Confidence level (High/Medium/Low)
3. Brief reasoning based on the provided parameters

Format your response clearly and concisely.
"""
        
        messages = [
            {"role": "system", "content": "You are a computational toxicology expert."},
            {"role": "user", "content": fallback_prompt}
        ]
        
        return query_chat_completion(
            primary_config.api_base_url,
            primary_config.api_key,
            primary_config.model_name,
            messages,
            timeout=primary_config.timeout
        )
        
    except Exception as e:
        return f"Toxicity prediction unavailable: {str(e)}"


def predict_all_matching_endpoints(max_endpoints: int = 50, **kwargs) -> Dict[str, str]:
    """
    Run predictions for all endpoints that match the provided parameters.
    
    Args:
        max_endpoints: Maximum number of endpoints to test (default 50, use -1 for all endpoints)
        **kwargs: Parameters that determine which prompts to use
        
    Returns:
        Dictionary with {endpoint_name: prediction_result}
    """
    from loguru import logger
    
    results = {}
    txgemma = get_txgemma_predictor()
    
    if not txgemma:
        return {"error": "TX-Gemma predictor not available and primary LLM fallback not implemented for batch predictions"}
    
    # Get all matching endpoints
    matching_endpoints = get_matching_prompts(**kwargs)
    
    if not matching_endpoints:
        return {"error": f"No endpoints found matching the provided parameters: {kwargs}"}
    
    # Select endpoints to test
    if max_endpoints == -1:
        # Test all endpoints
        test_endpoints = list(matching_endpoints.items())
        logger.info(f"Running predictions for ALL {len(test_endpoints)} matching endpoints")
    else:
        # Test a subset of endpoints
        test_endpoints = list(matching_endpoints.items())[:max_endpoints]
        logger.info(f"Running predictions for {len(test_endpoints)} matching endpoints (max: {max_endpoints})")
    
    for i, (endpoint_name, tdc_key) in enumerate(test_endpoints, 1):
        try:
            logger.info(f"  {i}/{len(test_endpoints)}: Testing {endpoint_name}...")
            result = txgemma(endpoint_name, **kwargs)
            results[endpoint_name] = result
            logger.info(f"    Result: {result}")
        except Exception as e:
            results[endpoint_name] = f"Error: {str(e)}"
            logger.error(f"    Failed: {str(e)}")
    
    return results


def get_txgemma_predictor() -> Optional[Callable]:
    """
    Get TX-Gemma predictor function if available.
    
    Returns:
        TX-Gemma predictor function or None if not available
    """
    try:
        config = ConfigManager.get_config()
        if not config.has_endpoint("txgemma"):
            return None
        
        endpoint_config = config.get_endpoint("txgemma")
        
        def txgemma_predictor(endpoint: str, **kwargs) -> str:
            """TX-Gemma predictor function."""
            # Get the prompt for this endpoint
            print(f"Available endpoints: {get_available_endpoints()}")
            print(f"Predicting toxicity for {endpoint} with kwargs: {kwargs}")
            tdc_prompts = load_tdc_prompts()
            endpoint_mapping = {tdc_key.lower().replace("_", " "): tdc_key for tdc_key in tdc_prompts.keys()}
            
            tdc_key = endpoint_mapping.get(endpoint.lower())
            if not tdc_key or tdc_key not in tdc_prompts:
                raise ValueError(f"Endpoint '{endpoint}' not found in TDC prompts")
            
            prompt = tdc_prompts[tdc_key]
            
            # Perform parameter substitutions
            formatted_prompt = prompt
            for placeholder, param_name in TDC_PARAMETER_MAPPING.items():
                if param_name in kwargs:
                    formatted_prompt = formatted_prompt.replace(placeholder, str(kwargs[param_name]))
            
            # Make API call to TX-Gemma
            messages = [
                {"role": "user", "content": formatted_prompt}
            ]
            
            return formatted_prompt + "\n" + query_chat_completion(
                endpoint_config.api_base_url,
                endpoint_config.api_key,
                endpoint_config.model_name,
                messages,
                timeout=endpoint_config.timeout
            )
        
        return txgemma_predictor
        
    except Exception as e:
        print(f"Failed to create TX-Gemma predictor: {e}")
        return None


def get_available_endpoints() -> Dict[str, List[str]]:
    """
    Get organized list of available TX-Gemma endpoints by parameter pattern.
    
    Returns:
        Dictionary with endpoint categories and their supported endpoints
    """
    tdc_prompts = load_tdc_prompts()
    endpoints_by_pattern = defaultdict(list)
    
    for tdc_key, prompt in tdc_prompts.items():
        required_params = extract_required_parameters(prompt)
        param_tuple = tuple(sorted(required_params))
        endpoint_name = tdc_key.lower().replace("_", " ")
        endpoints_by_pattern[str(param_tuple)].append(endpoint_name)
    
    return dict(endpoints_by_pattern)


def txgemma_predictor_factory(
    api_key: str,
    api_base_url: str,
    model_name: str = "google/txgemma-27b-chat",
    prompts_path: Optional[str] = None,
) -> Callable[[str, str], str]:
    """
    Factory function to create a TX-Gemma toxicity prediction function.
    
    This is a legacy function for backward compatibility.
    For new code, use predict_toxicity() directly.
    
    Args:
        api_key: API key for authentication
        api_base_url: Base URL of the TX-Gemma API endpoint
        model_name: TX-Gemma model name (e.g., google/txgemma-27b-chat)
        prompts_path: Optional path to TX-Gemma prompts JSON file

    Returns:
        Function that takes (smiles, endpoint) and returns toxicity prediction
    """
    
    def legacy_predictor(smiles: str, endpoint: str = "mutagenicity") -> str:
        """Legacy predictor function for backward compatibility."""
        return predict_toxicity(endpoint=endpoint, smiles=smiles)
    
    return legacy_predictor


if __name__ == "__main__":
    # Test the TX-Gemma predictor using central configuration
    from loguru import logger
    
    try:
        config = ConfigManager.get_config()
        
        # Test single SMILES prediction
        test_smiles = "c1ccccc1"  # benzene
        logger.info(f"Testing single SMILES prediction with benzene (SMILES: {test_smiles})")
        
        if config.has_endpoint("txgemma"):
            logger.info("TX-Gemma endpoint configured - using specialized model")
            endpoint_config = config.get_endpoint("txgemma")
            logger.info(f"TX-Gemma endpoint: {endpoint_config.api_base_url}")
        else:
            logger.info("️TX-Gemma not configured - will use primary LLM fallback")
            
        # Test single endpoint prediction
        logger.info("Testing single endpoint prediction...")
        result = predict_toxicity(endpoint="ames", smiles=test_smiles)
        logger.info(f"AMES prediction: {result}")
        
        # Test "all" endpoints prediction
        logger.info("\nTesting 'all' endpoints prediction...")
        all_results = predict_toxicity(endpoint="all", smiles=test_smiles)
        
        if isinstance(all_results, dict):
            logger.info(f"Completed predictions for {len(all_results)} endpoints:")
            for endpoint, prediction in list(all_results.items())[:5]:  # Show first 5
                logger.info(f"  {endpoint}: {prediction}")
            if len(all_results) > 5:
                logger.info(f"  ... and {len(all_results) - 5} more")
        else:
            logger.info(f"All endpoints result: {all_results}")
        
        # Test antibody prediction (no SMILES required)
        logger.info("\n" + "="*60)
        logger.info("TESTING ANTIBODY PREDICTION (NO SMILES REQUIRED)")
        logger.info("="*60)
        
        antibody_results = predict_toxicity(
            endpoint="all",
            antibody_heavy="QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYWMQWVKQRPGQGLEWIGYINPYNDGTKYNEKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARYYDDHYCLDYWGQGTTLTVSS",
            antibody_light="DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYASQSISGIPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTPFTFGQGTKVEIK"
        )
        
        if isinstance(antibody_results, dict):
            logger.info(f"Completed antibody predictions for {len(antibody_results)} endpoints:")
            for endpoint, prediction in antibody_results.items():
                logger.info(f"  {endpoint}: {prediction}")
        else:
            logger.info(f"Antibody result: {antibody_results}")
        
        # Test drug combination prediction
        logger.info("\n" + "="*60)
        logger.info("TESTING DRUG COMBINATION PREDICTION")
        logger.info("="*60)
        
        combination_results = predict_toxicity(
            endpoint="all",
            drug1_smiles=test_smiles,
            drug2_smiles="CC(=O)OC1=CC=CC=C1C(=O)O",  # Aspirin
            cell_line="MCF-7 breast cancer cell line"
        )
        
        if isinstance(combination_results, dict):
            logger.info(f"Completed drug combination predictions for {len(combination_results)} endpoints:")
            for endpoint, prediction in combination_results.items():
                logger.info(f"  {endpoint}: {prediction}")
        else:
            logger.info(f"Drug combination result: {combination_results}")
        
    except Exception as e:
        logger.error(f"Configuration or prediction error: {e}")
