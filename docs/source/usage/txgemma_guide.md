# TX-Gemma Toxicity Prediction Guide

## Overview

TX-Gemma is a specialized toxicity prediction system integrated into the Biological Reasoning Framework. It provides access to Google's TX-Gemma model for molecular toxicity prediction using standardized prompts from the Therapeutics Data Commons (TDC).

## Key Features

- **Parameter-Driven API**: Automatically determines which prompts to use based on provided parameters
- **703 TDC Endpoints**: Support for all endpoints in the Therapeutics Data Commons
- **12 Parameter Combinations**: From single SMILES to complex antibody-protein interactions
- **No Universal SMILES Requirement**: Supports antibody, peptide-MHC, protein-protein endpoints
- **Automatic Fallback**: Falls back to primary LLM when TX-Gemma unavailable
- **Dynamic Discovery**: All endpoints automatically discovered from TDC prompts

## Quick Start

### Basic Single SMILES Prediction

```python
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

# Predict mutagenicity for a compound
result = predict_toxicity(
    endpoint="ames",
    smiles="c1ccccc1"  # benzene
)
print(result)
# Output: Instructions: Answer the following question about drug properties...
#         Context: Mutagenicity means the ability of a drug to induce genetic alterations...
#         Question: Given a drug SMILES string, predict whether it
#         (A) is not mutagenic (B) is mutagenic
#         Drug SMILES: c1ccccc1
#         Answer: (A)
```

### Predict All Matching Endpoints

```python
# Run predictions for all endpoints that accept a single SMILES
all_results = predict_toxicity(
    endpoint="all",
    smiles="c1ccccc1"
)

# Results is a dictionary: {endpoint_name: prediction_result}
for endpoint, prediction in all_results.items():
    print(f"{endpoint}: {prediction}")
```

## Parameter Combinations

The system supports 12 distinct parameter combinations covering 703 TDC endpoints:

### 1. Single SMILES (671 endpoints)
```python
predict_toxicity(endpoint="ames", smiles="c1ccccc1")
```

### 2. Dual SMILES (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    drug1_smiles="c1ccccc1",
    drug2_smiles="CC(=O)OC1=CC=CC=C1C(=O)O"
)
```

### 3. SMILES + Protein (6 endpoints)
```python
predict_toxicity(
    endpoint="bindingdb kd",
    smiles="c1ccccc1",
    target_protein="MAKVISFVLLLVCFLQ"
)
```

### 4. Antibody (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    antibody_heavy="QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYWMQWVKQRPGQGLEWIGYINPYNDGTKYNEKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARYYDDHYCLDYWGQGTTLTVSS",
    antibody_light="DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYASQSISGIPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTPFTFGQGTKVEIK"
)
```

### 5. Peptide + MHC (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    peptide_sequence="SIINFEKL",
    mhc_pseudosequences="YFAMREKRFSV"
)
```

### 6. Epitope + TCR (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    epitope_sequence="SIINFEKL",
    tcr_sequence="CAVKSSNYGQKLVF"
)
```

### 7. Protein-Protein (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    protein1_sequence="MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTDGLLYGSQTPNEECLFLERLEENHYNTYISKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV"
)
```

### 8. miRNA (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    mirna_sequence="UGAGGUAGUAGGUUGUAUAGUU"
)
```

### 9. Cell Line (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    cell_line="MCF-7 breast cancer cell line"
)
```

### 10. Catalyst + Product (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    catalyst_smiles="[Pd]",
    product_smiles="c1ccccc1"
)
```

### 11. Reactant + Product (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    reactant_smiles="c1ccccc1",
    product_smiles="c1ccccc1"
)
```

### 12. GuideSeq (2 endpoints)
```python
predict_toxicity(
    endpoint="all",
    guideseq="GGCGAGGUGCUGCUGGGCUU"
)
```

## API Reference

### `predict_toxicity(endpoint="all", **kwargs)`

Main entry point for toxicity predictions.

**Parameters:**
- `endpoint` (str): Specific endpoint name or "all" for all matching endpoints
- `**kwargs`: Parameters that determine which prompts to use

**Returns:**
- `str` or `Dict[str, str]`: Single prediction result or dictionary of results

**Examples:**
```python
# Single endpoint
result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")

# All matching endpoints
results = predict_toxicity(endpoint="all", smiles="c1ccccc1")

# Limit number of endpoints
results = predict_toxicity(endpoint="all", smiles="c1ccccc1", max_endpoints=10)
```

### `get_available_endpoints()`

Get all available endpoints organized by parameter patterns.

**Returns:**
- `Dict[str, List[str]]`: Dictionary mapping parameter patterns to endpoint lists

**Example:**
```python
from bio_reasoning.layers.b.txgemma_predictor import get_available_endpoints

endpoints = get_available_endpoints()
for pattern, endpoint_list in endpoints.items():
    print(f"{pattern}: {len(endpoint_list)} endpoints")
```

## Configuration

TX-Gemma uses the centralized configuration system. Set up your environment variables:

```bash
# Required for TX-Gemma
BIO_TXGEMMA_API_KEY=your_api_key
BIO_TXGEMMA_BASE_URL=http://localhost:8000/v1
BIO_TXGEMMA_MODEL_NAME=google/txgemma-27b-chat

# Optional: Customize behavior
BIO_TXGEMMA_TEMPERATURE=0.1
BIO_TXGEMMA_MAX_TOKENS=2048
BIO_TXGEMMA_TIMEOUT=60
```

## Error Handling

The system provides graceful error handling:

```python
try:
    result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
    print(f"Prediction: {result}")
except ValueError as e:
    print(f"Invalid endpoint: {e}")
except Exception as e:
    print(f"Prediction failed: {e}")
```

## Fallback Behavior

When TX-Gemma is not available, the system automatically falls back to the primary LLM:

```python
# If TX-Gemma is down, this will use the primary LLM
result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
```

## Best Practices

1. **Use Specific Endpoints**: For single predictions, specify the exact endpoint
2. **Use "all" for Exploration**: Use `endpoint="all"` to discover available endpoints
3. **Limit Batch Size**: Use `max_endpoints` parameter for large batch predictions
4. **Validate Parameters**: Ensure all required parameters are provided
5. **Handle Errors**: Always wrap predictions in try-catch blocks

## Advanced Usage

### Custom Parameter Mapping

The system automatically maps TDC placeholders to function parameters:

```python
# TDC placeholder: {Drug SMILES} -> parameter: smiles
# TDC placeholder: {Target amino acid sequence} -> parameter: target_protein
# TDC placeholder: {Antibody heavy chain sequence} -> parameter: antibody_heavy
```

### Batch Processing

```python
# Process multiple compounds
compounds = ["c1ccccc1", "CC(=O)OC1=CC=CC=C1C(=O)O", "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"]

for smiles in compounds:
    results = predict_toxicity(endpoint="all", smiles=smiles)
    print(f"Compound {smiles}: {len(results)} predictions")
```

### Endpoint Discovery

```python
from bio_reasoning.layers.b.txgemma_predictor import get_matching_prompts

# Find all endpoints that require SMILES + protein
matching = get_matching_prompts(smiles="test", target_protein="test")
print(f"Found {len(matching)} endpoints requiring SMILES + protein")
```

## Troubleshooting

### Common Issues

1. **"Endpoint not found"**: Check endpoint name spelling and case
2. **"Missing parameters"**: Ensure all required parameters are provided
3. **"TX-Gemma not available"**: Check configuration and server status
4. **"Fallback to primary LLM"**: TX-Gemma server may be down

### Debug Mode

Enable debug logging to see detailed information:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now run predictions to see detailed logs
result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
```

## Integration with Biological Reasoning

TX-Gemma integrates seamlessly with the Biological Reasoning Framework:

```python
from bio_reasoning.coordinator import Coordinator
from bio_reasoning.config import ConfigManager

# Create coordinator with TX-Gemma support
config = ConfigManager.get_config()
coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())

# TX-Gemma predictions are automatically available in Layer B
# when the toxicology reasoning mode is used
```
