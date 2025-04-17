"""Configuration settings for the biological reasoning system."""

# Model Configuration
MODEL_NAME = "scout"
MODEL_BASE_URL = "http://localhost:9999/v1"
MODEL_API_KEY = "CELS"

# System Messages
SYSTEM_MESSAGES = {
    "knowledge_retrieval": "You are a biological knowledge retrieval system.",
    "sequence_analysis": "You are a genomic sequence analysis system.",
    "image_analysis": "You are a biological image analysis system.",
    "reasoning_mode": "Determine the most appropriate biological reasoning mode for this query."
}

# API Configuration
OPENTARGETS_BASE_URL = "https://platform-api.opentargets.io/v3"

# Reasoning Modes
REASONING_MODES = {
    "phylogenetic": "Uses evolutionary relationships (via genetic or phenotypic comparisons) to infer common ancestry, divergence, and the historical origins of traits. It relies on sequence alignments, phylogenetic trees, and taxonomic data to transfer knowledge among organisms.",
    "teleonomic": "Explains traits in terms of their purpose or function—that is, how a trait may confer a fitness advantage. It connects observed biological features with their adaptive benefits, often drawing on well‐documented case studies (e.g., beak shapes in finches).",
    "tradeoff": "Recognizes that organisms have finite resources and that optimizing one trait can come at the expense of another. This mode evaluates how biological systems balance competing demands (like growth versus reproduction or enzyme efficiency versus stability) and is supported by quantitative data and optimization models.",
    "mechanistic": "Focuses on the cause‐and‐effect processes underlying biological functions. It breaks down complex phenomena (e.g., metabolic pathways, signal transduction, muscle contraction) into component interactions and causal chains to explain 'how' a process works.",
    "systems": "Examines whole networks and emergent properties that arise from the interactions of many components. It is used to model and interpret complex behaviors (such as oscillations or robust cellular responses) in gene regulatory networks, metabolic circuits, or ecological systems.",
    "spatial": "Deals with the arrangement and physical distribution of biological components. This mode explains how spatial organization—from molecular structures and cellular architecture to tissue patterns—impacts function, using principles like diffusion, pattern formation, and geometry.",
    "temporal": "Addresses the time course of biological events by considering timing, sequence, rates, and cycles. It explains dynamic processes such as circadian rhythms, developmental stages, and temporal changes in molecular or physiological systems.",
    "homeostatic": "Describes how organisms maintain internal stability through feedback mechanisms. It focuses on the regulatory loops that keep physiological variables (e.g., temperature, blood glucose, pH) within optimal ranges, identifying both the mechanisms and consequences of homeostasis failures.",
    "ontogenetic": "Explores the processes by which an individual organism develops from embryo to adult. It explains how sequential, spatially coordinated events (e.g., induction, differentiation, morphogen gradients) lead to the formation of complex structures and functions.",
    "comparative": "Uses analogies and comparisons across different species or biological systems to draw inferences. By comparing model organisms to less-studied systems, it transfers insights (such as gene function or developmental patterns) across evolutionary boundaries."
}

# Mock Data (for development)
MOCK_DATA = {
    "opentargets": {
        "target": {
            "id": "ENSG00000141510",  # TP53
            "approvedSymbol": "TP53",
            "approvedName": "Tumor protein p53",
            "targetClass": "Protein Coding",
            "diseases": [
                {
                    "id": "EFO_0000222",
                    "name": "breast carcinoma"
                }
            ]
        }
    },
    "literature": {
        "papers": [
            {
                "title": "Example Paper Title",
                "authors": ["Author 1", "Author 2"],
                "year": 2023,
                "abstract": "Example abstract text"
            }
        ]
    }
} 