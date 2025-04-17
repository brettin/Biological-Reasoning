"""
Configuration package for the biological reasoning system.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Model Configuration
MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "meta-llama/Llama-3.3-70B-Instruct")
MODEL_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
MODEL_API_KEY = os.getenv("OPENAI_API_KEY")

# System Messages
SYSTEM_MESSAGES = {
    "knowledge_retrieval": "You are a biological knowledge retrieval system.",
    "sequence_analysis": "You are a genomic sequence analysis system.",
    "image_analysis": "You are a biological image analysis system.",
    "reasoning_mode": "Determine the most appropriate biological reasoning mode for this query."
}

# API Configuration
OPENTARGETS_BASE_URL = os.getenv("OPENTARGETS_BASE_URL", "https://platform-api.opentargets.io/v3")

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