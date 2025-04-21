"""Resource manager for handling external biological data resources."""
from typing import Dict, Any, List, Optional
import requests
import time
from datetime import datetime, timedelta
from ..config.external_resources import (
    EXTERNAL_RESOURCES,
    RESOURCE_SELECTION_RULES,
    CACHE_CONFIG,
    ResourceType
)

class ResourceManager:
    """Manages access to external biological data resources."""
    
    def __init__(self):
        self.cache = {}
        self.last_request_time = {}
        self._initialize_request_times()
    
    def _initialize_request_times(self):
        """Initialize last request times for rate limiting."""
        for resource_id in EXTERNAL_RESOURCES:
            if resource_id != "biorxiv":  # Skip BioRxiv as it's handled by the biorxiv-api package
                self.last_request_time[resource_id] = datetime.min
    
    def select_resources(self, query_type: str, data_needs: Dict[str, Any]) -> List[str]:
        """Select appropriate resources based on query type and data needs."""
        selected_resources = []
        
        # Get base resources from selection rules
        if query_type in RESOURCE_SELECTION_RULES:
            selected_resources.extend(RESOURCE_SELECTION_RULES[query_type])
        
        # Add resources based on specific data needs
        for resource_id, config in EXTERNAL_RESOURCES.items():
            if resource_id != "biorxiv":  # Skip BioRxiv as it's handled by the biorxiv-api package
                if any(data_type in config.data_types for data_type in data_needs.get("data_types", [])):
                    if resource_id not in selected_resources:
                        selected_resources.append(resource_id)
        
        # Sort by priority
        selected_resources.sort(
            key=lambda x: EXTERNAL_RESOURCES[x].priority,
            reverse=True
        )
        
        return selected_resources
    
    def _check_rate_limit(self, resource_id: str) -> bool:
        """Check if we can make a request based on rate limits."""
        config = EXTERNAL_RESOURCES[resource_id]
        last_request = self.last_request_time[resource_id]
        min_interval = 60 / config.rate_limit["requests_per_minute"]
        
        return (datetime.now() - last_request).total_seconds() >= min_interval
    
    def _check_cache(self, resource_id: str, query_params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Check if the result is in cache."""
        if not CACHE_CONFIG["enabled"]:
            return None
        
        cache_key = f"{resource_id}:{str(query_params)}"
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if datetime.now() - cached_data["timestamp"] < timedelta(seconds=CACHE_CONFIG["ttl"]):
                return cached_data["data"]
        
        return None
    
    def _update_cache(self, resource_id: str, query_params: Dict[str, Any], data: Dict[str, Any]):
        """Update the cache with new data."""
        if not CACHE_CONFIG["enabled"]:
            return
        
        cache_key = f"{resource_id}:{str(query_params)}"
        self.cache[cache_key] = {
            "data": data,
            "timestamp": datetime.now()
        }
        
        # Enforce cache size limit
        if len(self.cache) > CACHE_CONFIG["max_size"]:
            oldest_key = min(self.cache.items(), key=lambda x: x[1]["timestamp"])[0]
            del self.cache[oldest_key]
    
    def query_resource(self, resource_id: str, endpoint: str, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query a specific external resource."""
        # Skip BioRxiv as it's handled by the biorxiv-api package
        if resource_id == "biorxiv":
            return {}
            
        # Check cache first
        cached_data = self._check_cache(resource_id, query_params)
        if cached_data is not None:
            return cached_data
        
        # Check rate limit
        if not self._check_rate_limit(resource_id):
            time.sleep(1)  # Wait before retrying
        
        config = EXTERNAL_RESOURCES[resource_id]
        
        try:
            # Make the API request with SSL verification disabled for certain resources
            verify_ssl = True
            if resource_id == "opentargets":
                verify_ssl = False
            
            response = requests.get(
                f"{config.base_url}/{endpoint}",
                params=query_params,
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {config.api_key}" if config.api_key else None
                },
                verify=verify_ssl
            )
            
            if response.status_code == 200:
                data = response.json()
                self._update_cache(resource_id, query_params, data)
                self.last_request_time[resource_id] = datetime.now()
                return data
            else:
                print(f"Error querying {resource_id}: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"Error querying {resource_id}: {e}")
            return {}
    
    def query_multiple_resources(self, resource_ids: List[str], endpoint: str, 
                               query_params: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Query multiple resources and combine results."""
        results = {}
        
        for resource_id in resource_ids:
            if resource_id in EXTERNAL_RESOURCES:
                results[resource_id] = self.query_resource(resource_id, endpoint, query_params)
        
        return results 