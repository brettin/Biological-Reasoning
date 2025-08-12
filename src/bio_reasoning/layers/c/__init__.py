"""
Layer C encompasses external knowledge sources - APIs, databases, and knowledge graphs - 
to provide access to large, dynamic, or regulated datasets that cannot reside fully within models.
"""

from .pubchem_toxicity import pubchem_toxicity_factory
from .toxcast_endpoints import toxcast_endpoints_factory  
from .chembl_mechanisms import chembl_mechanisms_factory

__all__ = [
    "pubchem_toxicity_factory",
    "toxcast_endpoints_factory",
    "chembl_mechanisms_factory",
]