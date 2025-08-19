# TDC Parameter Combinations Reference

## Overview

The TX-Gemma predictor supports 12 distinct parameter combinations covering all 703 endpoints in the Therapeutics Data Commons (TDC). This document provides a comprehensive reference for all supported parameter patterns and their corresponding endpoints.

## Parameter Mapping

The system automatically maps TDC placeholders to function parameters:

| TDC Placeholder | Function Parameter | Description |
|-----------------|-------------------|-------------|
| `{Drug SMILES}` | `smiles` | Single drug molecule |
| `{Drug1 SMILES}` | `drug1_smiles` | First drug in combination |
| `{Drug2 SMILES}` | `drug2_smiles` | Second drug in combination |
| `{Target amino acid sequence}` | `target_protein` | Target protein sequence |
| `{Antibody heavy chain sequence}` | `antibody_heavy` | Antibody heavy chain |
| `{Antibody light chain sequence}` | `antibody_light` | Antibody light chain |
| `{Antigen sequence}` | `antigen_sequence` | Antigen sequence |
| `{Peptide amino acid sequence}` | `peptide_sequence` | Peptide sequence |
| `{Possible MHC pseudosequences}` | `mhc_pseudosequences` | MHC pseudosequences |
| `{Epitope amino acid sequence}` | `epitope_sequence` | Epitope sequence |
| `{TCR amino acid sequence}` | `tcr_sequence` | T-cell receptor sequence |
| `{Protein1 amino acid sequence}` | `protein1_sequence` | First protein in interaction |
| `{Protein2 amino acid sequence}` | `protein2_sequence` | Second protein in interaction |
| `{miRNA sequence}` | `mirna_sequence` | miRNA sequence |
| `{Cell line description}` | `cell_line` | Cell line description |
| `{Catalyst SMILES}` | `catalyst_smiles` | Catalyst molecule |
| `{Product SMILES}` | `product_smiles` | Product molecule |
| `{Reactant SMILES}` | `reactant_smiles` | Reactant molecule |
| `{GuideSeq}` | `guideseq` | CRISPR guide sequence |

## Parameter Combinations

### 1. Single SMILES (671 endpoints)

**Pattern**: `{Drug SMILES}`

**Description**: Basic molecular toxicity prediction using a single drug SMILES string.

**Example Endpoints**:
- `ames` - Ames mutagenicity test
- `herg` - hERG channel blocking
- `dili` - Drug-induced liver injury
- `bioavailability ma` - Oral bioavailability
- `bbb martins` - Blood-brain barrier penetration
- `cyp2d6 veith` - CYP2D6 inhibition
- `cyp3a4 veith` - CYP3A4 inhibition
- `cyp2c9 veith` - CYP2C9 inhibition

**Usage Example**:
```python
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

# Predict mutagenicity
result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")

# Predict hERG blocking
result = predict_toxicity(endpoint="herg", smiles="CN1C(=O)CN=C(C2=CCCCC2)c2cc(Cl)ccc21")

# Predict all single SMILES endpoints
all_results = predict_toxicity(endpoint="all", smiles="c1ccccc1")
```

### 2. Dual SMILES (2 endpoints)

**Pattern**: `{Drug1 SMILES}`, `{Drug2 SMILES}`

**Description**: Drug combination analysis for synergy or antagonism.

**Example Endpoints**:
- `drugcomb db` - Drug combination database
- `drugcomb nci60` - NCI-60 drug combination screen

**Usage Example**:
```python
# Analyze drug combination
result = predict_toxicity(
    endpoint="all",
    drug1_smiles="c1ccccc1",  # benzene
    drug2_smiles="CC(=O)OC1=CC=CC=C1C(=O)O"  # aspirin
)
```

### 3. SMILES + Protein (6 endpoints)

**Pattern**: `{Drug SMILES}`, `{Target amino acid sequence}`

**Description**: Drug-target binding affinity prediction.

**Example Endpoints**:
- `bindingdb kd` - BindingDB dissociation constant
- `bindingdb ic50` - BindingDB IC50 values
- `bindingdb ki` - BindingDB inhibition constant
- `bindingdb ec50` - BindingDB EC50 values
- `bindingdb kon` - BindingDB association rate
- `bindingdb koff` - BindingDB dissociation rate

**Usage Example**:
```python
# Predict binding affinity
result = predict_toxicity(
    endpoint="bindingdb kd",
    smiles="c1ccccc1",
    target_protein="MAKVISFVLLLVCFLQ"
)
```

### 4. Antibody (2 endpoints)

**Pattern**: `{Antibody heavy chain sequence}`, `{Antibody light chain sequence}`

**Description**: Antibody-antigen interaction prediction.

**Example Endpoints**:
- `sabdab chen` - SAbDab antibody-antigen binding
- `sabdab dunbar` - SAbDab antibody-antigen affinity

**Usage Example**:
```python
# Predict antibody-antigen binding
result = predict_toxicity(
    endpoint="all",
    antibody_heavy="QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYWMQWVKQRPGQGLEWIGYINPYNDGTKYNEKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARYYDDHYCLDYWGQGTTLTVSS",
    antibody_light="DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYASQSISGIPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTPFTFGQGTKVEIK"
)
```

### 5. Peptide + MHC (2 endpoints)

**Pattern**: `{Peptide amino acid sequence}`, `{Possible MHC pseudosequences}`

**Description**: Peptide-MHC binding prediction for immunology.

**Example Endpoints**:
- `mhc i` - MHC class I binding
- `mhc ii` - MHC class II binding

**Usage Example**:
```python
# Predict peptide-MHC binding
result = predict_toxicity(
    endpoint="all",
    peptide_sequence="SIINFEKL",
    mhc_pseudosequences="YFAMREKRFSV"
)
```

### 6. Epitope + TCR (2 endpoints)

**Pattern**: `{Epitope amino acid sequence}`, `{TCR amino acid sequence}`

**Description**: T-cell receptor-epitope interaction prediction.

**Example Endpoints**:
- `tcr epitope binding` - TCR-epitope binding prediction
- `tcr epitope affinity` - TCR-epitope affinity prediction

**Usage Example**:
```python
# Predict TCR-epitope interaction
result = predict_toxicity(
    endpoint="all",
    epitope_sequence="SIINFEKL",
    tcr_sequence="CAVKSSNYGQKLVF"
)
```

### 7. Protein-Protein (2 endpoints)

**Pattern**: `{Protein1 amino acid sequence}`, `{Protein2 amino acid sequence}`

**Description**: Protein-protein interaction prediction.

**Example Endpoints**:
- `protein protein binding` - Protein-protein binding prediction
- `protein protein affinity` - Protein-protein affinity prediction

**Usage Example**:
```python
# Predict protein-protein interaction
result = predict_toxicity(
    endpoint="all",
    protein1_sequence="MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTDGLLYGSQTPNEECLFLERLEENHYNTYISKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV",
    protein2_sequence="MKLFVVLLLFLGAGLGVGQKQEPLQLVVDLAGELGPLGLPEDAGPGAGAAEPGLQGVALPGPLWLLDLQVLLPLVLDGAGVLVTLAVGALAGALVLVLALLLRRRHRGQKQEPLQLVVDLAGELGPLGLPEDAGPGAGAAEPGLQGVALPGPLWLLDLQVLLPLVLDGAGVLVTLAVGALAGALVLVLALLLRRRHR"
)
```

### 8. miRNA (2 endpoints)

**Pattern**: `{miRNA sequence}`

**Description**: miRNA target prediction and analysis.

**Example Endpoints**:
- `mirna target` - miRNA target prediction
- `mirna binding` - miRNA binding prediction

**Usage Example**:
```python
# Predict miRNA target
result = predict_toxicity(
    endpoint="all",
    mirna_sequence="UGAGGUAGUAGGUUGUAUAGUU"
)
```

### 9. Cell Line (2 endpoints)

**Pattern**: `{Cell line description}`

**Description**: Cell line specific predictions and analysis.

**Example Endpoints**:
- `cell line toxicity` - Cell line toxicity prediction
- `cell line response` - Cell line response prediction

**Usage Example**:
```python
# Predict cell line response
result = predict_toxicity(
    endpoint="all",
    cell_line="MCF-7 breast cancer cell line"
)
```

### 10. Catalyst + Product (2 endpoints)

**Pattern**: `{Catalyst SMILES}`, `{Product SMILES}`

**Description**: Catalytic reaction prediction and analysis.

**Example Endpoints**:
- `catalyst product binding` - Catalyst-product binding prediction
- `catalyst product affinity` - Catalyst-product affinity prediction

**Usage Example**:
```python
# Predict catalytic reaction
result = predict_toxicity(
    endpoint="all",
    catalyst_smiles="[Pd]",
    product_smiles="c1ccccc1"
)
```

### 11. Reactant + Product (2 endpoints)

**Pattern**: `{Reactant SMILES}`, `{Product SMILES}`

**Description**: Chemical reaction prediction and analysis.

**Example Endpoints**:
- `reactant product binding` - Reactant-product binding prediction
- `reactant product affinity` - Reactant-product affinity prediction

**Usage Example**:
```python
# Predict chemical reaction
result = predict_toxicity(
    endpoint="all",
    reactant_smiles="c1ccccc1",
    product_smiles="c1ccccc1"
)
```

### 12. GuideSeq (2 endpoints)

**Pattern**: `{GuideSeq}`

**Description**: CRISPR guide sequence prediction and analysis.

**Example Endpoints**:
- `guideseq target` - GuideSeq target prediction
- `guideseq binding` - GuideSeq binding prediction

**Usage Example**:
```python
# Predict CRISPR guide sequence
result = predict_toxicity(
    endpoint="all",
    guideseq="GGCGAGGUGCUGCUGGGCUU"
)
```

## Validation Rules

The system enforces several validation rules:

1. **Parameter Completeness**: All required parameters for a given endpoint must be provided
2. **Parameter Pairing**: Related parameters must be provided together (e.g., `protein1_sequence` and `protein2_sequence`)
3. **Endpoint Existence**: The specified endpoint must exist in the TDC prompts
4. **Parameter Format**: Parameters must be in the correct format (SMILES, amino acid sequences, etc.)

## Error Handling

Common error scenarios and their solutions:

### Missing Parameters
```python
# Error: Missing required parameter
try:
    result = predict_toxicity(endpoint="bindingdb kd", smiles="c1ccccc1")
    # Missing target_protein parameter
except ValueError as e:
    print(f"Error: {e}")
    # Solution: Add target_protein parameter
    result = predict_toxicity(
        endpoint="bindingdb kd", 
        smiles="c1ccccc1",
        target_protein="MAKVISFVLLLVCFLQ"
    )
```

### Invalid Endpoint
```python
# Error: Endpoint not found
try:
    result = predict_toxicity(endpoint="invalid_endpoint", smiles="c1ccccc1")
except ValueError as e:
    print(f"Error: {e}")
    # Solution: Use valid endpoint name
    result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
```

### Parameter Mismatch
```python
# Error: Parameter mismatch
try:
    result = predict_toxicity(
        endpoint="all",
        protein1_sequence="MAEGEITTFTALTEKFNLPPGNYKKPKLLYCSNGGHFLRILPDGTVDGTRDRSDQHIQLQLSAESVGEVYIKSTETGQYLAMDTDGLLYGSQTPNEECLFLERLEENHYNTYISKKHAEKNWFVGLKKNGSCKRGPRTHYGQKAILFLPLPV"
        # Missing protein2_sequence
    )
except ValueError as e:
    print(f"Error: {e}")
    # Solution: Add protein2_sequence parameter
```

## Best Practices

1. **Use Specific Endpoints**: For single predictions, specify the exact endpoint name
2. **Use "all" for Exploration**: Use `endpoint="all"` to discover available endpoints for your parameters
3. **Validate Parameters**: Ensure all required parameters are provided before making predictions
4. **Handle Errors**: Always wrap predictions in try-catch blocks
5. **Limit Batch Size**: Use `max_endpoints` parameter for large batch predictions
6. **Check Endpoint Names**: Use the exact endpoint names as shown in the examples above

## Integration Examples

### Basic Integration
```python
from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity

def analyze_compound(smiles):
    """Analyze a compound for multiple toxicity endpoints."""
    results = {}
    
    # Single endpoint predictions
    results['mutagenicity'] = predict_toxicity(endpoint="ames", smiles=smiles)
    results['herg'] = predict_toxicity(endpoint="herg", smiles=smiles)
    results['dili'] = predict_toxicity(endpoint="dili", smiles=smiles)
    
    # All matching endpoints
    all_results = predict_toxicity(endpoint="all", smiles=smiles)
    results['all_endpoints'] = all_results
    
    return results
```

### Advanced Integration
```python
def comprehensive_analysis(compound_data):
    """Perform comprehensive analysis based on available data."""
    results = {}
    
    if 'smiles' in compound_data:
        # SMILES-based analysis
        results['smiles_analysis'] = predict_toxicity(
            endpoint="all", 
            smiles=compound_data['smiles']
        )
    
    if 'antibody_heavy' in compound_data and 'antibody_light' in compound_data:
        # Antibody analysis
        results['antibody_analysis'] = predict_toxicity(
            endpoint="all",
            antibody_heavy=compound_data['antibody_heavy'],
            antibody_light=compound_data['antibody_light']
        )
    
    if 'protein1' in compound_data and 'protein2' in compound_data:
        # Protein-protein interaction analysis
        results['protein_interaction'] = predict_toxicity(
            endpoint="all",
            protein1_sequence=compound_data['protein1'],
            protein2_sequence=compound_data['protein2']
        )
    
    return results
```

This comprehensive reference provides all the information needed to effectively use the TX-Gemma predictor with any of the 703 TDC endpoints.
