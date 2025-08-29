TX-Gemma Predictor
==================

.. automodule:: bio_reasoning.layers.b.txgemma_predictor
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The TX-Gemma predictor provides access to Google's TX-Gemma model for molecular toxicity prediction using standardized prompts from the Therapeutics Data Commons (TDC).

Key Features
------------

- **Parameter-Driven API**: Automatically determines which prompts to use based on provided parameters
- **703 TDC Endpoints**: Support for all endpoints in the Therapeutics Data Commons
- **12 Parameter Combinations**: From single SMILES to complex antibody-protein interactions
- **No Universal SMILES Requirement**: Supports antibody, peptide-MHC, protein-protein endpoints
- **Automatic Fallback**: Falls back to primary LLM when TX-Gemma unavailable
- **Dynamic Discovery**: All endpoints automatically discovered from TDC prompts

Parameter Combinations
----------------------

The system supports 12 distinct parameter combinations covering 703 TDC endpoints:

1. **Single SMILES** (671 endpoints): Basic molecular toxicity prediction
2. **Dual SMILES** (2 endpoints): Drug combination analysis
3. **SMILES + Protein** (6 endpoints): Drug-target binding affinity
4. **Antibody** (2 endpoints): Antibody-antigen interactions
5. **Peptide + MHC** (2 endpoints): Peptide-MHC binding prediction
6. **Epitope + TCR** (2 endpoints): T-cell receptor interactions
7. **Protein-Protein** (2 endpoints): Protein-protein interactions
8. **miRNA** (2 endpoints): miRNA target prediction
9. **Cell Line** (2 endpoints): Cell line specific predictions
10. **Catalyst + Product** (2 endpoints): Catalytic reaction prediction
11. **Reactant + Product** (2 endpoints): Chemical reaction prediction
12. **GuideSeq** (2 endpoints): CRISPR guide sequence prediction

Configuration
-------------

TX-Gemma uses the centralized configuration system. Required environment variables:

.. code-block:: bash

   BIO_TXGEMMA_API_KEY=your_api_key
   BIO_TXGEMMA_BASE_URL=http://localhost:8000/v1
   BIO_TXGEMMA_MODEL_NAME=google/txgemma-27b-chat

Optional configuration:

.. code-block:: bash

   BIO_TXGEMMA_TEMPERATURE=0.1
   BIO_TXGEMMA_MAX_TOKENS=2048
   BIO_TXGEMMA_TIMEOUT=60

Usage Examples
--------------

Basic single SMILES prediction:

.. code-block:: python

   from bio_reasoning.layers.b.txgemma_predictor import predict_toxicity
   
   result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
   print(result)

Predict all matching endpoints:

.. code-block:: python

   all_results = predict_toxicity(endpoint="all", smiles="c1ccccc1")
   for endpoint, prediction in all_results.items():
       print(f"{endpoint}: {prediction}")

Antibody prediction (no SMILES required):

.. code-block:: python

   antibody_results = predict_toxicity(
       endpoint="all",
       antibody_heavy="QVQLVQSGAEVKKPGASVKVSCKASGYTFTNYWMQWVKQRPGQGLEWIGYINPYNDGTKYNEKFKGKATLTADKSSSTAYMQLSSLTSEDSAVYYCARYYDDHYCLDYWGQGTTLTVSS",
       antibody_light="DIQMTQSPSSLSASVGDRVTITCRASQSISSYLNWYQQKPGKAPKLLIYASQSISGIPSRFSGSGSGTDFTLTISSLQPEDFATYYCQQSYSTPFTFGQGTKVEIK"
   )

Error Handling
--------------

The system provides graceful error handling:

.. code-block:: python

   try:
       result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")
       print(f"Prediction: {result}")
   except ValueError as e:
       print(f"Invalid endpoint: {e}")
   except Exception as e:
       print(f"Prediction failed: {e}")

Fallback Behavior
-----------------

When TX-Gemma is not available, the system automatically falls back to the primary LLM:

.. code-block:: python

   # If TX-Gemma is down, this will use the primary LLM
   result = predict_toxicity(endpoint="ames", smiles="c1ccccc1")

Integration with Biological Reasoning
------------------------------------

TX-Gemma integrates seamlessly with the Biological Reasoning Framework:

.. code-block:: python

   from bio_reasoning.coordinator import Coordinator
   from bio_reasoning.config import ConfigManager
   
   # Create coordinator with TX-Gemma support
   config = ConfigManager.get_config()
   coordinator = Coordinator(config=config.get_endpoint("primary").to_agent_config())
   
   # TX-Gemma predictions are automatically available in Layer B
   # when the toxicology reasoning mode is used



