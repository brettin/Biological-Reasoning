# Lightning Talk Manuscript: Biological Reasoning System (BioR5)

**[Duration: 8 minutes - Core slides only]**

**📊 images**: All image files are located in the [`figures/`](figures/) folder.

---

## **Slide 1: The Problem** ⏱️ **[1 min]**

**[Show: reasoning_examples.png]**

"Biology isn't just about having lots of data.

**The real challenge**: Biologists use **different modes of reasoning** for different questions:

- **"Why does this trait exist?"** → 🧬 Teleonomic reasoning
- **"How does this process work?"** → ⚙️ Mechanistic reasoning

**[OPTIONAL - Skip if running short]:**

- **"What evolved from what?"** → 🌳 Phylogenetic reasoning
- **"What happens over time?"** → ⏰ Temporal reasoning

Current AI: One model, one approach.
Biology: Eleven distinct reasoning modes, each with unique requirements."

---

## **Slide 2: Our Solution** ⏱️ **[2 min]**

**[Show: current_model_vs_BioR5.png]**

**Current AI**: "More data + bigger model = better science"

**BioR5**: Different questions need different computational approaches.

**Example**: "Why are finch beaks different shapes?"

- Needs evolutionary theory + ecological data
- NOT just pattern matching

**The Gap**: We need **reasoning-mode-aware** AI.

**[OPTIONAL - Skip if running short]:**
**Example**: "How does insulin regulate glucose?"

- Needs biochemical pathways + causal networks
- NOT just correlation in expression data

---

## **[OPTIONAL SLIDE - Skip if time is short]**

## **Slide 3: The Design Challenge**

**[Show: reasoning_mode_to_layer_arch.png]**

**Key Insight**: Each reasoning mode needs different computational resources:

1. **Model weights**: General principles ✓, Dynamic details ✗
2. **Specialized models**: Image analysis, structure prediction
3. **External resources**: Growing databases, simulations

**This is a fundamental mismatch between biological reasoning and current AI.**

---

## **Slide 3: Three-Layer Architecture** ⏱️ **[3 min - CORE CONTENT]**

**[Show: architecture.png]**

**BioR5**: Map each reasoning mode to the right computational layer

**Layer A - "The Generalist"**: LLM with specialized prompts

- General biological principles and knowledge
- Different prompts → Different knowledge distillation

**Layer B - "The Specialists"**: Specialized models

- Protein structure prediction, image analysis
- Handle non-text data

**Layer C - "The Library"**: External resources

- Live databases (PubMed, NCBI), computational tools
- Always current data, or restricted access

**Key**: The **reasoning mode** determines which layers activate and which tools to provide.

---

## **[DETAILED SLIDES - Use only if time allows]**

## **Slide 4A: Layer A Details** ⏱️ **[OPTIONAL - 1 min]**

**Implementation**: `parametric_memory` with specialized prompts

**Examples**:

- **Mechanistic**: _"Explain step-by-step pathway..."_
- **Evolutionary**: _"What adaptive advantage..."_

**Key insight**: Same LLM, different prompts → Different knowledge distillation

**Status**: Implemented across 11 reasoning modes

---

## **Slide 4B: Layer B Details** ⏱️ **[OPTIONAL - 1 min]**

**Role**: Handle modality beyond pure text

**Examples**:

- AlphaFold-style structure prediction for spatial reasoning
- Cell image classifier for developmental pattern analysis
- Sequence alignment models for phylogenetic analysis

**Integration**: Specialized models packaged as callable tools

---

## **Slide 4C: Layer C Details** ⏱️ **[OPTIONAL - 1 min]**

**Major categories**:

- **📊 Databases**: NCBI, PubMed, clinical data, websearch
- **⚙️ Computational Tools**: BLAST, phylogenetic builders
- **🕸️ Knowledge Graphs**: Gene Ontology, Reactome

**Why external**: Data grows daily, privacy regulations, computational intensity

---

## **Slide 4: Future Work** ⏱️ **[1 min]**

**[Show: triage_planner.png]**

**Next milestone**: Divide-and-conquer scheduling

**Example**: 'bird bone evolution' becomes:

- Evolutionary pressure → evolutionary_reasoning
- Bone mechanics → mechanistic_reasoning
- Flight integration → systems_reasoning

Results merge into final answer. Reasoning is traceable and further divisible.

---

## **Slide 5: Why This Matters** ⏱️ **[1 min]**

**Scalability**:

- Layers are packaged tools, via ToolRegistry
- Reasoning modes are recipes, via ReasoningModeRegistry
- Both can expand rapidly

**Team boundaries**:

- AI developers: Build framework
- Domain experts: Define reasoning modes
- Tool developers: Build components

**Beyond biology**: Could support other science domains.

---

## **Conclusion** ⏱️ **[30 seconds]**

**Thank you. Questions?**

---

## **[OPTIONAL DETAILED SLIDES - Skip if running short]**

## **Slide 6A: Technical Scalability** ⏱️ **[OPTIONAL]**

**ToolRegistry**: Handles tools from various resources uniformly

- Goes beyond MCP
- Includes Python tools and OpenAPI tools
- Rapid expansion of all layers

**ReasoningModeRegistry**: Manages reasoning modes

- Defines tool usage patterns
- Like recipes for each reasoning type

---

## **Slide 6B: Development Boundaries** ⏱️ **[OPTIONAL]**

**[Show: team_role_and_dev_role.png]**

**Clear separation**:

- **AI developers**: Coordinator, tool interfaces, planning logic
- **Domain experts**: Reasoning modes, prompts, tool selection
- **Tool developers**: Components using OpenAPI, MCP, Python

Each team works independently. Registry connects everything.

---

## **TIMING GUIDE FOR 8-MINUTE TALK:**

**CORE SLIDES (6 minutes):**

1. The Problem (1 min)
2. Our Solution (2 min)
3. Three-Layer Architecture (3 min)

**WRAP-UP (2 minutes):** 4. Future Work (1 min) 5. Why This Matters (1 min)

**OPTIONAL SLIDES (use only if ahead of schedule):**

- Slide 2 alternative examples
- Slide 3 Design Challenge
- Slides 4A-4C Layer details
- Slides 6A-6B Technical details

---

## **Q&A Preparation**

**Q: "How do you ensure tool reliability?"**
**A:** Each tool has defined interface contracts, input validation, output schemas, error handling.

**Q: "What makes this different from existing agent frameworks?"**
**A:** Built specifically for biological reasoning modes, and clear separation between coordination logic and domain tools.

**Q: "How do you handle tool conflicts?"**
**A:** Coordinator has conflict resolution strategies: weight outputs, ask clarification, escalate to human review.
