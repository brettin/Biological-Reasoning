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

- Phylogenetic Reasoning
- Teleonomic Reasoning
- Mechanistic Reasoning
- (Additional modes can be added following the same pattern)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/biological-reasoning.git
   cd biological-reasoning
   ```

2. Install dependencies:

   ```bash
   pip install .
   ```

3. Set up environment variables:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Usage

### Command Line Interface

Run the CLI in interactive mode:

```bash
python -m bio_reasoning.cli
```

Or process a specific query:

```bash
python -m bio_reasoning.cli --query "What is the function of TP53?"
```

### Python API

```python
from bio_reasoning.coordinator import BiologicalReasoningCoordinator

# Initialize the coordinator
coordinator = BiologicalReasoningCoordinator()

# Process a query
result = coordinator.process_query("What is the function of TP53?")
print(result)
```

## Project Structure

```
bio_reasoning/
├── layers/
│   ├── layer_a.py      # Parametric Memory implementation
│   ├── layer_b.py      # Bespoke Foundation Models
│   └── layer_c.py      # External Knowledge Repositories
├── reasoning/
│   └── reasoning_modes.py  # Biological reasoning modes
├── coordinator.py      # Main system coordinator
└── cli.py             # Command-line interface
```

## Development

To add new reasoning modes:

1. Create a new class in `reasoning_modes.py` that inherits from `ReasoningMode`
2. Implement the `reason` method
3. Add the new mode to the `reasoning_modes` dictionary in `coordinator.py`

## Testing

Run the test suite:

```bash
pytest tests/
```

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
