from typing import Dict, Any, List
from abc import ABC, abstractmethod
from bio_reasoning.layers.layer_a import BiologicalKnowledgeStore
from bio_reasoning.layers.layer_b import GenomicSequenceAnalyzer, ImagingAnalyzer
from bio_reasoning.layers.layer_c import OpenTargetsRepository, PubMedRepository, BioRxivRepository
from bio_reasoning.config import SYSTEM_MESSAGES

class ReasoningMode(ABC):
    """Abstract base class for biological reasoning modes."""
    
    def __init__(self):
        self.layer_a = BiologicalKnowledgeStore()
        self.layer_b_genomic = GenomicSequenceAnalyzer()
        self.layer_b_imaging = ImagingAnalyzer()
        self.layer_c_targets = OpenTargetsRepository()
        self.layer_c_pubmed = PubMedRepository()
        self.layer_c_biorxiv = BioRxivRepository()
    
    @abstractmethod
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform reasoning on a biological query."""
        pass

    def get_prompt(self, query: str, data: str = "") -> str:
        """Get the reasoning prompt for this mode."""
        mode_name = self.__class__.__name__.lower().replace("reasoning", "")
        return REASONING_PROMPTS[mode_name].format(question=query, data=data)

class PhylogeneticReasoning(ReasoningMode):
    """Reasoning based on evolutionary relationships."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform phylogenetic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Analyze sequences using Layer B
        sequence_analysis = self.layer_b_genomic.analyze(query)
        
        # Get evolutionary data from Layer C
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} phylogenetic analysis"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} phylogenetic analysis"})
        
        return {
            "reasoning_mode": "phylogenetic",
            "knowledge": knowledge,
            "sequence_analysis": sequence_analysis,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class TeleonomicReasoning(ReasoningMode):
    """Reasoning based on function and purpose."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform teleonomic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get functional data from OpenTargets
        target_data = self.layer_c_targets.query({"query": query})
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} function"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} function"})
        
        return {
            "reasoning_mode": "teleonomic",
            "knowledge": knowledge,
            "target_data": target_data,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class MechanisticReasoning(ReasoningMode):
    """Reasoning based on causal mechanisms."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform mechanistic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get mechanistic data from OpenTargets
        target_data = self.layer_c_targets.query({"query": query})
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} mechanism"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} mechanism"})
        
        return {
            "reasoning_mode": "mechanistic",
            "knowledge": knowledge,
            "target_data": target_data,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class TradeoffReasoning(ReasoningMode):
    """Reasoning based on biological trade-offs."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform trade-off reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} trade-off"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} trade-off"})
        
        return {
            "reasoning_mode": "tradeoff",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class SystemsReasoning(ReasoningMode):
    """Reasoning based on systems biology principles."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform systems biology reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get network data from OpenTargets
        target_data = self.layer_c_targets.query({"query": query})
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} systems biology"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} systems biology"})
        
        return {
            "reasoning_mode": "systems",
            "knowledge": knowledge,
            "target_data": target_data,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class ProbabilisticReasoning(ReasoningMode):
    """Reasoning based on probabilistic models."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform probabilistic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} probability"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} probability"})
        
        return {
            "reasoning_mode": "probabilistic",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class SpatialReasoning(ReasoningMode):
    """Reasoning based on spatial organization."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform spatial reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Analyze images using Layer B
        image_analysis = self.layer_b_imaging.analyze(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} spatial"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} spatial"})
        
        return {
            "reasoning_mode": "spatial",
            "knowledge": knowledge,
            "image_analysis": image_analysis,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class TemporalReasoning(ReasoningMode):
    """Reasoning based on temporal dynamics."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform temporal reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} temporal dynamics"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} temporal dynamics"})
        
        return {
            "reasoning_mode": "temporal",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class HomeostaticReasoning(ReasoningMode):
    """Reasoning based on homeostasis and feedback loops."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform homeostatic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} homeostasis"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} homeostasis"})
        
        return {
            "reasoning_mode": "homeostatic",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class DevelopmentalReasoning(ReasoningMode):
    """Reasoning based on developmental biology."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform developmental reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} development"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} development"})
        
        return {
            "reasoning_mode": "developmental",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

class ComparativeReasoning(ReasoningMode):
    """Reasoning based on comparative biology."""
    
    def reason(self, query: str, data: str = "") -> Dict[str, Any]:
        """Perform comparative reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)
        
        # Get supporting literature from PubMed and BioRxiv
        pubmed_literature = self.layer_c_pubmed.query({"query": f"{query} comparative"})
        biorxiv_literature = self.layer_c_biorxiv.query({"query": f"{query} comparative"})
        
        return {
            "reasoning_mode": "comparative",
            "knowledge": knowledge,
            "literature": {
                "pubmed": pubmed_literature,
                "biorxiv": biorxiv_literature
            }
        }

# Additional reasoning modes can be added here following the same pattern 
