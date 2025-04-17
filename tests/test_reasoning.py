import pytest
from src.coordinator import BiologicalReasoningCoordinator
from src.reasoning.reasoning_modes import (
    PhylogeneticReasoning,
    TeleonomicReasoning,
    MechanisticReasoning
)

@pytest.fixture
def coordinator():
    return BiologicalReasoningCoordinator()

def test_phylogenetic_reasoning():
    reasoner = PhylogeneticReasoning()
    result = reasoner.reason("TP53")
    assert "reasoning_mode" in result
    assert result["reasoning_mode"] == "phylogenetic"
    assert "knowledge" in result
    assert "sequence_analysis" in result
    assert "literature" in result

def test_teleonomic_reasoning():
    reasoner = TeleonomicReasoning()
    result = reasoner.reason("TP53")
    assert "reasoning_mode" in result
    assert result["reasoning_mode"] == "teleonomic"
    assert "knowledge" in result
    assert "target_data" in result
    assert "literature" in result

def test_mechanistic_reasoning():
    reasoner = MechanisticReasoning()
    result = reasoner.reason("TP53")
    assert "reasoning_mode" in result
    assert result["reasoning_mode"] == "mechanistic"
    assert "knowledge" in result
    assert "target_data" in result
    assert "literature" in result

def test_coordinator_process_query(coordinator):
    result = coordinator.process_query("What is the function of TP53?")
    assert "query" in result
    assert "reasoning_mode" in result
    assert "result" in result
    assert result["query"] == "What is the function of TP53?"

def test_coordinator_determine_reasoning_mode(coordinator):
    mode = coordinator.determine_reasoning_mode("What is the function of TP53?")
    assert mode in coordinator.reasoning_modes 