"""
TX-Gemma predictor factory for Layer B specialized toxicity prediction.

This module provides access to Google's TX-Gemma model for molecular toxicity prediction.
TX-Gemma is specifically trained for toxicity endpoints and uses specialized prompts.
"""

import json
import os
from typing import Callable, Dict, List, Optional, Union

from ...utils import query_chat_completion


def txgemma_predictor_factory(
    api_key: str,
    api_base_url: str,
    model_name: str = "google/txgemma-27b-chat",
    prompts_path: Optional[str] = None,
) -> Callable[[str, str], str]:
    """
    Factory function to create a TX-Gemma toxicity prediction function.

    Args:
        api_key: API key for authentication
        api_base_url: Base URL of the TX-Gemma API endpoint
        model_name: TX-Gemma model name (e.g., google/txgemma-27b-chat)
        prompts_path: Optional path to TX-Gemma prompts JSON file

    Returns:
        Function that takes (smiles, endpoint) and returns toxicity prediction
    """

    def txgemma_predictor(
        smiles: str, 
        endpoint: str = "mutagenicity",
        custom_prompt: Optional[str] = None
    ) -> str:
        """
        Predict toxicity endpoints using TX-Gemma model.

        Args:
            smiles: SMILES string of the molecule
            endpoint: Toxicity endpoint to predict. Options:
                     - "mutagenicity": Ames test mutagenicity
                     - "herg": hERG channel blocking
                     - "bbb": Blood-brain barrier permeability
                     - "caco2": Caco-2 cell permeability
                     - "cardiotoxicity": Cardiac toxicity
                     - "hepatotoxicity": Liver toxicity
                     - "general": General toxicity assessment
            custom_prompt: Optional custom prompt for specialized predictions

        Returns:
            TX-Gemma prediction result as string

        Raises:
            ValueError: If endpoint is not supported
            RuntimeError: If API request fails
        """
        if custom_prompt:
            # Use custom prompt
            prompt = custom_prompt.replace("{smiles}", smiles).replace("{SMILES}", smiles)
        else:
            # Use predefined endpoint prompts
            prompt = _get_endpoint_prompt(smiles, endpoint)

        # Prepare messages for TX-Gemma
        messages = [
            {"role": "user", "content": prompt}
        ]

        try:
            # Query TX-Gemma model
            response = query_chat_completion(
                base_url=api_base_url,
                api_key=api_key,
                model_name=model_name,
                messages=messages,
                timeout=120  # TX-Gemma may need more time
            )
            
            return response

        except Exception as e:
            raise RuntimeError(f"TX-Gemma prediction failed for {endpoint}: {str(e)}")

    return txgemma_predictor


def _get_endpoint_prompt(smiles: str, endpoint: str) -> str:
    """
    Get the appropriate TX-Gemma prompt for a specific toxicity endpoint.
    
    Args:
        smiles: SMILES string of the molecule
        endpoint: Toxicity endpoint name
        
    Returns:
        Formatted prompt for TX-Gemma
        
    Raises:
        ValueError: If endpoint is not supported
    """
    # TX-Gemma specific prompts based on TDC format
    endpoint_prompts = {
        "mutagenicity": {
            "instruction": "Classify the following molecule as mutagenic or not.",
            "context": "Mutagenicity is the ability of a compound to cause genetic mutations, and is a critical consideration for early toxicity screening.",
            "question": f"Is the following molecule mutagenic? SMILES: {smiles}"
        },
        
        "herg": {
            "instruction": "Predict whether the molecule blocks the hERG potassium channel.",
            "context": "Blockade of the hERG channel can lead to fatal cardiac arrhythmia, and is a common cause of drug withdrawal.",
            "question": f"Does the following molecule block the hERG channel? SMILES: {smiles}"
        },
        
        "bbb": {
            "instruction": "Assess the molecule's ability to cross the blood-brain barrier.",
            "context": "Only molecules with suitable physicochemical properties can penetrate the blood-brain barrier, essential for CNS drug development.",
            "question": f"Can this molecule cross the blood-brain barrier? SMILES: {smiles}"
        },
        
        "caco2": {
            "instruction": "Estimate the Caco-2 cell permeability of the compound.",
            "context": "The Caco-2 assay simulates intestinal absorption. Values are reported in cm/s.",
            "question": f"What is the Caco-2 permeability of SMILES: {smiles}?"
        },
        
        "cardiotoxicity": {
            "instruction": "Assess the cardiotoxicity potential of the molecule.",
            "context": "Cardiotoxicity can manifest through various mechanisms including hERG channel blockade, calcium channel interference, and direct myocardial damage.",
            "question": f"Does the following molecule have cardiotoxicity potential? SMILES: {smiles}"
        },
        
        "hepatotoxicity": {
            "instruction": "Predict hepatotoxicity potential of the molecule.",
            "context": "Hepatotoxicity is a major cause of drug attrition and can occur through multiple mechanisms including metabolic activation, oxidative stress, and mitochondrial dysfunction.",
            "question": f"Does the following molecule have hepatotoxicity potential? SMILES: {smiles}"
        },
        
        "general": {
            "instruction": "Provide a comprehensive toxicity assessment of the molecule.",
            "context": "Comprehensive toxicity assessment should consider multiple endpoints including mutagenicity, organ toxicity, and ADMET properties.",
            "question": f"Provide a comprehensive toxicity assessment for SMILES: {smiles}"
        }
    }
    
    if endpoint not in endpoint_prompts:
        available_endpoints = list(endpoint_prompts.keys())
        raise ValueError(f"Unsupported endpoint '{endpoint}'. Available endpoints: {available_endpoints}")
    
    prompt_data = endpoint_prompts[endpoint]
    
    # Format in TX-Gemma expected format
    formatted_prompt = f"""Instruction: {prompt_data['instruction']}

Context: {prompt_data['context']}

Question: {prompt_data['question']}

Answer:"""
    
    return formatted_prompt


def get_available_endpoints() -> List[str]:
    """
    Get list of available TX-Gemma toxicity endpoints.
    
    Returns:
        List of supported endpoint names
    """
    return [
        "mutagenicity",
        "herg", 
        "bbb",
        "caco2",
        "cardiotoxicity",
        "hepatotoxicity",
        "general"
    ]


def batch_predict(
    smiles_list: List[str],
    endpoint: str,
    api_key: str,
    api_base_url: str,
    model_name: str = "google/txgemma-27b-chat"
) -> Dict[str, str]:
    """
    Batch prediction for multiple SMILES strings.
    
    Args:
        smiles_list: List of SMILES strings
        endpoint: Toxicity endpoint to predict
        api_key: API key for authentication
        api_base_url: Base URL of the TX-Gemma API
        model_name: TX-Gemma model name
        
    Returns:
        Dictionary mapping SMILES to prediction results
    """
    predictor = txgemma_predictor_factory(api_key, api_base_url, model_name)
    
    results = {}
    for smiles in smiles_list:
        try:
            prediction = predictor(smiles, endpoint)
            results[smiles] = prediction
        except Exception as e:
            results[smiles] = f"Error: {str(e)}"
    
    return results


if __name__ == "__main__":
    # Test the TX-Gemma predictor
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    # Example usage
    predictor = txgemma_predictor_factory(
        api_key=os.getenv("TXGEMMA_API_KEY", "EMPTY"),
        api_base_url=os.getenv("TXGEMMA_BASE_URL", "http://REPLACE_WITH_YOUR_BASE_URL/v1"),
        model_name=os.getenv("TXGEMMA_MODEL_NAME", "google/txgemma-27b-chat")
    )
    
    # Test with benzene
    test_smiles = "c1ccccc1"  # benzene
    
    print(f"Testing TX-Gemma with benzene (SMILES: {test_smiles})")
    print(f"Available endpoints: {get_available_endpoints()}")
    
    try:
        # Test mutagenicity prediction
        result = predictor(test_smiles, "mutagenicity")
        print(f"\nMutagenicity prediction: {result}")
        
        # Test hERG prediction
        result = predictor(test_smiles, "herg")
        print(f"hERG prediction: {result}")
        
    except Exception as e:
        print(f"Error during testing: {e}")
        print("Note: Make sure TX-Gemma model server is running on the specified endpoint")
