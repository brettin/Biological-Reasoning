"""
ToxCast endpoints integration for Layer C external knowledge sources.

This module provides access to EPA's ToxCast database for high-throughput 
toxicity screening data and predictive toxicology endpoints.
"""

import json
import time
from typing import Dict, List, Optional, Union

import requests


def toxcast_endpoints_factory(
    timeout: int = 30,
    max_retries: int = 3
) -> callable:
    """
    Factory function to create a ToxCast endpoints retrieval function.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        
    Returns:
        Function that retrieves ToxCast data
    """
    
    def toxcast_search(
        identifier: str,
        identifier_type: str = "casrn",
        endpoints: Optional[List[str]] = None
    ) -> str:
        """
        Search ToxCast for toxicity endpoint data.
        
        Args:
            identifier: Chemical identifier (CAS RN, DTXSID, name, etc.)
            identifier_type: Type of identifier ("casrn", "dtxsid", "name")
            endpoints: Specific endpoints to retrieve (default: key toxicity endpoints)
            
        Returns:
            Formatted ToxCast endpoint data summary
        """
        if endpoints is None:
            endpoints = [
                "cytotoxicity", "genotoxicity", "endocrine", "neurotoxicity", 
                "developmental", "cardiotoxicity", "hepatotoxicity"
            ]
        
        try:
            # ToxCast data through EPA's CompTox Chemicals Dashboard API
            results = {}
            
            # Step 1: Get chemical information
            chem_info = _get_chemical_info(identifier, identifier_type, timeout)
            if not chem_info:
                return f"Chemical not found in EPA CompTox database: {identifier}"
            
            # Step 2: Get ToxCast bioactivity data
            bioactivity = _get_toxcast_bioactivity(chem_info, timeout)
            results["bioactivity"] = bioactivity
            
            # Step 3: Get specific endpoint predictions
            endpoint_predictions = _get_endpoint_predictions(chem_info, endpoints, timeout)
            results["predictions"] = endpoint_predictions
            
            # Step 4: Get QSAR model predictions
            qsar_predictions = _get_qsar_predictions(chem_info, timeout)
            results["qsar"] = qsar_predictions
            
            return _format_toxcast_results(identifier, chem_info, results)
            
        except Exception as e:
            return f"Error retrieving ToxCast data for {identifier}: {str(e)}"
    
    return toxcast_search


def _get_chemical_info(identifier: str, identifier_type: str, timeout: int) -> Optional[Dict]:
    """Get chemical information from EPA CompTox."""
    
    # EPA CompTox Chemicals Dashboard API endpoints
    base_url = "https://comptox.epa.gov/dashboard-api"
    
    try:
        if identifier_type == "casrn":
            url = f"{base_url}/ccdapp1/chemical-detail/by-casrn/{identifier}"
        elif identifier_type == "dtxsid":
            url = f"{base_url}/ccdapp1/chemical-detail/by-dtxsid/{identifier}"
        elif identifier_type == "name":
            # Search by name first to get DTXSID
            search_url = f"{base_url}/ccdapp1/search/chemical/equal/{identifier}"
            response = requests.get(search_url, timeout=timeout)
            if response.status_code == 200:
                search_data = response.json()
                if search_data and len(search_data) > 0:
                    dtxsid = search_data[0].get("dtxsid")
                    if dtxsid:
                        url = f"{base_url}/ccdapp1/chemical-detail/by-dtxsid/{dtxsid}"
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            return None
        
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            return response.json()
        
    except:
        pass
    
    return None


def _get_toxcast_bioactivity(chem_info: Dict, timeout: int) -> Dict:
    """Get ToxCast bioactivity data."""
    
    try:
        dtxsid = chem_info.get("dtxsid")
        if not dtxsid:
            return {"error": "No DTXSID available"}
        
        # ToxCast bioactivity endpoint
        url = f"https://comptox.epa.gov/dashboard-api/ccdapp1/bioactivity/by-dtxsid/{dtxsid}"
        
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            
            # Summarize key bioactivity metrics
            summary = {
                "total_assays": len(data) if isinstance(data, list) else 0,
                "active_assays": 0,
                "toxicity_targets": []
            }
            
            if isinstance(data, list):
                for assay in data:
                    if assay.get("hitCall") == 1:  # Active hit
                        summary["active_assays"] += 1
                        target = assay.get("assayComponentEndpointName", "Unknown")
                        if any(tox_term in target.lower() for tox_term in 
                               ["tox", "cyto", "geno", "mutagen", "carcino"]):
                            summary["toxicity_targets"].append(target)
            
            return summary
        
    except:
        pass
    
    return {"error": "Could not retrieve ToxCast bioactivity data"}


def _get_endpoint_predictions(chem_info: Dict, endpoints: List[str], timeout: int) -> Dict:
    """Get specific toxicity endpoint predictions."""
    
    predictions = {}
    dtxsid = chem_info.get("dtxsid")
    
    if not dtxsid:
        return {"error": "No DTXSID available for predictions"}
    
    # Simplified endpoint mapping - real implementation would use specific API endpoints
    endpoint_mapping = {
        "cytotoxicity": "Cell viability and cytotoxicity",
        "genotoxicity": "DNA damage and mutagenicity", 
        "endocrine": "Estrogen and androgen receptor activity",
        "neurotoxicity": "Neurotoxicity and neurodevelopment",
        "developmental": "Developmental and reproductive toxicity",
        "cardiotoxicity": "Cardiovascular toxicity",
        "hepatotoxicity": "Liver toxicity"
    }
    
    for endpoint in endpoints:
        if endpoint in endpoint_mapping:
            # In a real implementation, this would query specific prediction models
            predictions[endpoint] = {
                "description": endpoint_mapping[endpoint],
                "prediction": "Data would be retrieved from EPA models",
                "confidence": "Model confidence scores would be included"
            }
    
    return predictions


def _get_qsar_predictions(chem_info: Dict, timeout: int) -> Dict:
    """Get QSAR model predictions for toxicity."""
    
    try:
        dtxsid = chem_info.get("dtxsid")
        if not dtxsid:
            return {"error": "No DTXSID available"}
        
        # EPA provides OPERA QSAR predictions
        # This is a simplified placeholder - real implementation would access OPERA models
        qsar_data = {
            "models_available": [
                "Acute oral toxicity (LD50)",
                "Bioconcentration factor (BCF)", 
                "Skin sensitization",
                "Eye irritation",
                "Ames mutagenicity"
            ],
            "note": "QSAR predictions from EPA OPERA models would be retrieved here"
        }
        
        return qsar_data
        
    except:
        return {"error": "Could not retrieve QSAR predictions"}


def _format_toxcast_results(identifier: str, chem_info: Dict, results: Dict) -> str:
    """Format ToxCast results into readable summary."""
    
    output = f"=== TOXCAST ENDPOINT DATA ===\n"
    output += f"Query: {identifier}\n"
    
    if chem_info:
        output += f"DTXSID: {chem_info.get('dtxsid', 'N/A')}\n"
        output += f"CAS RN: {chem_info.get('casrn', 'N/A')}\n"
        output += f"Preferred Name: {chem_info.get('preferredName', 'N/A')}\n\n"
    
    # Format bioactivity data
    bioactivity = results.get("bioactivity", {})
    if "error" not in bioactivity:
        output += "TOXCAST BIOACTIVITY SUMMARY:\n"
        output += f"• Total assays tested: {bioactivity.get('total_assays', 0)}\n"
        output += f"• Active (positive) assays: {bioactivity.get('active_assays', 0)}\n"
        
        toxicity_targets = bioactivity.get("toxicity_targets", [])
        if toxicity_targets:
            output += f"• Toxicity-related targets ({len(toxicity_targets)}):\n"
            for target in toxicity_targets[:5]:  # Limit display
                output += f"  - {target}\n"
        output += "\n"
    else:
        output += "TOXCAST BIOACTIVITY: No data available\n\n"
    
    # Format endpoint predictions
    predictions = results.get("predictions", {})
    if "error" not in predictions:
        output += "TOXICITY ENDPOINT PREDICTIONS:\n"
        for endpoint, data in predictions.items():
            output += f"• {endpoint.title()}: {data.get('description', 'N/A')}\n"
        output += "\n"
    
    # Format QSAR data
    qsar = results.get("qsar", {})
    if "error" not in qsar:
        output += "QSAR MODEL PREDICTIONS:\n"
        models = qsar.get("models_available", [])
        for model in models[:5]:  # Limit display
            output += f"• {model}\n"
        output += f"• {qsar.get('note', '')}\n\n"
    
    output += "DATA SOURCE: EPA ToxCast & CompTox Chemicals Dashboard\n"
    output += "URL: https://comptox.epa.gov/dashboard/\n"
    output += "NOTE: ToxCast data represents high-throughput screening results.\n"
    output += "Positive results indicate biological activity but not necessarily adverse effects.\n"
    
    return output


# Additional utility functions for specific ToxCast analyses
def get_toxcast_summary_by_target(identifier: str, target_family: str = "nuclear_receptor") -> str:
    """
    Get ToxCast summary focused on specific target families.
    
    Args:
        identifier: Chemical identifier
        target_family: Target family ("nuclear_receptor", "kinase", "gpcr", etc.)
        
    Returns:
        Target-specific ToxCast summary
    """
    # Implementation would filter ToxCast data by target family
    return f"ToxCast {target_family} activity summary for {identifier}"


def compare_toxcast_activity(identifiers: List[str]) -> str:
    """
    Compare ToxCast activity profiles across multiple chemicals.
    
    Args:
        identifiers: List of chemical identifiers
        
    Returns:
        Comparative ToxCast activity analysis
    """
    # Implementation would retrieve and compare ToxCast profiles
    return f"Comparative ToxCast analysis for {len(identifiers)} chemicals"


if __name__ == "__main__":
    # Test the ToxCast integration
    toxcast_search = toxcast_endpoints_factory()
    
    # Test with a known chemical (bisphenol A)
    print("Testing ToxCast integration...")
    
    # BPA CAS number for testing
    test_cas = "80-05-7"  # Bisphenol A
    result = toxcast_search(test_cas, "casrn")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Test with benzene
    benzene_cas = "71-43-2"  # Benzene
    result = toxcast_search(benzene_cas, "casrn") 
    print(result)
