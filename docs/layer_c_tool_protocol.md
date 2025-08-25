# Layer C Tool Development Protocol

## Overview

Layer C encompasses external knowledge sources - APIs, databases, and knowledge graphs - to provide access to large, dynamic, or regulated datasets that cannot reside fully within models. This protocol provides a standardized approach for developers to add new tools to Layer C.

## Design Principles

1. **Factory Pattern**: All Layer C tools use factory functions for consistent instantiation
2. **Error Handling**: Graceful degradation with informative error messages
3. **Rate Limiting**: Respect API rate limits with built-in delays
4. **Retry Logic**: Robust retry mechanisms for transient failures
5. **Formatted Output**: Consistent, human-readable output format
6. **Modular Design**: Separate data retrieval, processing, and formatting functions

## Standard Tool Structure

### 1. Module Header and Documentation

```python
"""
[Database/API Name] integration for Layer C external knowledge sources.

This module provides access to [specific data types] including
[list of key features and data types].
"""

import json
import time
from typing import Dict, List, Optional, Union
from urllib.parse import quote

import requests
```

### 2. Factory Function Template

```python
def [database_name]_[data_type]_factory(
    timeout: int = 30,
    max_retries: int = 3,
    delay_between_requests: float = 0.2,
    api_base_url: str = "https://api.example.com/v1"
) -> callable:
    """
    Factory function to create a [Database] [data type] retrieval function.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        delay_between_requests: Delay between API calls to respect rate limits
        api_base_url: Base URL for the API (if applicable)
        
    Returns:
        Function that retrieves [data type] from [Database]
    """
    
    def [database_name]_[data_type]_search(
        identifier: str,
        identifier_type: str = "default_type",
        data_types: Optional[List[str]] = None
    ) -> str:
        """
        Search [Database] for [data type] data.
        
        Args:
            identifier: [Type of identifier] (examples of supported formats)
            identifier_type: Type of identifier ("type1", "type2", "type3")
            data_types: Types of data to retrieve (default: all relevant types)
            
        Returns:
            Formatted [data type] summary from [Database]
        """
        if data_types is None:
            data_types = ["type1", "type2", "type3", "type4"]
        
        try:
            # Step 1: Get [Database] ID
            db_id = _get_[database_name]_id(identifier, identifier_type, timeout, max_retries)
            if not db_id:
                return f"Could not find [Database] entry for {identifier}"
            
            # Step 2: Retrieve data
            results = {}
            
            if "type1" in data_types:
                results["type1"] = _get_type1_data(db_id, timeout)
                time.sleep(delay_between_requests)
            
            if "type2" in data_types:
                results["type2"] = _get_type2_data(db_id, timeout)
                time.sleep(delay_between_requests)
            
            # Step 3: Format results
            return _format_[database_name]_results(identifier, db_id, results)
            
        except Exception as e:
            return f"Error retrieving [Database] data for {identifier}: {str(e)}"
    
    return [database_name]_[data_type]_search
```

### 3. Helper Functions Pattern

#### ID Resolution Function
```python
def _get_[database_name]_id(identifier: str, identifier_type: str, timeout: int, max_retries: int) -> Optional[str]:
    """Get [Database] ID from identifier."""
    
    # Map identifier types to [Database] namespace
    namespace_map = {
        "type1": "namespace1",
        "type2": "namespace2",
        "type3": "namespace3"
    }
    
    if identifier_type not in namespace_map:
        raise ValueError(f"Unsupported identifier type: {identifier_type}")
    
    if identifier_type == "direct_id":
        return identifier  # Already a [Database] ID
    
    namespace = namespace_map[identifier_type]
    url = f"https://api.example.com/search/{namespace}/{quote(identifier)}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            if "results" in data and data["results"]:
                return str(data["results"][0]["id"])
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Wait before retry
    
    return None
```

#### Data Retrieval Functions
```python
def _get_type1_data(db_id: str, timeout: int) -> Dict:
    """Get type1 data from [Database]."""
    
    try:
        url = f"https://api.example.com/data/{db_id}/type1"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("type1_data", {})
        
    except Exception:
        return {"error": "Could not retrieve type1 data"}

def _get_type2_data(db_id: str, timeout: int) -> List[Dict]:
    """Get type2 data from [Database]."""
    
    try:
        url = f"https://api.example.com/data/{db_id}/type2"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("type2_list", [])
        
    except Exception:
        return [{"error": "Could not retrieve type2 data"}]
```

#### Results Formatting Function
```python
def _format_[database_name]_results(identifier: str, db_id: str, results: Dict) -> str:
    """Format [Database] results into readable summary."""
    
    output = f"=== [DATABASE] [DATA TYPE] DATA ===\n"
    output += f"Query: {identifier}\n"
    output += f"[Database] ID: {db_id}\n\n"
    
    # Format type1 data
    type1_data = results.get("type1", {})
    if "error" not in type1_data:
        output += "TYPE1 DATA:\n"
        # Add specific formatting logic
        output += f"• Key field: {type1_data.get('key_field', 'N/A')}\n"
        output += "\n"
    
    # Format type2 data
    type2_data = results.get("type2", [])
    if type2_data and "error" not in type2_data[0]:
        output += "TYPE2 DATA:\n"
        for item in type2_data[:5]:  # Limit display
            output += f"• {item.get('description', 'N/A')}\n"
        output += "\n"
    
    output += "DATA SOURCE: [Database Name] (https://database-url.com/)\n"
    output += "NOTE: [Important usage note or disclaimer]\n"
    
    return output
```

### 4. Testing Section

```python
if __name__ == "__main__":
    # Test the [Database] integration
    [database_name]_search = [database_name]_[data_type]_factory()
    
    # Test with example data
    print("Testing [Database] integration...")
    result = [database_name]_search("test_identifier", "test_type")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Test with another example
    print("Testing [Database] integration with different data...")
    result = [database_name]_search("another_identifier", "another_type")
    print(result)
```

## Implementation Checklist

### ✅ Required Components

- [ ] **Module documentation** with clear description
- [ ] **Factory function** with configurable parameters
- [ ] **Main search function** with proper error handling
- [ ] **ID resolution function** with retry logic
- [ ] **Data retrieval functions** for each data type
- [ ] **Results formatting function** with consistent output
- [ ] **Testing section** with example usage
- [ ] **Rate limiting** with configurable delays
- [ ] **Error handling** with informative messages
- [ ] **Type hints** for all function parameters

### ✅ Best Practices

- [ ] **Consistent naming**: Use `[database_name]_[data_type]_factory` pattern
- [ ] **Parameter validation**: Check for valid identifier types
- [ ] **Graceful degradation**: Return informative error messages
- [ ] **Rate limiting**: Respect API limits with built-in delays
- [ ] **Retry logic**: Handle transient network failures
- [ ] **Modular design**: Separate concerns into helper functions
- [ ] **Documentation**: Clear docstrings for all functions
- [ ] **Testing**: Include example usage in `__main__` section

## Integration Steps

### 1. Create the Tool File

Create a new file in `src/bio_reasoning/layers/c/` following the naming convention:
```
[database_name]_[data_type].py
```

### 2. Update Layer C Init File

Add the factory import to `src/bio_reasoning/layers/c/__init__.py`:

```python
from .[database_name]_[data_type] import [database_name]_[data_type]_factory

__all__ = [
    # ... existing imports ...
    "[database_name]_[data_type]_factory",
]
```

### 3. Register in Reasoning Modes

Add the tool to relevant reasoning modes in `src/bio_reasoning/reasoning/modes/`:

```python
# In the reasoning mode's __init__ method
from ...layers.c.[database_name]_[data_type] import [database_name]_[data_type]_factory

# Add to layer_c
[database_name]_search = [database_name]_[data_type]_factory()
layer_c.register([database_name]_search, name="[database_name]_[data_type]")
```

### 4. Add to Toxicology Instantiation (if applicable)

If the tool is relevant for toxicology analysis, add it to `src/bio_reasoning/reasoning/toxicology_instantiation.py`:

```python
from ..layers.c.[database_name]_[data_type] import [database_name]_[data_type]_factory

# Add to toxicology mode
[database_name]_search = [database_name]_[data_type]_factory()
base_mode.layer_c.register([database_name]_search, name="[database_name]_[data_type]")
```

## Example Implementation

Here's a complete example for a hypothetical "GeneDB" tool:

```python
"""
GeneDB integration for Layer C external knowledge sources.

This module provides access to GeneDB database for gene information,
expression data, and functional annotations.
"""

import json
import time
from typing import Dict, List, Optional, Union
from urllib.parse import quote

import requests


def genedb_gene_factory(
    timeout: int = 30,
    max_retries: int = 3,
    delay_between_requests: float = 0.2,
    api_base_url: str = "https://api.genedb.org/v1"
) -> callable:
    """
    Factory function to create a GeneDB gene data retrieval function.
    
    Args:
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        delay_between_requests: Delay between API calls to respect rate limits
        api_base_url: Base URL for the GeneDB API
        
    Returns:
        Function that retrieves gene data from GeneDB
    """
    
    def genedb_gene_search(
        identifier: str,
        identifier_type: str = "gene_symbol",
        data_types: Optional[List[str]] = None
    ) -> str:
        """
        Search GeneDB for gene information and expression data.
        
        Args:
            identifier: Gene identifier (symbol, ID, name, etc.)
            identifier_type: Type of identifier ("gene_symbol", "gene_id", "name")
            data_types: Types of data to retrieve (default: all gene data)
            
        Returns:
            Formatted gene data summary from GeneDB
        """
        if data_types is None:
            data_types = ["basic_info", "expression", "function", "pathways"]
        
        try:
            # Step 1: Get GeneDB gene ID
            gene_id = _get_genedb_gene_id(identifier, identifier_type, api_base_url, timeout, max_retries)
            if not gene_id:
                return f"Could not find GeneDB entry for {identifier}"
            
            # Step 2: Retrieve gene data
            results = {}
            
            if "basic_info" in data_types:
                results["basic_info"] = _get_gene_basic_info(gene_id, api_base_url, timeout)
                time.sleep(delay_between_requests)
            
            if "expression" in data_types:
                results["expression"] = _get_gene_expression(gene_id, api_base_url, timeout)
                time.sleep(delay_between_requests)
            
            if "function" in data_types:
                results["function"] = _get_gene_function(gene_id, api_base_url, timeout)
                time.sleep(delay_between_requests)
            
            if "pathways" in data_types:
                results["pathways"] = _get_gene_pathways(gene_id, api_base_url, timeout)
                time.sleep(delay_between_requests)
            
            # Step 3: Format results
            return _format_genedb_results(identifier, gene_id, results)
            
        except Exception as e:
            return f"Error retrieving GeneDB data for {identifier}: {str(e)}"
    
    return genedb_gene_search


def _get_genedb_gene_id(identifier: str, identifier_type: str, api_base_url: str, timeout: int, max_retries: int) -> Optional[str]:
    """Get GeneDB gene ID from identifier."""
    
    namespace_map = {
        "gene_symbol": "symbol",
        "gene_id": "id",
        "name": "name"
    }
    
    if identifier_type not in namespace_map:
        raise ValueError(f"Unsupported identifier type: {identifier_type}")
    
    if identifier_type == "gene_id":
        return identifier
    
    namespace = namespace_map[identifier_type]
    url = f"{api_base_url}/search/gene/{namespace}/{quote(identifier)}"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            data = response.json()
            if "genes" in data and data["genes"]:
                return str(data["genes"][0]["id"])
            
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)
    
    return None


def _get_gene_basic_info(gene_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get basic gene information from GeneDB."""
    
    try:
        url = f"{api_base_url}/gene/{gene_id}/basic"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("basic_info", {})
        
    except Exception:
        return {"error": "Could not retrieve basic gene information"}


def _get_gene_expression(gene_id: str, api_base_url: str, timeout: int) -> Dict:
    """Get gene expression data from GeneDB."""
    
    try:
        url = f"{api_base_url}/gene/{gene_id}/expression"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("expression_data", {})
        
    except Exception:
        return {"error": "Could not retrieve gene expression data"}


def _get_gene_function(gene_id: str, api_base_url: str, timeout: int) -> List[Dict]:
    """Get gene functional annotations from GeneDB."""
    
    try:
        url = f"{api_base_url}/gene/{gene_id}/function"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("functions", [])
        
    except Exception:
        return [{"error": "Could not retrieve gene function data"}]


def _get_gene_pathways(gene_id: str, api_base_url: str, timeout: int) -> List[Dict]:
    """Get gene pathway information from GeneDB."""
    
    try:
        url = f"{api_base_url}/gene/{gene_id}/pathways"
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        return data.get("pathways", [])
        
    except Exception:
        return [{"error": "Could not retrieve gene pathway data"}]


def _format_genedb_results(identifier: str, gene_id: str, results: Dict) -> str:
    """Format GeneDB results into readable summary."""
    
    output = f"=== GENEDB GENE DATA ===\n"
    output += f"Query: {identifier}\n"
    output += f"GeneDB ID: {gene_id}\n\n"
    
    # Format basic info
    basic_info = results.get("basic_info", {})
    if "error" not in basic_info:
        output += "BASIC GENE INFORMATION:\n"
        output += f"• Gene Symbol: {basic_info.get('symbol', 'N/A')}\n"
        output += f"• Gene Name: {basic_info.get('name', 'N/A')}\n"
        output += f"• Chromosome: {basic_info.get('chromosome', 'N/A')}\n"
        output += f"• Strand: {basic_info.get('strand', 'N/A')}\n"
        output += "\n"
    
    # Format expression data
    expression = results.get("expression", {})
    if "error" not in expression:
        output += "EXPRESSION DATA:\n"
        tissues = expression.get("tissues", [])
        for tissue in tissues[:5]:
            output += f"• {tissue.get('name', 'N/A')}: {tissue.get('level', 'N/A')}\n"
        output += "\n"
    
    # Format function data
    functions = results.get("function", [])
    if functions and "error" not in functions[0]:
        output += "FUNCTIONAL ANNOTATIONS:\n"
        for func in functions[:5]:
            output += f"• {func.get('term', 'N/A')}: {func.get('description', 'N/A')}\n"
        output += "\n"
    
    # Format pathway data
    pathways = results.get("pathways", [])
    if pathways and "error" not in pathways[0]:
        output += "PATHWAY INVOLVEMENT:\n"
        for pathway in pathways[:5]:
            output += f"• {pathway.get('name', 'N/A')}: {pathway.get('description', 'N/A')}\n"
        output += "\n"
    
    output += "DATA SOURCE: GeneDB (https://genedb.org/)\n"
    output += "NOTE: GeneDB data represents curated gene information from multiple sources.\n"
    
    return output


if __name__ == "__main__":
    # Test the GeneDB integration
    genedb_search = genedb_gene_factory()
    
    # Test with a gene symbol
    print("Testing GeneDB integration with TP53...")
    result = genedb_search("TP53", "gene_symbol")
    print(result)
    
    print("\n" + "="*50 + "\n")
    
    # Test with a gene name
    print("Testing GeneDB integration with tumor protein p53...")
    result = genedb_search("tumor protein p53", "name")
    print(result)
```

## Common Patterns and Tips

### 1. API Rate Limiting
Always include rate limiting to respect API limits:
```python
time.sleep(delay_between_requests)  # Between API calls
```

### 2. Error Handling
Provide informative error messages:
```python
except Exception as e:
    return f"Error retrieving [Database] data for {identifier}: {str(e)}"
```

### 3. Data Type Flexibility
Support multiple identifier types:
```python
identifier_type: str = "default_type"  # Allow different input formats
```

### 4. Configurable Data Retrieval
Allow users to specify which data types to retrieve:
```python
data_types: Optional[List[str]] = None  # Let users choose what to get
```

### 5. Consistent Output Format
Use a standardized output format:
```python
output = f"=== [DATABASE] [DATA TYPE] DATA ===\n"
output += f"Query: {identifier}\n"
# ... data formatting ...
output += "DATA SOURCE: [Database Name] (https://database-url.com/)\n"
output += "NOTE: [Important usage note]\n"
```

## Testing Your Tool

1. **Unit Testing**: Test individual functions with mock data
2. **Integration Testing**: Test with real API endpoints
3. **Error Testing**: Test error conditions and edge cases
4. **Performance Testing**: Verify rate limiting and timeout handling
5. **Documentation Testing**: Ensure examples work correctly

## Contributing Guidelines

1. Follow the established naming conventions
2. Include comprehensive documentation
3. Add proper error handling and logging
4. Test with real API endpoints
5. Update the relevant `__init__.py` files
6. Add to appropriate reasoning modes
7. Include example usage in the `__main__` section

This protocol ensures consistency across all Layer C tools while maintaining flexibility for different data sources and use cases.
