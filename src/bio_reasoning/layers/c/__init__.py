"""
Layer C encompasses external knowledge sources - APIs, databases, and knowledge graphs - to provide access to large, dynamic, or regulated datasets that cannot reside fully within models.
"""

from .pubmed import pubmed_search_toxicity
from .toxcast import toxcast_endpoints
from .chembl import chembl_mechanism
from .pubchem import pubchem_summary

__all__ = [
    "pubmed_search_toxicity",
    "toxcast_endpoints", 
    "chembl_mechanism",
    "pubchem_summary",
]
