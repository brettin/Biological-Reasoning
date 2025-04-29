from typing import Dict, Any, List
from abc import ABC, abstractmethod
from bio_reasoning.layers.layer_a import BiologicalKnowledgeStore
from bio_reasoning.layers.layer_b import GenomicSequenceAnalyzer, ImagingAnalyzer
from bio_reasoning.layers.layer_c import (
    OpenTargetsRepository,
    PubMedRepository,
    BioRxivRepository,
)
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
    def reason(self, query: str) -> Dict[str, Any]:
        """Perform reasoning on a biological query."""
        pass


class PhylogeneticReasoning(ReasoningMode):
    """Reasoning based on evolutionary relationships."""

    def reason(self, query: str) -> Dict[str, Any]:
        """Perform phylogenetic reasoning."""
        # Get basic knowledge from Layer A
        knowledge = self.layer_a.retrieve_knowledge(query)

        # Analyze sequences using Layer B
        sequence_analysis = self.layer_b_genomic.analyze(query)

        # Get evolutionary data from Layer C
        pubmed_literature = self.layer_c_pubmed.query(
            {"query": f"{query} phylogenetic analysis"}
        )
        biorxiv_literature = self.layer_c_biorxiv.query(
            {"query": f"{query} phylogenetic analysis"}
        )

        return {
            "reasoning_mode": "phylogenetic",
            "knowledge": knowledge,
            "sequence_analysis": sequence_analysis,
            "literature": {"pubmed": pubmed_literature, "biorxiv": biorxiv_literature},
        }


class TeleonomicReasoning(ReasoningMode):
    """Reasoning based on function and purpose."""

    """Teleonomic: Explains traits in terms of their purpose or function—that is, 
    how a trait may confer a fitness advantage. It connects observed biological 
    features with their adaptive benefits, often drawing on well‐documented case 
    studies (e.g., beak shapes in finches)."""
    
    def reason(self, query: str) -> Dict[str, Any]:
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
            "literature": {"pubmed": pubmed_literature, "biorxiv": biorxiv_literature},
        }


class MechanisticReasoning(ReasoningMode):
    """Reasoning based on causal mechanisms."""

    def reason(self, query: str) -> Dict[str, Any]:
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
            "literature": {"pubmed": pubmed_literature, "biorxiv": biorxiv_literature},
        }


# Additional reasoning modes can be added here following the same pattern
