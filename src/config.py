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
    "phylogenetic": "phylogenetic",
    "teleonomic": "teleonomic",
    "mechanistic": "mechanistic"
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