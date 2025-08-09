# BioR5 Architecture

## Reasoning Modes

There are 11 reasoning mode categories. See `src/bio_reasoning/reasoning/` for the full list.

## Development Guidelines

When developing for an objective:

1. **Identify suitable reasoning mode(s)** - An objective may fit multiple categories
2. **Plan tools for layers A, B, C** - Check `src/bio_reasoning/layers/` for available tools, proposed tools if not available
3. **Instantiation instead of inheritance** - Use instantiation to create specialized versions of reasoning modes
4. **Avoid unnecessary abstraction** - Keep abstraction layers thin and focused
