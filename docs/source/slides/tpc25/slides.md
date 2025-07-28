---
marp: true
theme: default
class: lead
paginate: true
backgroundColor: #fff
backgroundImage: url('https://marp.app/assets/hero-background.svg')
header: "BioR5: Biological Reasoning System"
footer: "Lightning Talk - TPC25"
---

<!-- _class: lead -->

# BioR5: Biological Reasoning System

## A Three-Layer Tool-Calling Architecture

**Peng Ding**
Argonne National Laboratory
University of Chicago

---

## The Problem

![bg right:50% 90%](figures/reasoning_examples.png)

**The challenge**: Biologists use **different reasoning modes**

- **"Why does this trait exist?"** → Teleonomic
- **"How does this work?"** → Mechanistic

**Current AI**: One model, one approach
**Biology**: Eleven distinct reasoning modes

---

## Our Solution

**BioR5**: Different questions → Different approaches
**Current AI**: "More data + bigger model"

**Example**: "How does insulin regulate glucose?"

- Needs biochemical pathways + causal networks
- NOT just correlation in expression data

![bg right:50% 90%](figures/current_model_vs_BioR5.png)

---

## Three-Layer Architecture

**BioR5**: Map reasoning modes to computational layers

**Layer A**: LLM + specialized prompts
**Layer B**: Specialized models (proteins, images)  
**Layer C**: External resources (databases, tools)

![w:90%](figures/architecture.png)

---

## Reasoning Mode Details - A Receipe

**Key Insight**: Each reasoning mode needs different resources:

1. **Model weights**: Principles ✓, Details ✗
2. **Specialized models**: Images, structures, etc.
3. **External**: Databases, simulations, etc.

![w:90%](figures/reasoning_mode_to_layer_arch.png)

---

## Layer Details - ToolRegistries

**Layer A**: `parametric_memory`= LLM + specialized prompts

- Same LLM, different prompts → Different knowledge distillation
- Status: 11 reasoning modes implemented

**Layer B**: Specialized models as tools

- Structure prediction, image analysis
- Packaged as callable tools

**Layer C**: External resources

- Databases, computational tools, knowledge graphs

---

## Working in Progress

![bg right:65% 90%](figures/triage_planner.png)

**Next**: Divide-and-conquer scheduling

**Example**: 'bird bone evolution' →

- Evolutionary pressure
- Bone mechanics
- Flight integration

Results merge into final answer

---

## Why This Matters

![bg right:50% 90%](figures/team_role_and_dev_role.png)

**Scalability**:

- ToolRegistry: Any OpenAPI/MCP/Python function becomes a tool
- ReasoningModeRegistry: Recipes for reasoning

**Team boundaries**:

- AI developers: Framework
- Domain experts: Reasoning modes
- Tool developers: Components

---

<!-- _class: lead -->

# Thank You

## **Questions?**
