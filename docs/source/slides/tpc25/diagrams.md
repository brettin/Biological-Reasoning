# BioR5 Presentation Visual Resources

## Image File Mapping

| Slide                                 | Image File                         | Content Description                                                         | Usage                   |
| ------------------------------------- | ---------------------------------- | --------------------------------------------------------------------------- | ----------------------- |
| **Slide 1: The Problem**              | `reasoning_examples.png`           | Reasoning modes overview - different problem types and reasoning approaches | Core slide (required)   |
| **Slide 2: Our Solution**             | `current_model_vs_BioR5.png`       | Current AI vs BioR5 comparison diagram                                      | Core slide (required)   |
| **Slide 3: Design Challenge**         | `reasoning_mode_to_layer_arch.png` | Reasoning mode to architecture layer mapping                                | Optional slide          |
| **Slide 3: Three-Layer Architecture** | `architecture.png`                 | BioR5 three-layer architecture core diagram                                 | Core slide (required)   |
| **Slide 4: Future Work**              | `triage_planner.png`               | Reasoning trace and divide-and-conquer scheduling                           | Core slide (required)   |
| **Slide 6B: Development Boundaries**  | `team_role_and_dev_role.png`       | Team roles and development boundaries                                       | Optional detailed slide |

## Mermaid Diagram Sources

### 1. Reasoning Modes Overview (Slide 1)

```mermaid
graph LR
    Q1["Why does this trait exist?"] --> T1[🧬 Teleonomic]
    Q2["How does this process work?"] --> T2[⚙️ Mechanistic]
    Q3["What evolved from what?"] --> T3[🌳 Phylogenetic]
    Q4["What happens over time?"] --> T4[⏰ Temporal]

    style T1 fill:#e1f5fe
    style T2 fill:#f3e5f5
    style T3 fill:#e8f5e8
    style T4 fill:#fff3e0
```

### 2. Current AI vs BioR5 Comparison (Slide 2)

```mermaid
graph LR
subgraph "Current AI"
direction LR
CA[More Data + Bigger Model]
CA --> CAR[One Approach for All]
end

subgraph "BioR5"
direction LR
BR[Reasoning-Mode-Aware]
BR --> BR1[Teleonomic: Evolutionary theory]
BR --> BR2[Mechanistic: Pathway analysis]
BR --> BR3[Different tools for different questions]
end

style CA fill:#ffcdd2
style BR fill:#c8e6c9
```

### 3. Reasoning Mode to Architecture Mapping (Slide 3 Optional)

```mermaid
graph TD
    RM[Reasoning Mode] --> D1[Parametric Memory]
    RM --> D2[Specialized Models]
    RM --> D3[External Resources]

    D1 --> D1A[✓ General principles]
    D1 --> D1B[✗ Dynamic details]

    D2 --> D2A[Image analysis]
    D2 --> D2B[Structure prediction]

    D3 --> D3A[Growing databases]
    D3 --> D3B[Simulations]

    style D1 fill:#e3f2fd
    style D2 fill:#f1f8e9
    style D3 fill:#fce4ec
```

### 4. Three-Layer Architecture Core Diagram (Slide 3 Core)

```mermaid
graph TB
    subgraph "BioR5 Architecture"
        RM[🧠 Reasoning Mode] --> C[🎯 Coordinator]

        C --> A[Layer A: The Generalist]
        C --> B[Layer B: The Specialists]
        C --> CC[Layer C: The Library]

        subgraph "Layer A"
            A1[LLM + Specialized Prompts]
            A2[Parametric Memory Tools]
        end

        subgraph "Layer B"
            B1[Protein Structure Models]
            B2[Image Analysis Models]
            B3[Sequence Models]
        end

        subgraph "Layer C"
            C1[📊 PubMed, NCBI]
            C2[⚙️ BLAST, Phylogenetic Tools]
            C3[🕸️ Gene Ontology, Reactome]
        end
    end

    style A fill:#e3f2fd
    style B fill:#f1f8e9
    style CC fill:#fce4ec
    style RM fill:#fff3e0
```

### 5. Reasoning Trace Diagram (Slide 4 Future Work)

```mermaid
graph LR
    Q[Why do birds have hollow bones?] --> C[Coordinator]

    C --> O1[Objective 1: Evolutionary pressure]
    C --> O2[Objective 2: Bone mechanics]
    C --> O3[Objective 3: Flight integration]
    C --> O4[Objective N: xxxxxxxx]

    O1 --> R1(Evolutionary Reasoning)
    O2 --> R2(Mechanistic Reasoning)
    O3 --> R3(Systems Reasoning)
    O4 --> R4(xxx Reasoning)

    R1 --x T1[Tools: Phylogenetic DB, Evolution Models]
    R2 --x T2[Tools: Structure Analysis, Physics Models]
    R3 --x T3[Tools: Flight Simulation, Integration Analysis]
    R4 --x T4[Tools: xxx, yyy, zzz]

    T1 --> A1[Result 1: Selection pressure for weight reduction]
    T2 --> A2[Result 2: Hollow structure maintains strength]
    T3 --> A3[Result 3: Enables efficient flight mechanics]
    T4 --> A4[Result 4: xxxxxxxxxxxx]

    A1 --> F[Final Answer: Integrated explanation]
    A2 --> F
    A3 --> F
    A4 --> F

    style Q fill:#fff3e0
    style C fill:#e1f5fe
    style F fill:#c8e6c9
```

### 6. Team Roles and Development Boundaries (Optional)

```mermaid
graph LR
    subgraph "ToolRegistry"
        TR[Tool Registry]
        TR --> API[OpenAPI Tools]
        TR --> MCP[MCP Tools]
        TR --> PY[Python Tools]
    end

    subgraph "ReasoningModeRegistry"
        RMR[Reasoning Mode Registry]
        RMR --> RM1[Teleonomic Mode]
        RMR --> RM2[Mechanistic Mode]
        RMR --> RM3[Phylogenetic Mode]
        RMR --> RMN[... 11 modes total]
    end

    TR --> RMR

    subgraph "Team Boundaries"
        AI[AI Developers: Framework]
        DE[Domain Experts: Reasoning Modes]
        TD[Tool Developers: Components]
    end

    AI --> TR
    DE --> RMR
    TD --> TR

    style TR fill:#e3f2fd
    style RMR fill:#f1f8e9
```

## 8-Minute Core Presentation Strategy

### Required Images (Core Content)

1. `reasoning_examples.png` - Problem definition
2. `current_model_vs_BioR5.png` - Solution comparison
3. `architecture.png` - Three-layer architecture
4. `triage_planner.png` - Future work

### Optional Images (Time Permitting)

5. `reasoning_mode_to_layer_arch.png` - Design challenge
6. `team_role_and_dev_role.png` - Team collaboration

## Usage Instructions

### For Static Images

- All image files are located in the `figures/` folder
- Preload all images in your presentation tool
- The core 4 images are sufficient for an 8-minute presentation
- Optional images can be used flexibly based on available time

### For Mermaid Diagrams

1. **Copy the corresponding Mermaid code** into your presentation tool
2. **Online preview**: Use [Mermaid Live Editor](https://mermaid.live/) to preview
3. **Export images**: Most Mermaid tools support PNG/SVG export
4. **Marp integration**: Direct embedding in markdown presentations

## Recommended Visual Flow

**Core Presentation (8 minutes)**:

- Diagram 1: Reasoning Modes Overview → Problem identification
- Diagram 2: Current AI vs BioR5 → Solution positioning
- Diagram 4: Three-Layer Architecture → Technical approach
- Diagram 5: Reasoning Trace → Future capabilities

**Extended Presentation (12+ minutes)**:

- Add Diagram 3: Architecture mapping details
- Add Diagram 6: Team collaboration model
