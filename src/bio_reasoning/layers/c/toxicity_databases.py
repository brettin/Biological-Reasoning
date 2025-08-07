"""
Layer C: External Knowledge Tools for Toxicity Analysis

This module provides tools for accessing external databases and literature
sources relevant to molecular toxicity analysis.
"""

import logging
from typing import Dict, List, Optional
import httpx
import json

# Set up logging
layer_c_logger = logging.getLogger(__name__)


def pubmed_search_factory() -> callable:
    """
    Factory function to create a PubMed literature search tool.
    
    Returns:
        A function that searches PubMed for toxicity-related literature.
    """
    layer_c_logger.info("🏭 Creating PubMed search factory")
    
    def pubmed_search(query: str, max_results: int = 10) -> str:
        """
        Search PubMed for toxicity-related literature.
        
        Args:
            query: Search query (e.g., compound name + "toxicity" or structural terms)
            max_results: Maximum number of results to return
            
        Returns:
            Formatted search results
        """
        layer_c_logger.info(f"📚 PubMed search called with query: {query}")
        
        try:
            # Using NCBI E-utilities API
            base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
            
            # Search for articles
            search_url = f"{base_url}/esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json",
                "sort": "relevance"
            }
            
            layer_c_logger.info(f"🔍 Searching PubMed with URL: {search_url}")
            response = httpx.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            
            search_data = response.json()
            id_list = search_data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                layer_c_logger.warning("⚠️ No PubMed results found")
                return f"No PubMed articles found for query: {query}"
            
            layer_c_logger.info(f"📄 Found {len(id_list)} PubMed articles")
            
            # Get article details
            fetch_url = f"{base_url}/efetch.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "xml",
                "rettype": "abstract"
            }
            
            layer_c_logger.info("📥 Fetching article details...")
            fetch_response = httpx.get(fetch_url, params=fetch_params, timeout=30)
            fetch_response.raise_for_status()
            
            # For now, return a summary of found articles
            # In a full implementation, we'd parse the XML and extract titles/abstracts
            result = f"Found {len(id_list)} PubMed articles for '{query}':\n"
            result += f"Article IDs: {', '.join(id_list[:5])}"
            if len(id_list) > 5:
                result += f" and {len(id_list) - 5} more..."
            
            layer_c_logger.info(f"✅ PubMed search completed successfully")
            return result
            
        except Exception as e:
            layer_c_logger.error(f"❌ PubMed search failed: {e}")
            return f"Error searching PubMed: {str(e)}"
    
    return pubmed_search


def pubchem_search_factory() -> callable:
    """
    Factory function to create a PubChem search tool.
    
    Returns:
        A function that searches PubChem for chemical information.
    """
    layer_c_logger.info("🏭 Creating PubChem search factory")
    
    def pubchem_search(compound_name: str, search_type: str = "name") -> str:
        """
        Search PubChem for compound information.
        
        Args:
            compound_name: Name, SMILES, or identifier of the compound
            search_type: Type of search ("name", "smiles", "cid")
            
        Returns:
            Formatted compound information
        """
        layer_c_logger.info(f"🔍 PubChem search called with: {compound_name}, type: {search_type}")
        
        try:
            # Using PubChem PUG REST API
            base_url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
            
            if search_type == "name":
                search_url = f"{base_url}/compound/name/{compound_name}/JSON"
            elif search_type == "smiles":
                search_url = f"{base_url}/compound/smiles/{compound_name}/JSON"
            elif search_type == "cid":
                search_url = f"{base_url}/compound/cid/{compound_name}/JSON"
            else:
                return f"Unsupported search type: {search_type}"
            
            layer_c_logger.info(f"🔍 Searching PubChem with URL: {search_url}")
            response = httpx.get(search_url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract basic information
            pc_compound = data.get("PC_Compounds", [{}])[0]
            props = pc_compound.get("props", [])
            
            # Try to get compound name from properties
            compound_name_display = compound_name
            for prop in props:
                if prop.get("urn", {}).get("label") == "IUPAC Name":
                    compound_name_display = prop.get("value", {}).get("sval", compound_name)
                    break
                elif prop.get("urn", {}).get("label") == "Title":
                    compound_name_display = prop.get("value", {}).get("sval", compound_name)
                    break
            
            result = f"PubChem Information for {compound_name_display}:\n"
            if search_type == "smiles":
                result += f"SMILES: {compound_name}\n"
            
            # Extract molecular weight, formula, etc.
            for prop in props:
                if prop.get("urn", {}).get("label") == "Molecular Weight":
                    mw = prop.get("value", {}).get("sval", "N/A")
                    result += f"Molecular Weight: {mw}\n"
                elif prop.get("urn", {}).get("label") == "Molecular Formula":
                    formula = prop.get("value", {}).get("sval", "N/A")
                    result += f"Molecular Formula: {formula}\n"
                elif prop.get("urn", {}).get("label") == "Canonical SMILES":
                    smiles = prop.get("value", {}).get("sval", "N/A")
                    result += f"Canonical SMILES: {smiles}\n"
            
            # Get toxicity information if available
            if search_type == "smiles":
                # For SMILES search, try to get toxicity data using the found compound name
                tox_url = f"{base_url}/compound/name/{compound_name_display}/property/Toxicity/JSON"
            else:
                tox_url = f"{base_url}/compound/name/{compound_name}/property/Toxicity/JSON"
            
            try:
                tox_response = httpx.get(tox_url, timeout=30)
                if tox_response.status_code == 200:
                    tox_data = tox_response.json()
                    result += "\nToxicity Information Available\n"
            except:
                result += "\nNo toxicity information found\n"
            
            layer_c_logger.info(f"✅ PubChem search completed successfully")
            return result
            
        except Exception as e:
            layer_c_logger.error(f"❌ PubChem search failed: {e}")
            return f"Error searching PubChem: {str(e)}"
    
    return pubchem_search


def chembl_search_factory() -> callable:
    """
    Factory function to create a ChEMBL search tool.
    
    Returns:
        A function that searches ChEMBL for bioactivity data.
    """
    layer_c_logger.info("🏭 Creating ChEMBL search factory")
    
    def chembl_search(compound_name: str, target_type: str = "toxicity", search_type: str = "name") -> str:
        """
        Search ChEMBL for bioactivity and toxicity data.
        
        Args:
            compound_name: Name or SMILES of the compound
            target_type: Type of target data to search for
            search_type: Type of search ("name" or "smiles")
            
        Returns:
            Formatted bioactivity data
        """
        layer_c_logger.info(f"🧪 ChEMBL search called with: {compound_name}, target: {target_type}, type: {search_type}")
        
        try:
            # Using ChEMBL REST API
            base_url = "https://www.ebi.ac.uk/chembl/api/data"
            
            # Search for compound
            search_url = f"{base_url}/molecule.json"
            
            if search_type == "smiles":
                # For SMILES search, use exact SMILES match
                params = {
                    "molecule_structures__canonical_smiles": compound_name,
                    "limit": 5
                }
            else:
                # For name search, use contains match
                params = {
                    "molecule_structures__canonical_smiles__icontains": compound_name,
                    "limit": 5
                }
            
            layer_c_logger.info(f"🔍 Searching ChEMBL with URL: {search_url}")
            response = httpx.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            molecules = data.get("molecules", [])
            
            if not molecules:
                layer_c_logger.warning("⚠️ No ChEMBL results found")
                return f"No ChEMBL data found for compound: {compound_name}"
            
            layer_c_logger.info(f"📄 Found {len(molecules)} ChEMBL molecules")
            
            result = f"ChEMBL Data for {compound_name}:\n"
            if search_type == "smiles":
                result += f"SMILES: {compound_name}\n"
            
            for mol in molecules[:3]:  # Limit to first 3 results
                mol_id = mol.get("molecule_chembl_id", "N/A")
                mol_name = mol.get("pref_name", "N/A")
                mol_smiles = mol.get("molecule_structures", {}).get("canonical_smiles", "N/A")
                result += f"\nMolecule: {mol_name} (ChEMBL ID: {mol_id})\n"
                if mol_smiles != "N/A":
                    result += f"SMILES: {mol_smiles}\n"
                
                # Get bioactivity data
                activity_url = f"{base_url}/activity.json"
                activity_params = {
                    "molecule_chembl_id": mol_id,
                    "limit": 3
                }
                
                try:
                    activity_response = httpx.get(activity_url, params=activity_params, timeout=30)
                    if activity_response.status_code == 200:
                        activity_data = activity_response.json()
                        activities = activity_data.get("activities", [])
                        
                        if activities:
                            result += "Bioactivity Data:\n"
                            for act in activities[:2]:
                                target = act.get("target_chembl_id", "N/A")
                                value = act.get("standard_value", "N/A")
                                unit = act.get("standard_units", "")
                                result += f"  Target: {target}, Value: {value} {unit}\n"
                except Exception as e:
                    layer_c_logger.warning(f"⚠️ Could not fetch activity data: {e}")
            
            layer_c_logger.info(f"✅ ChEMBL search completed successfully")
            return result
            
        except Exception as e:
            layer_c_logger.error(f"❌ ChEMBL search failed: {e}")
            return f"Error searching ChEMBL: {str(e)}"
    
    return chembl_search


def toxcast_search_factory() -> callable:
    """
    Factory function to create a ToxCast/Tox21 search tool.
    
    Returns:
        A function that searches EPA toxicity databases.
    """
    layer_c_logger.info("🏭 Creating ToxCast search factory")
    
    def toxcast_search(compound_name: str, endpoint_type: str = "all") -> str:
        """
        Search ToxCast/Tox21 for toxicity screening data.
        
        Args:
            compound_name: Name of the compound
            endpoint_type: Type of toxicity endpoint to search for
            
        Returns:
            Formatted toxicity screening data
        """
        layer_c_logger.info(f"🧬 ToxCast search called with: {compound_name}, endpoint: {endpoint_type}")
        
        try:
            # Using EPA CompTox Dashboard API
            base_url = "https://comptox.epa.gov/dashboard-api"
            
            # Search for compound
            search_url = f"{base_url}/search"
            params = {
                "search": compound_name,
                "type": "chemical"
            }
            
            layer_c_logger.info(f"🔍 Searching ToxCast with URL: {search_url}")
            response = httpx.get(search_url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            if not results:
                layer_c_logger.warning("⚠️ No ToxCast results found")
                return f"No ToxCast data found for compound: {compound_name}"
            
            layer_c_logger.info(f"📄 Found {len(results)} ToxCast results")
            
            result = f"ToxCast/Tox21 Data for {compound_name}:\n"
            
            for chem in results[:3]:  # Limit to first 3 results
                dtxsid = chem.get("dtxsid", "N/A")
                casrn = chem.get("casrn", "N/A")
                result += f"\nChemical: {chem.get('name', 'N/A')}\n"
                result += f"DTXSID: {dtxsid}\n"
                result += f"CASRN: {casrn}\n"
                
                # Get toxicity data
                if dtxsid != "N/A":
                    tox_url = f"{base_url}/chemical/{dtxsid}/toxicity"
                    try:
                        tox_response = httpx.get(tox_url, timeout=30)
                        if tox_response.status_code == 200:
                            tox_data = tox_response.json()
                            assays = tox_data.get("assays", [])
                            
                            if assays:
                                result += "Toxicity Assays:\n"
                                for assay in assays[:3]:
                                    assay_name = assay.get("assay_name", "N/A")
                                    result_type = assay.get("result_type", "N/A")
                                    result += f"  {assay_name}: {result_type}\n"
                    except Exception as e:
                        layer_c_logger.warning(f"⚠️ Could not fetch toxicity data: {e}")
            
            layer_c_logger.info(f"✅ ToxCast search completed successfully")
            return result
            
        except Exception as e:
            layer_c_logger.error(f"❌ ToxCast search failed: {e}")
            return f"Error searching ToxCast: {str(e)}"
    
    return toxcast_search 