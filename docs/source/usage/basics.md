# Basic Usage

## Overview

The Biological Reasoning Framework provides a three-layer architecture for biological reasoning tasks. This guide covers the basic usage patterns and common workflows.

## Quick Start

### Basic Coordinator Usage

```python
from bio_reasoning.coordinator import Coordinator
from bio_reasoning.config import ConfigManager

# Get centralized configuration
config = ConfigManager.get_config()
primary_config = config.get_endpoint("primary").to_agent_config()

# Create coordinator
coordinator = Coordinator(config=primary_config)

# Run a biological reasoning task
result = coordinator.run("Analyze the toxicity of benzene (c1ccccc1)")
print(result)
```

### Configuration Setup

The framework uses a centralized configuration system. Set up your environment variables:

```bash
# Required: Primary LLM
BIO_PRIMARY_API_KEY=your_api_key
BIO_PRIMARY_BASE_URL=https://api.openai.com/v1
BIO_PRIMARY_MODEL_NAME=gpt-4o

# Optional: TX-Gemma for specialized toxicity prediction
BIO_TXGEMMA_API_KEY=your_txgemma_key
BIO_TXGEMMA_BASE_URL=http://localhost:8000/v1
BIO_TXGEMMA_MODEL_NAME=google/txgemma-27b-chat

# Optional: Registry LLM for reasoning mode selection
BIO_REGISTRY_API_KEY=your_registry_key
BIO_REGISTRY_BASE_URL=https://api.openai.com/v1
BIO_REGISTRY_MODEL_NAME=gpt-4-turbo
```

## Core Components

### 1. Coordinator

The main orchestrator that manages the three-layer architecture:

```python
from bio_reasoning.coordinator import Coordinator

coordinator = Coordinator(config=agent_config)

# Run biological reasoning
result = coordinator.run("What are the potential toxicity concerns for aspirin?")
```

### 2. Reasoning Modes

The framework supports 11 reasoning modes for different types of biological analysis:

```python
from bio_reasoning.reasoning.registry import get_reasoning_modes

# Get available reasoning modes
modes = get_reasoning_modes()
print(f"Available modes: {list(modes.keys())}")

# Use specific reasoning mode
from bio_reasoning.reasoning.toxicology_instantiation import create_toxicology_mode

toxicology_mode = create_toxicology_mode()
result = toxicology_mode.reason("Analyze toxicity of benzene")
```

### 3. Layer B Tools

Layer B provides specialized tools for biological analysis:

```python
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

# Toxicity prediction
result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
print(f"Mutagenicity prediction: {result}")

# Comprehensive analysis
all_results = predict_toxicity(endpoint="all", smiles="c1ccccc1")
for endpoint, prediction in all_results.items():
    print(f"{endpoint}: {prediction}")
```

## Common Workflows

### Toxicity Analysis

```python
from bio_reasoning.coordinator import Coordinator
from bio_reasoning.config import ConfigManager

def analyze_toxicity(smiles):
    """Comprehensive toxicity analysis of a compound."""
    
    # Setup
    config = ConfigManager.get_config()
    coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())
    
    # Run analysis
    query = f"Perform a comprehensive toxicity analysis of the compound with SMILES: {smiles}"
    result = coordinator.run(query)
    
    return result

# Usage
result = analyze_toxicity("c1ccccc1")  # benzene
print(result)
```

### Drug-Target Interaction Analysis

```python
def analyze_drug_target(smiles, target_protein):
    """Analyze drug-target interactions."""
    
    from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity
    
    # Predict binding affinity
    binding_result = predict_toxicity(
        endpoint="bindingdb kd",
        smiles=smiles,
        target_protein=target_protein
    )
    
    # Use coordinator for comprehensive analysis
    config = ConfigManager.get_config()
    coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())
    
    query = f"Analyze the drug-target interaction between compound {smiles} and protein {target_protein}"
    comprehensive_result = coordinator.run(query)
    
    return {
        "binding_prediction": binding_result,
        "comprehensive_analysis": comprehensive_result
    }

# Usage
result = analyze_drug_target(
    smiles="c1ccccc1",
    target_protein="MAKVISFVLLLVCFLQ"
)
```

### Antibody Analysis

```python
def analyze_antibody(antibody_heavy, antibody_light):
    """Analyze antibody properties and interactions."""
    
    from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity
    
    # Predict antibody-antigen binding
    binding_results = predict_toxicity(
        endpoint="all",
        antibody_heavy=antibody_heavy,
        antibody_light=antibody_light
    )
    
    return binding_results

# Usage
result = analyze_antibody(
    antibody_heavy="QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYWMQWVKQRPGQGLEWIGYINPYNDGTKYNEKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARYYDDHYCLDYWGQGTTLTVSS",
    antibody_light="DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYASQSISGIPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTPFTFGQGTKVEIK"
)
```

## Error Handling

### Configuration Errors

```python
try:
    config = ConfigManager.get_config()
    coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())
except Exception as e:
    print(f"Configuration error: {e}")
    print("Please check your .env file or environment variables")
```

### Prediction Errors

```python
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

try:
    result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
    print(f"Prediction: {result}")
except ValueError as e:
    print(f"Invalid endpoint: {e}")
except Exception as e:
    print(f"Prediction failed: {e}")
```

## Best Practices

### 1. Use Centralized Configuration

Always use the centralized configuration system:

```python
from bio_reasoning.config import ConfigManager

config = ConfigManager.get_config()
# This ensures consistent configuration across all components
```

### 2. Handle Missing Endpoints Gracefully

```python
config = ConfigManager.get_config()

if config.has_endpoint("txgemma"):
    print("TX-Gemma available for specialized toxicity predictions")
else:
    print("TX-Gemma not configured - using primary LLM fallback")
```

### 3. Use Appropriate Reasoning Modes

```python
# For toxicity analysis
from bio_reasoning.reasoning.toxicology_instantiation import create_toxicology_mode

# For mechanistic analysis
from bio_reasoning.reasoning.mechanistic_reasoning import MechanisticReasoning

# For systems analysis
from bio_reasoning.reasoning.systems_reasoning import SystemsReasoning
```

### 4. Batch Processing

For multiple compounds, use batch processing:

```python
compounds = ["c1ccccc1", "CC(=O)OC1=CC=CC=C1C(=O)O", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"]

for smiles in compounds:
    result = predict_toxicity(endpoint="all", smiles=smiles)
    print(f"Compound {smiles}: {len(result)} predictions")
```

## Integration Examples

### With External Data Sources

```python
import pandas as pd
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

def analyze_compound_library(compounds_df):
    """Analyze a library of compounds."""
    
    results = []
    
    for _, row in compounds_df.iterrows():
        smiles = row['smiles']
        compound_id = row['compound_id']
        
        try:
            # Get toxicity predictions
            toxicity_results = predict_toxicity(endpoint="all", smiles=smiles)
            
            # Store results
            results.append({
                'compound_id': compound_id,
                'smiles': smiles,
                'toxicity_predictions': toxicity_results
            })
            
        except Exception as e:
            print(f"Error analyzing compound {compound_id}: {e}")
    
    return pd.DataFrame(results)

# Usage
compounds_df = pd.DataFrame({
    'compound_id': ['C001', 'C002', 'C003'],
    'smiles': ['c1ccccc1', 'CC(=O)OC1=CC=CC=C1C(=O)O', 'CN1C=NC2=C1C(=O)N(C(=O)N2C)C']
})

results_df = analyze_compound_library(compounds_df)
print(results_df)
```

### With Scientific Workflows

```python
def scientific_workflow(compound_data):
    """Complete scientific workflow for compound analysis."""
    
    # 1. Initial toxicity screening
    toxicity_results = predict_toxicity(endpoint="all", smiles=compound_data['smiles'])
    
    # 2. Detailed mechanistic analysis
    config = ConfigManager.get_config()
    coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())
    
    mechanistic_query = f"Analyze the mechanistic basis for the toxicity of {compound_data['smiles']}"
    mechanistic_analysis = coordinator.run(mechanistic_query)
    
    # 3. Target interaction analysis (if target provided)
    target_analysis = None
    if 'target_protein' in compound_data:
        target_analysis = predict_toxicity(
            endpoint="bindingdb kd",
            smiles=compound_data['smiles'],
            target_protein=compound_data['target_protein']
        )
    
    return {
        'toxicity_screening': toxicity_results,
        'mechanistic_analysis': mechanistic_analysis,
        'target_interaction': target_analysis
    }

# Usage
compound_data = {
    'smiles': 'c1ccccc1',
    'target_protein': 'MAKVISFVLLLVCFLQ'
}

workflow_results = scientific_workflow(compound_data)
```

This basic usage guide provides the foundation for using the Biological Reasoning Framework effectively. For more advanced usage, see the [TX-Gemma Guide](txgemma_guide.md) and [API Reference](../api/index.md).
