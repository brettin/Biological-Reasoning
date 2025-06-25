# Biological Reasoning Framework

A three-layer artificial intelligence architecture designed to emulate biological reasoning, following the principles outlined in "Biological Reasoning for Advanced AI: A Layered Architecture Approach".

## Architecture Overview

The system consists of three main layers:

1. **Layer A (Parametric Memory)**

   - General-purpose language model interface
   - Stores and retrieves broad biological knowledge
   - Natural language processing capabilities

2. **Layer B (Bespoke Foundation Models)**

   - Specialized modules for biological data analysis
   - Genomic sequence analysis
   - Imaging analysis
   - Integration with language models

3. **Layer C (External Knowledge Repositories)**
   - Integration with external databases and APIs
   - OpenTargets database integration
   - Literature search capabilities

## Reasoning Modes

The system supports multiple biological reasoning modes:

- Phylogenetic Reasoning: Uses evolutionary relationships (via genetic or phenotypic comparisons) to infer common ancestry, divergence, and the historical origins of traits. It relies on sequence alignments, phylogenetic trees, and taxonomic data to transfer knowledge among organisms.
- Teleonomic Reasoning: Explains traits in terms of their purpose or function—that is, how a trait may confer a fitness advantage. It connects observed biological features with their adaptive benefits, often drawing on well‐documented case studies (e.g., beak shapes in finches).
- Mechanistic Reasoning: Focuses on the cause‐and‐effect processes underlying biological functions. It breaks down complex phenomena (e.g., metabolic pathways, signal transduction, muscle contraction) into component interactions and causal chains to explain 'how' a process works.
- Tradeoff Reasoning:
- Systems Reasoning:
- Spatial Reasoning:
- Temporal Reasoning:
- Homeostatic Reasoning:
- Ontogenetic Reasoning:
- Comparative Reasoning:
- (Additional modes can be added following the same pattern)

## Installation

### Prerequisites

- Python 3.10+
- pip

### From PyPI

```bash
pip install bio-reasoning
```

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/brettin/biological-reasoning.git
   cd biological-reasoning
   ```

2. Install dependencies:

   ```bash
   pip install .
   ```

## Configuration

Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

## Usage

### Example Query with Coordinator

```bash
python -m bio_reasoning.coordinator
```

## Project Structure

```bash
$ tree -I "__pycache__|*.egg-info|dist|dev_scripts|config.yaml" src/bio_reasoning
src/bio_reasoning
├── coordinator.py
├── __init__.py
├── layers
│   ├── a
│   │   ├── __init__.py
│   │   └── ...
│   ├── b
│   │   ├── __init__.py
│   │   └── ...
│   ├── c
│   │   ├── __init__.py
│   │   └── ...
│   └── __init__.py
├── reasoning
│   ├── basics.py
│   ├── __init__.py
│   └── ...
└── utils.py
```

## Development

To add new reasoning modes:

1. Create a new file in `reasoning/` that inherits from `ReasoningMode`
2. Register the necessary tools for layer_a, layer_b, and layer_c
3. Compose a proper system prompt for the new reasoning mode
4. `super().__init__(layer_a=layer_a, layer_b=layer_b, layer_c=layer_c, sys_prompt=system_prompt)` to initialize the new reasoning mode

<!-- 
## Testing

Run the test suite:

```bash
pytest tests/
``` -->

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
