# BioR5 Lightning Talk Script

## Slide 1 (Title slide)

[greeting]
[introduction]

## Slide 2 (Scenario)

In biology, scientists often need to answer questions that require different modes of reasoning. For example:

- Why does certain trait exist? This requires teleonomic reasoning.
  We need to understand the purpose of the trait. How does it help survival and reproduction?

- How does a certain process work? This requires mechanistic reasoning.
  We need to understand the underlying mechanisms. How do different components interact?

When building agents for biological study, we must consider these different reasoning modes.

## slide 3 (Problem statement)

But the fact is: we often build with one "model".

Here "model" means a set of rules, parameters, or prompts. It is kind of rigid.

Plus, the traditional "more data, bigger model" approach has limitations in the LLM and agent era. Why?

1. Training big LLMs is expensive.
2. Too much new data and knowledge emerges daily.
3. Researchers are not AI engineers.

So we need flexible and agile agents.

## slide 4 (Architecture, Big picture)

We propose BioR5, a biological reasoning system that can handle different modes of reasoning.

It is a three-layer, tool-calling agent architecture.

It composes of:

- an agentic coordinator
- a set of reasoning modes
- three layers of tools

## slide 5 (Reasoning mode details)

As mentioned before, each reasoning mode has unique characteristics.

Each needs different **thinking patterns** and **different tools**.

Thinking patterns are implemented as prompt sets. These prompts shape LLM behavior.

Tools are defined independently. They are not bound to specific reasoning modes. We sort tools into three layers by resource categories.

## slide 6 (Layer of tools)

[Layer A]

Layer A is the most basic layer. It contains parametric memory tools. At its core, it's a prompted LLM packaged as a tool.

Knowledge is baked into LLMs during training. They're good at general principles. But they don't always excel at specific details.

We can use the same LLM with different prompts. Or different LLMs with different prompts.

[Layer B]

Layer B concerns specialized models. They're also packaged as tools.

Examples include:

- protein models for sequence analysis
- graph models for topology
- specialized LLMs for SMILES notation

By packaging as tools, we hide complexity. We provide simple functional interfaces.

[Layer C]

Layer C concerns external resources. These include databases, simulators, RAG pipelines, and APIs.

These tools are dynamic. They update frequently. Some have license restrictions. Others have location or privacy concerns. We can't expect them in powerful LLMs all the time. It's expensive, impossible, and unnecessary.

## slide 7 (WIP, triage-planner)

Our next milestone is a divide and conquer scheduler.

Take bird bone evolution as an example. We can decompose the question into sub-tasks.

Each sub-task has its own reasoning mode. Each uses tools from the three layers.

Sub-tasks can be self-contained. Or they can be further decomposed.

We assemble the final answer from sub-task results.

## slide 8 (Importance)

This architecture design is important in two folds:

**First**, it scales easily.

We can add, update, or remove tools in each layer. This doesn't affect other layers.

Tool implementations can vary.

Python functions, Python classes, OpenAPI services, or MCP servers. Our ToolRegistry handles them all with a unified interface.

We can add reasoning modes by extending the ReasoningMode class. Just add dedicated prompts and tool selections.

**Second**, teams with different expertise can work together more easily.

Domain experts focus on reasoning mode prompts. They use their familiar tools.

Software experts help adapt tools. They wrap them as Python functions or package them using OpenAPI or MCP.

AI framework experts tune the control logic and scheduler.

Everyone works with their most familiar tools and languages.

## slide 9 (Thank you)
