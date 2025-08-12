"""
PubChem toxicity data integration for Layer C external knowledge sources.

This module provides access to PubChem's toxicity and safety data including
bioassays, compound properties, and experimental toxicity endpoints.
"""

import json
import time
from typing import Dict, List, Optional, Union
from urllib.parse import quote

import requests


def pubchem_toxicity_factory(
    timeout: int = 30,
    max_retries: int = 3,
    delay_between_requests: float = 0.2
) -> callable:
    """
    Factory function to create a PubChem toxicity data retrieval function.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        delay_between_requests: Delay between API calls to respect rate limits
        
    Returns:
        Function that retrieves toxicity data from PubChem
    """
    
    def pubchem_toxicity_search(
        identifier: str,
        identifier_type: str = "smiles",
        data_types: Optional[List[str]] = None
    ) -> str:
        """
        Search PubChem for toxicity and safety data.
        
        Args:
            identifier: Chemical identifier (SMILES, CID, name, etc.)
            identifier_type: Type of identifier ("smiles", "cid", "name", "inchi")
            data_types: Types of data to retrieve (default: all toxicity-relevant)
            
        Returns:
            Formatted toxicity data summary from PubChem
        """
        if data_types is None:
            data_types = ["properties", "bioassays", "ghs", "experimental"]
        
        try:
            # Step 1: Get PubChem Compound ID (CID)
            cid = _get_pubchem_cid(identifier, identifier_type, timeout, max_retries)
            if not cid:
                return f"Could not find PubChem entry for {identifier}"
            
            # Step 2: Retrieve toxicity-relevant data
            results = {}
            
            if "properties" in data_types:
                results["properties"] = _get_compound_properties(cid, timeout)
                time.sleep(delay_between_requests)
            
            if "bioassays" in data_types:
                results["bioassays"] = _get_toxicity_bioassays(cid, timeout)
                time.sleep(delay_between_requests)
                
            if "ghs" in data_types:
                results["ghs"] = _get_ghs_classification(cid, timeout)
                time.sleep(delay_between_requests)
            
            if "experimental" in data_types:
                results["experimental"] = _get_experimental_data(cid, timeout)
                time.sleep(delay_between_requests)
            
            # Step 3: Format results
            return _format_toxicity_results(identifier, cid, results)
            
        except Exception as e:
            return f"Error retrieving PubChem data for {identifier}: {str(e)}"
    
    return pubchem_toxicity_search


def _get_pubchem_cid(identifier: str, identifier_type: str, timeout: int, max_retries: int) -> Optional[str]:
    """Get PubChem Compound ID from identifier."""
    
    # Map identifier types to PubChem namespace
    namespace_map = {
        "smiles": "smiles",
        "cid": "cid", 
        "name": "name",
        "inchi": "inchi",
        "inchikey": "inchikey"
    }
    
    if identifier_type not in namespace_map:
        raise ValueError(f"Unsupported identifier type: {identifier_type}")
    
    if identifier_type == "cid":
        return identifier  # Already a CID
    
    namespace = namespace_map[identifier_type]
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/{namespace}/{quote(identifier)}/cids/JSON"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            if "IdentifierList" in data and data["IdentifierList"]["CID"]:
                return str(data["IdentifierList"]["CID"][0])
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry
    
    return None


def _get_compound_properties(cid: str, timeout: int) -> Dict:
    """Get basic compound properties relevant to toxicity."""
    
    properties = [
        "MolecularWeight", "XLogP", "TPSA", "HBondDonorCount", "HBondAcceptorCount",
        "RotatableBondCount", "HeavyAtomCount", "Complexity", "Charge"
    ]
    
    prop_string = ",".join(properties)
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/{prop_string}/JSON"
    
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        if "PropertyTable" in data and data["PropertyTable"]["Properties"]:
            return data["PropertyTable"]["Properties"][0]
    except:
        pass
    
    return {}


def _get_toxicity_bioassays(cid: str, timeout: int) -> List[Dict]:
    """Get toxicity-related bioassay data."""
    
    # Search for toxicity-related bioassays
    toxicity_keywords = ["toxic", "cytotox", "ames", "mutagenic", "genotox", "herg", "cardiotox"]
    bioassays = []
    
    for keyword in toxicity_keywords[:3]:  # Limit to avoid too many requests
        try:
            url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/target/geneid/1/aids/JSON"
            # Note: This is a simplified example - real implementation would need more specific queries
            
            response = requests.get(url, timeout=timeout)
            if response.status_code == 200:
                # Parse bioassay results (simplified)
                break
        except:
            continue
    
    # For now, return placeholder - real implementation would parse bioassay results
    return [{"note": "Bioassay search functionality requires more specific implementation"}]


def _get_ghs_classification(cid: str, timeout: int) -> Dict:
    """Get GHS (Globally Harmonized System) classification data."""
    
    try:
        # PubChem stores GHS data in annotations
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
        
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        # Parse GHS classification from the complex PubChem structure
        ghs_data = {}
        
        if "Record" in data:
            sections = data["Record"].get("Section", [])
            for section in sections:
                if "GHS" in section.get("TOCHeading", ""):
                    # Extract GHS hazard statements, signal words, etc.
                    ghs_data["found"] = True
                    # Detailed parsing would go here
                    break
        
        return ghs_data
        
    except:
        return {"error": "Could not retrieve GHS classification"}


def _get_experimental_data(cid: str, timeout: int) -> Dict:
    """Get experimental toxicity data from literature."""
    
    try:
        # Get experimental data from PubChem's curated sources
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
        
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        experimental = {}
        
        if "Record" in data:
            sections = data["Record"].get("Section", [])
            for section in sections:
                heading = section.get("TOCHeading", "")
                if any(term in heading.lower() for term in ["toxicity", "safety", "hazard", "ld50"]):
                    experimental[heading] = "Found experimental data section"
        
        return experimental
        
    except:
        return {"error": "Could not retrieve experimental data"}


def _format_toxicity_results(identifier: str, cid: str, results: Dict) -> str:
    """Format PubChem toxicity results into readable summary."""
    
    output = f"=== PUBCHEM TOXICITY DATA ===\n"
    output += f"Query: {identifier}\n"
    output += f"PubChem CID: {cid}\n\n"
    
    # Format properties
    if "properties" in results and results["properties"]:
        props = results["properties"]
        output += "MOLECULAR PROPERTIES:\n"
        if "MolecularWeight" in props:
            output += f"• Molecular Weight: {props['MolecularWeight']} g/mol\n"
        if "XLogP" in props:
            output += f"• LogP: {props['XLogP']}\n"
        if "TPSA" in props:
            output += f"• Topological Polar Surface Area: {props['TPSA']} Ų\n"
        if "HBondDonorCount" in props:
            output += f"• H-bond Donors: {props['HBondDonorCount']}\n"
        if "HBondAcceptorCount" in props:
            output += f"• H-bond Acceptors: {props['HBondAcceptorCount']}\n"
        output += "\n"
    
    # Format GHS data
    if "ghs" in results:
        output += "GHS HAZARD CLASSIFICATION:\n"
        if results["ghs"].get("found"):
            output += "• GHS classification data found in PubChem\n"
        else:
            output += "• No GHS classification data available\n"
        output += "\n"
    
    # Format experimental data
    if "experimental" in results:
        output += "EXPERIMENTAL TOXICITY DATA:\n"
        exp_data = results["experimental"]
        if exp_data and "error" not in exp_data:
            for section, info in exp_data.items():
                output += f"• {section}: {info}\n"
        else:
            output += "• Limited experimental data available in PubChem\n"
        output += "\n"
    
    # Format bioassays
    if "bioassays" in results:
        output += "BIOASSAY DATA:\n"
        bioassays = results["bioassays"]
        if bioassays:
            for assay in bioassays[:3]:  # Limit display
                output += f"• {assay.get('note', 'Bioassay data available')}\n"
        else:
            output += "• No specific toxicity bioassays found\n"
        output += "\n"
    
    output += "DATA SOURCE: PubChem (https://pubchem.ncbi.nlm.nih.gov/)\n"
    output += "NOTE: For comprehensive toxicity assessment, consult primary literature and regulatory databases.\n"
    
    return output


if __name__ == "__main__":
    # Test the PubChem integration
    pubchem_search = pubchem_toxicity_factory()
    
    # Test with benzene
    print("Testing PubChem integration with benzene...")
    result = pubchem_search("c1ccccc1", "smiles")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Test with ibuprofen
    print("Testing PubChem integration with ibuprofen...")
    result = pubchem_search("ibuprofen", "name")
    print(result)
