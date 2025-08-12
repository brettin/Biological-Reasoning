"""
ChEMBL mechanism data integration for Layer C external knowledge sources.

This module provides access to ChEMBL database for drug mechanism of action,
target interactions, and toxicity-related bioactivity data.
"""

import json
import time
from typing import Dict, List, Optional, Union
from urllib.parse import quote

import requests


def chembl_mechanisms_factory(
    timeout: int = 30,
    max_retries: int = 3,
    api_base_url: str = "https://www.ebi.ac.uk/chembl/api/data"
) -> callable:
    """
    Factory function to create a ChEMBL mechanism data retrieval function.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        api_base_url: ChEMBL API base URL
        
    Returns:
        Function that retrieves mechanism data from ChEMBL
    """
    
    def chembl_mechanism_search(
        identifier: str,
        identifier_type: str = "smiles",
        search_types: Optional[List[str]] = None
    ) -> str:
        """
        Search ChEMBL for mechanism of action and toxicity data.
        
        Args:
            identifier: Chemical identifier (SMILES, ChEMBL ID, name, etc.)
            identifier_type: Type of identifier ("smiles", "chembl_id", "name")
            search_types: Types of data to search ("mechanisms", "targets", "bioactivities", "admet")
            
        Returns:
            Formatted ChEMBL mechanism and toxicity data summary
        """
        if search_types is None:
            search_types = ["mechanisms", "targets", "bioactivities", "admet"]
        
        try:
            # Step 1: Get ChEMBL compound ID
            chembl_id = _get_chembl_compound_id(identifier, identifier_type, api_base_url, timeout)
            if not chembl_id:
                return f"Compound not found in ChEMBL: {identifier}"
            
            # Step 2: Retrieve different types of data
            results = {}
            
            if "mechanisms" in search_types:
                results["mechanisms"] = _get_mechanism_data(chembl_id, api_base_url, timeout)
                time.sleep(0.2)  # Rate limiting
            
            if "targets" in search_types:
                results["targets"] = _get_target_data(chembl_id, api_base_url, timeout)
                time.sleep(0.2)
            
            if "bioactivities" in search_types:
                results["bioactivities"] = _get_toxicity_bioactivities(chembl_id, api_base_url, timeout)
                time.sleep(0.2)
            
            if "admet" in search_types:
                results["admet"] = _get_admet_data(chembl_id, api_base_url, timeout)
                time.sleep(0.2)
            
            return _format_chembl_results(identifier, chembl_id, results)
            
        except Exception as e:
            return f"Error retrieving ChEMBL data for {identifier}: {str(e)}"
    
    return chembl_mechanism_search


def _get_chembl_compound_id(identifier: str, identifier_type: str, api_base_url: str, timeout: int) -> Optional[str]:
    """Get ChEMBL compound ID from identifier."""
    
    try:
        if identifier_type == "chembl_id":
            return identifier  # Already a ChEMBL ID
        
        elif identifier_type == "smiles":
            # Search by similarity using SMILES
            url = f"{api_base_url}/similarity/{quote(identifier)}/70"
            response = requests.get(url, timeout=timeout, headers={'Accept': 'application/json'})
            
            if response.status_code == 200:
                data = response.json()
                if "molecules" in data and data["molecules"]:
                    return data["molecules"][0]["molecule_chembl_id"]
        
        elif identifier_type == "name":
            # Search by molecule name
            url = f"{api_base_url}/molecule/search.json?q={quote(identifier)}"
            response = requests.get(url, timeout=timeout)
            
            if response.status_code == 200:
                data = response.json()
                if "molecules" in data and data["molecules"]:
                    for mol in data["molecules"]:
                        if mol.get("pref_name", "").lower() == identifier.lower():
                            return mol["molecule_chembl_id"]
                    # If no exact match, return first result
                    return data["molecules"][0]["molecule_chembl_id"]
        
    except Exception:
        pass
    
    return None


def _get_mechanism_data(chembl_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get mechanism of action data from ChEMBL."""
    
    try:
        url = f"{api_base_url}/mechanism.json?molecule_chembl_id={chembl_id}"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            mechanisms = data.get("mechanisms", [])
            
            # Summarize mechanism data
            summary = {
                "total_mechanisms": len(mechanisms),
                "mechanisms_list": []
            }
            
            for mech in mechanisms:
                mech_info = {
                    "mechanism_of_action": mech.get("mechanism_of_action"),
                    "target_name": mech.get("target_chembl_id"),
                    "action_type": mech.get("action_type"),
                    "mechanism_comment": mech.get("mechanism_comment")
                }
                summary["mechanisms_list"].append(mech_info)
            
            return summary
        
    except Exception:
        pass
    
    return {"error": "Could not retrieve mechanism data"}


def _get_target_data(chembl_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get target interaction data focusing on toxicity-relevant targets."""
    
    try:
        # Get activities for the compound
        url = f"{api_base_url}/activity.json?molecule_chembl_id={chembl_id}&limit=100"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            activities = data.get("activities", [])
            
            # Filter for toxicity-relevant targets
            toxicity_targets = []
            safety_targets = [
                "hERG", "CYP", "cytochrome", "BSEP", "Nav1.5", "Cav1.2", 
                "liver", "kidney", "cardiac", "hepato", "nephro", "neuro"
            ]
            
            target_summary = {}
            
            for activity in activities:
                target_name = activity.get("target_pref_name", "").lower()
                target_type = activity.get("target_type", "")
                
                # Check if target is safety-relevant
                is_safety_target = any(safety_term in target_name for safety_term in safety_targets)
                
                if is_safety_target:
                    activity_type = activity.get("standard_type")
                    activity_value = activity.get("standard_value")
                    activity_unit = activity.get("standard_units")
                    
                    if target_name not in target_summary:
                        target_summary[target_name] = []
                    
                    target_summary[target_name].append({
                        "activity_type": activity_type,
                        "value": activity_value,
                        "units": activity_unit,
                        "target_type": target_type
                    })
            
            return {
                "total_activities": len(activities),
                "safety_targets": target_summary,
                "safety_target_count": len(target_summary)
            }
        
    except Exception:
        pass
    
    return {"error": "Could not retrieve target data"}


def _get_toxicity_bioactivities(chembl_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get toxicity-related bioactivity data."""
    
    try:
        # Search for toxicity-related assays
        url = f"{api_base_url}/activity.json?molecule_chembl_id={chembl_id}"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            activities = data.get("activities", [])
            
            # Filter toxicity-related activities
            toxicity_keywords = [
                "toxic", "cytotox", "lethal", "ld50", "lc50", "viability", 
                "death", "mortality", "hepatotox", "cardiotox", "neurotox"
            ]
            
            toxicity_activities = []
            
            for activity in activities:
                assay_description = activity.get("assay_description", "").lower()
                activity_type = activity.get("standard_type", "").lower()
                
                is_toxicity = any(tox_term in assay_description or tox_term in activity_type 
                                for tox_term in toxicity_keywords)
                
                if is_toxicity:
                    toxicity_activities.append({
                        "assay_description": activity.get("assay_description"),
                        "activity_type": activity.get("standard_type"),
                        "value": activity.get("standard_value"),
                        "units": activity.get("standard_units"),
                        "organism": activity.get("assay_organism")
                    })
            
            return {
                "total_toxicity_assays": len(toxicity_activities),
                "toxicity_data": toxicity_activities[:10]  # Limit display
            }
        
    except Exception:
        pass
    
    return {"error": "Could not retrieve toxicity bioactivity data"}


def _get_admet_data(chembl_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) data."""
    
    try:
        # Get compound properties
        url = f"{api_base_url}/molecule/{chembl_id}.json"
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract ADMET-relevant properties
            admet_props = {}
            
            # Molecular properties affecting ADMET
            mol_props = data.get("molecule_properties", {})
            if mol_props:
                admet_props.update({
                    "molecular_weight": mol_props.get("full_mwt"),
                    "logp": mol_props.get("alogp"),
                    "hbd": mol_props.get("hbd"),  # H-bond donors
                    "hba": mol_props.get("hba"),  # H-bond acceptors
                    "psa": mol_props.get("psa"),  # Polar surface area
                    "ro5_violations": mol_props.get("num_ro5_violations")
                })
            
            # Drug-like properties
            admet_props["max_phase"] = data.get("max_phase")  # Clinical development phase
            admet_props["therapeutic_flag"] = data.get("therapeutic_flag")
            
            return admet_props
        
    except Exception:
        pass
    
    return {"error": "Could not retrieve ADMET data"}


def _format_chembl_results(identifier: str, chembl_id: str, results: Dict) -> str:
    """Format ChEMBL results into readable summary."""
    
    output = f"=== ChEMBL MECHANISM & TOXICITY DATA ===\n"
    output += f"Query: {identifier}\n"
    output += f"ChEMBL ID: {chembl_id}\n\n"
    
    # Format mechanism data
    mechanisms = results.get("mechanisms", {})
    if "error" not in mechanisms:
        output += "MECHANISM OF ACTION:\n"
        mech_list = mechanisms.get("mechanisms_list", [])
        if mech_list:
            for i, mech in enumerate(mech_list[:5], 1):  # Limit display
                output += f"{i}. {mech.get('mechanism_of_action', 'Unknown mechanism')}\n"
                if mech.get("action_type"):
                    output += f"   Action Type: {mech['action_type']}\n"
                if mech.get("target_name"):
                    output += f"   Target: {mech['target_name']}\n"
        else:
            output += "• No mechanism of action data available\n"
        output += "\n"
    
    # Format target data
    targets = results.get("targets", {})
    if "error" not in targets:
        output += "SAFETY-RELEVANT TARGET INTERACTIONS:\n"
        safety_targets = targets.get("safety_targets", {})
        if safety_targets:
            output += f"• Found interactions with {len(safety_targets)} safety-relevant targets:\n"
            for target_name, activities in list(safety_targets.items())[:5]:
                output += f"  - {target_name.title()}: {len(activities)} activities\n"
        else:
            output += "• No safety-relevant target interactions found\n"
        output += "\n"
    
    # Format toxicity bioactivities
    bioactivities = results.get("bioactivities", {})
    if "error" not in bioactivities:
        output += "TOXICITY BIOACTIVITY DATA:\n"
        tox_count = bioactivities.get("total_toxicity_assays", 0)
        if tox_count > 0:
            output += f"• Found {tox_count} toxicity-related assays\n"
            tox_data = bioactivities.get("toxicity_data", [])
            for assay in tox_data[:3]:  # Show first 3
                assay_desc = assay.get("assay_description", "Unknown assay")
                if len(assay_desc) > 80:
                    assay_desc = assay_desc[:80] + "..."
                output += f"  - {assay_desc}\n"
        else:
            output += "• No specific toxicity assays found\n"
        output += "\n"
    
    # Format ADMET data
    admet = results.get("admet", {})
    if "error" not in admet:
        output += "ADMET PROPERTIES:\n"
        if admet.get("molecular_weight"):
            output += f"• Molecular Weight: {admet['molecular_weight']} g/mol\n"
        if admet.get("logp"):
            output += f"• LogP: {admet['logp']}\n"
        if admet.get("hbd") is not None:
            output += f"• H-bond Donors: {admet['hbd']}\n"
        if admet.get("hba") is not None:
            output += f"• H-bond Acceptors: {admet['hba']}\n"
        if admet.get("psa"):
            output += f"• Polar Surface Area: {admet['psa']} Ų\n"
        if admet.get("ro5_violations") is not None:
            output += f"• Lipinski Rule of 5 Violations: {admet['ro5_violations']}\n"
        if admet.get("max_phase"):
            output += f"• Maximum Clinical Phase: {admet['max_phase']}\n"
        output += "\n"
    
    output += "DATA SOURCE: ChEMBL Database (https://www.ebi.ac.uk/chembl/)\n"
    output += "NOTE: ChEMBL data represents experimental bioactivity measurements.\n"
    output += "Interpret results in context of assay conditions and organism tested.\n"
    
    return output


# Additional utility functions
def get_chembl_drug_mechanisms(drug_name: str) -> str:
    """Get known drug mechanisms from ChEMBL for comparison."""
    chembl_search = chembl_mechanisms_factory()
    return chembl_search(drug_name, "name", ["mechanisms", "targets"])


def compare_chembl_safety_profiles(compounds: List[str]) -> str:
    """Compare safety target profiles across multiple compounds."""
    # Implementation would retrieve and compare safety profiles
    return f"Comparative ChEMBL safety analysis for {len(compounds)} compounds"


if __name__ == "__main__":
    # Test the ChEMBL integration
    chembl_search = chembl_mechanisms_factory()
    
    # Test with aspirin
    print("Testing ChEMBL integration with aspirin...")
    result = chembl_search("aspirin", "name")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Test with ibuprofen using SMILES
    print("Testing ChEMBL integration with ibuprofen SMILES...")
    ibuprofen_smiles = "CC(C)CC1=CC=C(C=C1)C(C)C(=O)O"
    result = chembl_search(ibuprofen_smiles, "smiles")
    print(result)
