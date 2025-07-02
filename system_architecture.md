# Biological Reasoning System Architecture

```mermaid
graph TB
    %% User Interface
    User[User Query] --> Coordinator
    
    %% Main Coordinator
    subgraph "Coordinator"
        Config[Configuration<br/>API Key, Base URL, Model]
        SystemPrompt[System Prompt]
        ReasoningMode[Reasoning Mode]
        Core[MultiModalModel Core]
    end
    
    %% Reasoning Modes
    subgraph "Reasoning Modes"
        BaseMode[ReasoningMode Base Class]
        ExampleMode[ExampleReasoningMode]
        Phylogenetic[Phylogenetic Mode]
        Teleonomic[Teleonomic Mode]
        Mechanistic[Mechanistic Mode]
        Systems[Systems Biology Mode]
        OtherModes[Other Modes...]
    end
    
    %% Layer Architecture
    subgraph "Layer A - Parametric Memory"
        LLM[General LLM<br/>Pre-trained Knowledge]
        ParamMemory[Parametric Memory Factory]
    end
    
    subgraph "Layer B - Specialized Models"
        VisualDesc[Visual Describer<br/>Image Analysis]
        ImageUtils[Image Processing Utils]
        GenomicModel[Genomic Models]
        ProteinModel[Protein Structure Models]
    end
    
    subgraph "Layer C - External Knowledge"
        WebSearch[Web Search APIs]
        PubMed[PubMed Database]
        BioDB[Biological Databases]
        KnowledgeGraph[Knowledge Graphs]
    end
    
    %% Tool Registry
    subgraph "Tool Registry"
        ToolRegA[Layer A Tools]
        ToolRegB[Layer B Tools]
        ToolRegC[Layer C Tools]
        MergedTools[Merged Tool Registry]
    end
    
    %% Data Flow
    Coordinator --> BaseMode
    BaseMode --> ExampleMode
    ExampleMode --> ToolRegA
    ExampleMode --> ToolRegB
    ExampleMode --> ToolRegC
    
    ToolRegA --> ParamMemory
    ToolRegB --> VisualDesc
    ToolRegB --> ImageUtils
    ToolRegC --> WebSearch
    
    ParamMemory --> LLM
    VisualDesc --> LLM
    ImageUtils --> VisualDesc
    
    %% API Communication
    subgraph "External APIs"
        OpenAI[OpenAI API]
        CustomAPI[Custom APIs]
    end
    
    LLM --> OpenAI
    WebSearch --> CustomAPI
    
    %% Response Flow
    MergedTools --> Core
    Core --> Response[Response to User]
    
    %% Styling
    classDef coordinator fill:#e1f5fe
    classDef reasoning fill:#f3e5f5
    classDef layerA fill:#e8f5e8
    classDef layerB fill:#fff3e0
    classDef layerC fill:#fce4ec
    classDef tools fill:#f1f8e9
    classDef api fill:#fafafa
    
    class Config,SystemPrompt,ReasoningMode,Core coordinator
    class BaseMode,ExampleMode,Phylogenetic,Teleonomic,Mechanistic,Systems,OtherModes reasoning
    class LLM,ParamMemory layerA
    class VisualDesc,ImageUtils,GenomicModel,ProteinModel layerB
    class WebSearch,PubMed,BioDB,KnowledgeGraph layerC
    class ToolRegA,ToolRegB,ToolRegC,MergedTools tools
    class OpenAI,CustomAPI api
```

## Architecture Overview

### Core Components

1. **Coordinator**: The main orchestrator that manages the entire system
   - Handles configuration (API keys, base URLs, model names)
   - Manages reasoning modes and system prompts
   - Coordinates between layers and tools

2. **Reasoning Modes**: Define specific approaches to biological reasoning
   - Base class provides common functionality
   - Example mode demonstrates the framework
   - Specialized modes for different biological reasoning types

3. **Three-Layer Architecture**:
   - **Layer A**: Parametric memory using general LLM knowledge
   - **Layer B**: Specialized models for multimodal data (images, sequences, structures)
   - **Layer C**: External knowledge sources (APIs, databases, knowledge graphs)

4. **Tool Registry**: Manages and organizes tools from all layers
   - Individual registries for each layer
   - Merged registry for unified access
   - Tool selection and execution handling

### Data Flow

1. User submits a query to the Coordinator
2. Coordinator determines appropriate reasoning mode
3. Reasoning mode provides system prompt and available tools
4. Tools from all layers are merged into a single registry
5. MultiModalModel core processes the query using available tools
6. Response is returned to the user

### Key Features

- **Modular Design**: Each layer can be developed independently
- **Extensible**: New reasoning modes and tools can be easily added
- **Flexible**: Different combinations of tools can be used for different tasks
- **Scalable**: External APIs and databases provide access to vast knowledge sources 