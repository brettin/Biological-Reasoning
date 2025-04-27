````mermaid
graph TD
    %% Main Application Modules
    subgraph Main Application
        CLI[cli.py]
        Coordinator[coordinator.py]
        Config[config.py]
    end

    %% Reasoning Module
    subgraph Reasoning
        ReasoningModes[reasoning_modes.py]
        Phylogenetic[PhylogeneticReasoning]
        Teleonomic[TeleonomicReasoning]
        Mechanistic[MechanisticReasoning]
    end

    %% Layer Modules
    subgraph Layer A
        LayerA[layer_a.py]
        BioKnowledge[BiologicalKnowledgeStore]
    end

    subgraph Layer B
        LayerB[layer_b.py]
        GenomicAnalyzer[GenomicSequenceAnalyzer]
        ImagingAnalyzer[ImagingAnalyzer]
    end

    subgraph Layer C
        LayerC[layer_c.py]
        PubMedRepo[PubMedRepository]
        BioRxivRepo[BioRxivRepository]
        TargetRepo[TargetDiseaseRepository]
        SimpleBioRxiv[simple_bioxriv_requests.py]
    end

    %% Resource Management
    subgraph Resource Management
        ResourceManager[resource_manager.py]
    end

    %% Dependencies
    CLI --> Coordinator
    Coordinator --> Config
    Coordinator --> ReasoningModes
    ReasoningModes --> LayerA
    ReasoningModes --> LayerB
    ReasoningModes --> LayerC
    LayerA --> ResourceManager
    LayerB --> ResourceManager
    LayerC --> ResourceManager
    LayerC --> SimpleBioRxiv
```
