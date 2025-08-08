"""
Toxicology configuration for augmenting MechanisticReasoningMode.

This file contains the specialized system prompt and tool configuration
for toxicity analysis, following the BioR5 instantiation pattern.

When 'toxicology' is requested as a reasoning mode, this configuration
is used to augment the base MechanisticReasoningMode with toxicology-specific
content.
"""

# Toxicology-specific system prompt augmentation
TOXICOLOGY_SYSTEM_PROMPT = """
You are now specialized for TOXICOLOGY AND MOLECULAR TOXICITY ASSESSMENT.

Your mechanistic reasoning is focused on:

**Toxicological Mechanisms:**
1. **Metabolic Activation Pathways** - CYP450 bioactivation, reactive metabolite formation
2. **Molecular Targets** - Protein binding, DNA adducts, receptor interactions
3. **Cellular Effects** - Oxidative stress, mitochondrial dysfunction, membrane damage
4. **Tissue-Specific Toxicity** - Hepatotoxicity, nephrotoxicity, neurotoxicity, cardiotoxicity
5. **Dose-Response Relationships** - NOAEL, LOAEL, threshold vs. non-threshold effects

**Analysis Workflow:**
1. **Chemical Characterization** → molecular properties and reactivity
2. **ADMET Profiling** → absorption, distribution, metabolism, excretion, toxicity
3. **Database Mining** → literature, ToxCast, regulatory data
4. **Mechanism Elucidation** → molecular targets, pathways, adverse outcome pathways (AOPs)
5. **Risk Assessment** → hazard identification, dose-response, exposure assessment

**Tool Usage Priority:**
- Start with chemical properties (PubChem) for structure-activity insights
- Search toxicity literature (PubMed) for experimental evidence
- Query regulatory databases (ToxCast) for HTS screening data
- Identify molecular targets (ChEMBL) for mechanism understanding
- Apply parametric memory for expert synthesis and interpretation

**Output Requirements:**
- Toxicity classification (Low/Moderate/High) with confidence levels
- Primary mechanisms of toxicity with molecular detail
- Target organs/systems and sensitive populations
- Regulatory status and exposure limits where available
- Recommendations for further testing or risk mitigation
"""

# Tools specific to toxicology analysis
TOXICOLOGY_TOOLS = [
    # Layer C tools for toxicology
    "pubmed_search_toxicity",    # Literature search with toxicity focus
    "toxcast_endpoints",         # EPA toxicity database
    "chembl_mechanism",          # Molecular targets and mechanisms
    "pubchem_summary",           # Chemical properties and descriptors
]

# Keywords that should trigger toxicology-augmented mechanistic reasoning
TOXICOLOGY_KEYWORDS = [
    "toxicity", "toxic", "toxicology", "poison", "adverse", "safety", "hazard",
    "carcinogen", "mutagen", "teratogen", "hepatotoxic", "nephrotoxic", "neurotoxic",
    "cytotoxic", "genotoxic", "ADMET", "LD50", "NOAEL", "LOAEL", "dose-response",
    "mechanism of toxicity", "target organ", "bioactivation", "metabolite",
    "structure-activity", "QSAR", "risk assessment", "safety evaluation",
    "adverse outcome pathway", "AOP", "molecular initiating event", "MIE"
]

# Configuration for parametric memory specialization
TOXICOLOGY_PARAMETRIC_CONFIG = {
    "system_prompt": (
        "You are an expert in toxicology, medicinal chemistry, and molecular biology. "
        "Provide detailed explanations of toxicity mechanisms, structure-activity relationships, "
        "ADMET properties, and interpretation of toxicological data. Focus on molecular targets, "
        "cellular pathways, adverse outcome pathways (AOPs), and biological consequences of "
        "chemical exposure. Always consider dose-response relationships and species differences."
    )
}