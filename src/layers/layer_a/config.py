"""Configuration for distllm-based Parametric Memory implementation."""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any


@dataclass
class DistllmConfig:
    """Configuration for distllm-based ParametricMemory implementation."""
    
    # Model Configuration
    encoder_name: str = "auto"
    pretrained_model: str = "Salesforce/SFR-Embedding-Mistral"  # Good for biomedical domain
    
    # Embedding Configuration
    batch_size: int = 32
    chunk_size: int = 512
    chunk_overlap: int = 128
    pooler_name: str = "mean"
    embedder_name: str = "semantic_chunk"
    
    # Search Configuration
    top_k: int = 5
    similarity_threshold: float = 0.7
    index_name: str = "biological_knowledge"
    
    # Generation Configuration
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    
    # Device Configuration
    device: str = "cuda"  # "cpu" or "cuda"
    
    # Persistence Configuration
    storage_path: str = "./data/knowledge_store"
    
    # RAG Configuration
    rag_template: str = """
    System: You are a biological reasoning system with expertise in biological knowledge.
    
    Context information:
    {context}
    
    User query: {query}
    
    Provide a comprehensive and scientifically accurate response based on the context information.
    """

from dataclasses import dataclass
from typing import List, Optional

@dataclass
class DistllmConfig:
    """Configuration for distllm-based ParametricMemory implementation."""
    
    # Model Configuration
    encoder_name: str = "auto"
    pretrained_model: str = "Salesforce/SFR-Embedding-Mistral"  # Good for biomedical domain
    
    # Embedding Configuration
    batch_size: int = 32
    chunk_size: int = 512
    chunk_overlap: int = 128
    pooler_name: str = "mean"
    embedder_name: str = "semantic_chunk"
    
    # Search Configuration
    top_k: int = 5
    similarity_threshold: float = 0.7
    index_name: str = "biological_knowledge"
    
    # Generation Configuration
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.95
    
    # Device Configuration
    device: str = "cuda"  # "cpu" or "cuda"
    
    # Persistence Configuration
    storage_path: str = "./data/knowledge_store"
    
    # RAG Configuration
    rag_template: str = """
    System: You are a biological reasoning system with expertise in biological knowledge.
    
    Context information:
    {context}
    
    User query: {query}
    
    Provide a comprehensive and scientifically accurate response based on the context information.
    """

