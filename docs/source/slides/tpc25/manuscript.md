# Lightning Talk Manuscript: Biological Reasoning System (BioR5)

**[Duration: 8-10 minutes]**

---

## **Slide 1: The Hidden Complexity of Biological Reasoning**

**[Show: Different reasoning mode icons]**

"Biology isn't just about having lots of data types.

**The real challenge**: Biologists use **fundamentally different modes of reasoning** for different questions:

- **"Why does this trait exist?"** → Teleonomic reasoning
- **"How does this process work?"** → Mechanistic reasoning
- **"What evolved from what?"** → Phylogenetic reasoning
- **"What happens over time?"** → Temporal reasoning

**Each mode requires different data, different frameworks, different thinking patterns.**

Current AI: One model, one reasoning approach.
Biology: Eleven distinct reasoning modes, each with unique requirements."

---

## **Slide 2: Why Current AI Falls Short**

**[Show: Current AI vs. Biological Reasoning Requirements]**

**Current AI Assumption**: "More data + bigger model = better science"

**Biological Reality**: Different questions need different approaches:

**Question**: "Why are finch beaks different shapes?"

- **Teleonomic reasoning**: Each shape provides feeding advantage
- **Requires**: Evolutionary theory + ecological data
- **NOT**: Just sequence similarity or pattern matching

**Question**: "How does insulin regulate glucose?"

- **Mechanistic reasoning**: Step-by-step pathway analysis
- **Requires**: Biochemical pathways + causal networks
- **NOT**: Just correlation in expression data

**The Gap**: We need **reasoning-mode-aware** AI, not just multimodal AI.

---

## **Slide 3: The Core Design Challenge**

**[Show: Reasoning Mode → Data → Architecture mapping]**

**Key Insight from BioR5**: Each reasoning mode has specific requirements for:

1. **What knowledge should be in model weights?**

   - Phylogenetic: General evolutionary principles ✓
   - Mechanistic: All pathway details ✗ (too dynamic)

2. **What needs specialized models?**

   - Spatial: Image analysis, structure prediction
   - Temporal: Time-series analysis, oscillation detection

3. **What must stay external?**
   - Comparative: Growing databases, regulated patient data
   - Systems: Heavy simulations, network analysis

**This isn't just engineering - it's a fundamental mismatch between biological reasoning and current AI architecture.**

---

## **Slide 4: A Reasoning-Driven Architecture**

**[Show: Three-layer diagram with reasoning modes mapped]**

**BioR5's Innovation**: Map each reasoning mode to appropriate computational layer

**Layer A (LLM)**: "The Generalist Biologist"

- Holds principles that work across biology
- _"Negative feedback loops maintain homeostasis"_

**Layer B (Specialist Models)**: "The Lab Instruments"

- Handles modality-specific analysis
- _Image analysis for spatial patterns, sequence models for phylogeny_

**Layer C (External Resources)**: "The Library & Compute Center"

- Dynamic data and heavy computation
- _Daily-updated genomes, simulation engines_

**Key**: The **reasoning mode** determines which layers get activated.

---

## **Slide 5: Layer A - Knowledge in Weights**

**Implementation**: `parametric_memory` tool with specialized prompts

**How it works**: Different prompts extract different reasoning knowledge from LLM weights

**Specialized prompt examples**:

- **Mechanistic prompt**: _"Explain the step-by-step biochemical pathway..."_
- **Teleonomic prompt**: _"What adaptive advantage does this trait provide..."_
- **Homeostatic prompt**: _"Identify the feedback loops that maintain..."_
- **Phylogenetic prompt**: _"Based on evolutionary relationships..."_

**What's encoded in weights**:

- Fundamental biological principles across all reasoning modes
- Cross-modal knowledge patterns
- Scientific language and conceptual frameworks

**Key insight**: Same LLM, different prompting strategies → Different reasoning outputs

**Current status**: Implemented and tested across 11 reasoning modes

---

## **Layer B: Bespoke Foundation Models (The Specialists)**

**Role**: Handle non-textual data that Layer A cannot process

**Key capabilities**:

- **Protein sequence models**: Interpret amino acid sequences, predict structure
- **Imaging models**: Analyze microscopy, histology, cellular patterns
- **Graph networks**: Gene regulatory networks, pathway analysis

**Examples**:

- AlphaFold-style structure prediction for spatial reasoning
- Cell image classifier for developmental pattern analysis
- Sequence alignment models for phylogenetic analysis

**Integration**: LLM calls these models, gets results back

- _"Send DNA sequence to sequence model → get motif analysis"_
- _"Send histology image to vision model → get tissue classification"_

**Why needed**: Each biological data type needs specialized processing

---

## **Layer C: External Knowledge & Tools (The Dynamic Layer)**

**Role**: Handle resources too large, dynamic, or regulated for model weights

**Three categories**:

**📊 Massive Databases**: NCBI, KEGG, PubMed, clinical databases
**⚙️ Computational Tools**: Phylogenetic tree builders, ODE solvers, BLAST
**🕸️ Knowledge Graphs**: Gene Ontology, Reactome pathways, BioKG

**Real-time examples**:

- Query: _"Latest genomic variants"_ → NCBI API call
- Query: _"Protein interaction network"_ → Reactome database
- Query: _"Statistical analysis"_ → External R/Python tools

**Why external**:

- Data grows daily (literature, genomes)
- Privacy regulations (patient data)
- Computational intensity (simulations)

**Result**: Always current, verifiable, scalable knowledge

---

## **Slide 7: Divide-and-Conquer Scheduling (Work in Progress)**

**[Show reasoning trace diagram]**

"We're developing divide-and-conquer scheduling for the coordinator.

Complex questions get broken into sub-objectives. Each objective is assigned with a reasoning mode

Example: 'bone evolution in birds' becomes:

- Objective 1: Evolutionary pressure analysis → evolutionary_reasoning task
- Objective 2: Bone structure mechanics → mechanistic_reasoning task
- Objective 3: Flight system integration → systems_reasoning task

Each task could trace to sub-tasks or reach a conclusion.
Results merge into final answer. Tool calls are logged. Reasoning is traceable.

This is our next major development milestone."

---

## **Slide 8: Scalability Through ToolRegistry and ReasoningModeRegistry**

"The system scales through `ToolRegistry` and `ReasoningModeRegistry`.

1. **ToolRegistry:**
   ToolRegistry handles tools from various resources in a unified manner. It registers, presents, and runs tools. It goes beyond MCP. Includes Python tools directly and existing OpenAPI tools.

   This means Layer A, B, and C can all expand rapidly. Any API becomes a tool. Any Python function becomes a tool. Any specialized model becomes a tool.

   People can add new tools to Layer A, B, or C respectively.
   People can also define new reasoning modes separately.

2. **ReasoningModeRegistry:**
   ReasoningModeRegistry manages these modes. It defines how tools are used together, which tools are used for which reasoning mode. And what prompting is used. It's like a recipe

This paradigm may go beyond biology. It could support reasoning modes in other science domains."

---

## **Slide 9: Development Team Boundaries**

"This creates clear development boundaries.

AI developers build the coordinator, tool interfaces and generic planning logic. That's the framework layer.

Domain experts defines reasoning mode. They know the science. They write the prompts and designate which tools to use in each layer.

Tool developers build tool components. They can use OpenAPI, MCP, or Python. Whatever works best or most convenient.

---
