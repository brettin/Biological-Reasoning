"""Configuration for external biological data resources."""

from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class ResourceType(Enum):
    GENOMIC = "genomic"
    PROTEOMIC = "proteomic"
    LITERATURE = "literature"
    PATHWAY = "pathway"
    DISEASE = "disease"
    DRUG = "drug"

@dataclass
class ResourceConfig:
    name: str
    base_url: str
    api_key: str
    resource_type: ResourceType
    data_types: List[str]
    update_frequency: str  # e.g., "daily", "weekly", "real-time"
    reliability_score: float  # 0-1
    rate_limit: Dict[str, int]  # e.g., {"requests_per_minute": 60}
    priority: int  # Higher number = higher priority

# External Resource Configurations
EXTERNAL_RESOURCES = {
    "opentargets": ResourceConfig(
        name="OpenTargets",
        base_url="https://platform-api.opentargets.io/v3",
        api_key="",  # To be set via environment variable
        resource_type=ResourceType.GENOMIC,
        data_types=["target-disease", "target-drug", "evidence"],
        update_frequency="weekly",
        reliability_score=0.9,
        rate_limit={"requests_per_minute": 60},
        priority=1
    ),
    "uniprot": ResourceConfig(
        name="UniProt",
        base_url="https://rest.uniprot.org",
        api_key="",  # To be set via environment variable
        resource_type=ResourceType.PROTEOMIC,
        data_types=["protein", "sequence", "function"],
        update_frequency="monthly",
        reliability_score=0.95,
        rate_limit={"requests_per_minute": 30},
        priority=2
    ),
    "pubmed": ResourceConfig(
        name="PubMed",
        base_url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils",
        api_key="",  # To be set via environment variable
        resource_type=ResourceType.LITERATURE,
        data_types=["publication", "abstract", "citation"],
        update_frequency="daily",
        reliability_score=0.85,
        rate_limit={"requests_per_minute": 10},
        priority=3
    ),
    "biorxiv": ResourceConfig(
        name="BioRxiv",
        base_url="https://api.biorxiv.org/details/biorxiv",  # Updated base URL
        api_key="",  # BioRxiv API is public, no key needed
        resource_type=ResourceType.LITERATURE,
        data_types=["preprint", "abstract", "citation"],
        update_frequency="real-time",
        reliability_score=0.8,
        rate_limit={"requests_per_minute": 20},
        priority=4
    ),
    "kegg": ResourceConfig(
        name="KEGG",
        base_url="https://rest.kegg.jp",
        api_key="",  # To be set via environment variable
        resource_type=ResourceType.PATHWAY,
        data_types=["pathway", "compound", "reaction"],
        update_frequency="monthly",
        reliability_score=0.8,
        rate_limit={"requests_per_minute": 20},
        priority=5
    )
}

# Resource Selection Rules
RESOURCE_SELECTION_RULES = {
    "target_disease": ["opentargets", "uniprot", "pubmed"],
    "protein_function": ["uniprot", "pubmed"],
    "pathway_analysis": ["kegg", "opentargets"],
    "literature_review": ["pubmed", "biorxiv"],
    "drug_target": ["opentargets", "uniprot"]
}

# Cache Configuration
CACHE_CONFIG = {
    "enabled": True,
    "ttl": 3600,  # Time to live in seconds
    "max_size": 1000  # Maximum number of cached items
} 