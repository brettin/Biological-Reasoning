from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from .resource_manager import ResourceManager
from ..external_resources import EXTERNAL_RESOURCES
import urllib.parse
import requests
import warnings

# Suppress the InsecureRequestWarning when making requests with verify=False
warnings.filterwarnings("ignore", message="Unverified HTTPS request")

class ExternalRepository(ABC):
    """Base class for external knowledge repositories."""
    
    def __init__(self):
        self.resource_manager = ResourceManager()
    
    @abstractmethod
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query the external repository."""
        pass
    
    def _create_standard_response(self, query_params: Dict[str, Any], results: Any, 
                                status: str = "success", error: str = None, count: int = None) -> Dict[str, Any]:
        """Create a standardized response format."""
        if results is None:
            results = []
        
        if count is None and isinstance(results, list):
            count = len(results)
        elif count is None:
            count = 0
            
        response = {
            "query": query_params,
            "results": results,
            "status": status,
            "count": count
        }
        
        if error:
            response["error"] = error
            
        return response

class OpenTargetsRepository(ExternalRepository):
    """Repository for OpenTargets Platform data."""
    
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query OpenTargets Platform."""
        try:
            # Extract query parameters
            query_term = query_params.get("query", "")
            target_id = query_params.get("target", "")
            disease_id = query_params.get("disease", "")
            
            # If no specific target/disease IDs provided but we have a query term,
            # try to use it as a search term for targets or diseases
            if not target_id and not disease_id and query_term:
                # Try to query directly with the search term
                endpoint = "public/search"
                search_params = {
                    "q": query_term,
                    "size": 10
                }
                
                # Direct API request with specific params and SSL verification disabled
                results = self._direct_api_request(endpoint, search_params)
                
                return self._create_standard_response(
                    query_params, 
                    results,
                    "success" if results else "error",
                    None if results else "No results found",
                    len(results.get("data", [])) if results and "data" in results else 0
                )
            
            # If we have target or disease IDs, query for associations
            elif target_id or disease_id:
                # Use evidence endpoint for target-disease associations
                endpoint = "public/association/filter"
                assoc_params = {
                    "target": target_id if target_id else None,
                    "disease": disease_id if disease_id else None,
                    "size": 100
                }
                
                # Remove None values from params
                assoc_params = {k: v for k, v in assoc_params.items() if v is not None}
                
                # Direct API request with specific params and SSL verification disabled
                results = self._direct_api_request(endpoint, assoc_params)
                
                return self._create_standard_response(
                    query_params, 
                    results,
                    "success" if results else "error",
                    None if results else "No results found",
                    len(results.get("data", [])) if results and "data" in results else 0
                )
            
            # Default case: use the resource manager
            else:
                selected_resources = self.resource_manager.select_resources(
                    "opentargets",
                    {
                        "data_types": ["target", "disease", "evidence"],
                        "target": target_id,
                        "disease": disease_id
                    }
                )
                
                results = self.resource_manager.query_resource(
                    "opentargets",
                    "platform/public/association/filter",
                    {
                        "q": query_term,
                        "size": 100
                    }
                )
                
                return self._create_standard_response(query_params, results)
                
        except Exception as e:
            print(f"Error querying opentargets: {e}")
            return self._create_standard_response(query_params, {}, "error", str(e), 0)
    
    def _direct_api_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a direct request to the OpenTargets API without using the resource manager."""
        try:
            # Get the base URL from the external resources configuration
            base_url = EXTERNAL_RESOURCES["opentargets"].base_url
            
            # Build the full URL
            url = f"{base_url}/{endpoint}"
            
            # Make the request with SSL verification disabled
            #response = requests.get(
            #    url,
            #    params=params,
            #    headers={"Accept": "application/json"},
            #    verify=False  # Disable SSL verification
            #)
            print("Fix call to OpenTargets")
            #if response.status_code == 200:
            #    return response.json()
            #else:
            #    print(f"OpenTargets API returned status code {response.status_code}")
            #    return {}
            return {}    
        except Exception as e:
            print(f"Error in direct API request to OpenTargets: {e}")
            return {}

class TargetDiseaseRepository(ExternalRepository):
    """Repository for target-disease associations."""
    
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query target-disease associations."""
        try:
            # Select appropriate resources
            resource_ids = self.resource_manager.select_resources(
                "target_disease",
                {
                    "data_types": ["target-disease", "evidence"],
                    "target": query_params.get("target"),
                    "disease": query_params.get("disease")
                }
            )
            
            # Query selected resources
            results = self.resource_manager.query_multiple_resources(
                resource_ids,
                "evidence/filter",
                {
                    "target": query_params.get("target"),
                    "disease": query_params.get("disease"),
                    "size": 100
                }
            )
            
            return self._create_standard_response(query_params, results)
        except Exception as e:
            return self._create_standard_response(query_params, {}, "error", str(e), 0)

class ProteinFunctionRepository(ExternalRepository):
    """Repository for protein function information."""
    
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query protein function information."""
        try:
            # Select appropriate resources
            resource_ids = self.resource_manager.select_resources(
                "protein_function",
                {
                    "data_types": ["protein", "function"],
                    "protein_id": query_params.get("protein_id")
                }
            )
            
            # Query selected resources
            results = self.resource_manager.query_multiple_resources(
                resource_ids,
                "uniprotkb/search",
                {
                    "query": f"accession:{query_params.get('protein_id')}",
                    "format": "json",
                    "fields": "accession,id,gene_names,protein_name,go,keywords"
                }
            )
            
            return self._create_standard_response(query_params, results)
        except Exception as e:
            return self._create_standard_response(query_params, {}, "error", str(e), 0)

class PubMedRepository(ExternalRepository):
    """Repository for PubMed literature search."""
    
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query PubMed database."""
        try:
            # Format the query for better results
            search_query = query_params.get("query", "")
            formatted_query = search_query.replace("What is", "").replace("what is", "")
            formatted_query = formatted_query.strip(" ?")
            
            # Query PubMed API
            results = self.resource_manager.query_resource(
                "pubmed",
                "esearch.fcgi",
                {
                    "db": "pubmed",
                    "term": formatted_query,
                    "retmax": 10,
                    "retmode": "json",
                    "sort": "relevance"
                }
            )
            
            # Count the number of results
            count = 0
            if results and "esearchresult" in results and "count" in results["esearchresult"]:
                count = int(results["esearchresult"]["count"])
                
            return self._create_standard_response(query_params, results, count=count)
        except Exception as e:
            print(f"Error querying PubMed: {e}")
            return self._create_standard_response(query_params, {}, "error", str(e), 0)

class BioRxivRepository(ExternalRepository):
    """Repository for BioRxiv preprints."""
    
    def query(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query BioRxiv preprints."""
        try:
            # Get search parameters
            search_query = query_params.get("query", "")
            # Use a wider date range to capture more relevant papers
            start_date = '2010-01-01'  # Start of date range
            end_date = '2024-12-31'    # End of date range
            cursor = 0                  # Starting index
            limit = 10                  # Maximum records
            
            # URL encode the search term
            encoded_query = urllib.parse.quote(search_query)
            
            # Construct the URL
            url = (
                f"https://api.biorxiv.org/details/biorxiv/"
                f"{start_date}/{end_date}/{cursor}/{limit}"
                f"?query={encoded_query}"
            )
            
            # Make the HTTP GET request
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                # Extract and format the results
                collection = data.get("collection", [])
                formatted_results = []
                
                for item in collection:
                    formatted_results.append({
                        "title": item.get("title", ""),
                        "abstract": item.get("abstract", ""),
                        "doi": item.get("doi", ""),
                        "published": item.get("published", ""),
                        "authors": item.get("authors", []),
                        "source": "biorxiv"
                    })
                
                return self._create_standard_response(query_params, formatted_results)
            else:
                return self._create_standard_response(
                    query_params, 
                    [], 
                    "error", 
                    f"BioRxiv API returned status code {response.status_code}", 
                    0
                )
        except Exception as e:
            return self._create_standard_response(query_params, [], "error", str(e), 0) 