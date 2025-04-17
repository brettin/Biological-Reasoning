"""distllm-based implementation of Parametric Memory."""

from typing import Dict, Any, Optional, List
import os
import json
import logging
from pathlib import Path

try:
    import torch
    from distllm.rag.search import SemanticSearch
    from distllm.embed.encoders import AutoEncoder
    from distllm.embed.poolers import MeanPooler
    from distllm.embed.embedders import SemanticChunkEmbedder
    from distllm.generate.generators import VLLMGenerator
    DISTLLM_AVAILABLE = True
except ImportError:
    logging.warning("distllm is not installed. DistllmParametricMemory will not be available.")
    DISTLLM_AVAILABLE = False

from src.layers.layer_a.base import ParametricMemory
from src.layers.layer_a.config import DistllmConfig
from src.config import SYSTEM_MESSAGES


class DistllmParametricMemory(ParametricMemory):
    """Implementation of Parametric Memory using distllm library.
    
    This implementation uses the distributed inference capabilities of distllm
    to efficiently process and retrieve biological knowledge.
    """
    
    def __init__(self, config: Optional[DistllmConfig] = None):
        """Initialize DistllmParametricMemory with optional configuration.
        
        Args:
            config: Configuration for distllm components. If None, default config is used.
        """
        if not DISTLLM_AVAILABLE:
            raise ImportError(
                "The distllm package is required to use DistllmParametricMemory. "
                "Please install it with 'pip install distllm'."
            )
            
        self.config = config or DistllmConfig()
        super().__init__(self.config.pretrained_model)
        self._initialize_distllm_components()
        self.knowledge_store = {}
    
    def _initialize_model(self):
        """Override base initialization to use distllm instead of OpenAI."""
        # We'll initialize our models in _initialize_distllm_components instead
        pass
    
    def _initialize_distllm_components(self):
        """Initialize distllm components for embedding and generation."""
        try:
            # Initialize encoder
            self.encoder = AutoEncoder.from_pretrained(
                pretrained_model_name_or_path=self.config.pretrained_model,
                device=self.config.device
            )
            
            # Initialize pooler
            self.pooler = MeanPooler()
            
            # Initialize embedder
            self.embedder = SemanticChunkEmbedder(
                encoder=self.encoder,
                pooler=self.pooler,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            
            # Initialize semantic search
            os.makedirs(self.config.storage_path, exist_ok=True)
            index_path = os.path.join(self.config.storage_path, f"{self.config.index_name}.faiss")
            
            # Check if index exists, otherwise create new one
            if os.path.exists(index_path):
                self.search = SemanticSearch.load(index_path)
            else:
                self.search = SemanticSearch(
                    dim=self.encoder.get_dimension(),
                    device=self.config.device
                )
            
            # Initialize generator
            self.generator = VLLMGenerator(
                model_name=self.config.pretrained_model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p
            )
            
            # Load existing knowledge if available
            knowledge_path = os.path.join(self.config.storage_path, "knowledge_store.json")
            if os.path.exists(knowledge_path):
                with open(knowledge_path, 'r') as f:
                    self.knowledge_store = json.load(f)
                    
            logging.info("DistllmParametricMemory initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing distllm components: {e}")
            raise
    
    def store_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Store biological knowledge using embeddings.
        
        Args:
            knowledge: Dictionary containing biological knowledge to store.
        """
        try:
            # Convert knowledge to text format for embedding
            texts = self._prepare_knowledge(knowledge)
            
            # Generate embeddings
            embeddings = []
            for text in texts:
                embedding = self.embedder.embed_text(text)
                embeddings.append(embedding)
            
            # Add to semantic search index
            metadata = [{**knowledge, "text": text} for text in texts]
            self.search.add_embeddings(
                embeddings=embeddings,
                metadata=metadata
            )
            
            # Save to knowledge store
            for key, value in knowledge.items():
                self.knowledge_store[key] = value
            
            # Persist knowledge store
            os.makedirs(self.config.storage_path, exist_ok=True)
            knowledge_path = os.path.join(self.config.storage_path, "knowledge_store.json")
            with open(knowledge_path, 'w') as f:
                json.dump(self.knowledge_store, f)
            
            # Save index
            self.search.save(os.path.join(self.config.storage_path, f"{self.config.index_name}.faiss"))
            
            logging.info(f"Stored knowledge with {len(texts)} text chunks")
            
        except Exception as e:
            logging.error(f"Error storing knowledge: {e}")
            raise
    
    def retrieve_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve relevant biological knowledge using semantic search.
        
        Args:
            query: The query string to search for relevant knowledge.
            
        Returns:
            Dictionary containing relevant knowledge or None if an error occurs.
        """
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed_text(query)
            
            # Perform semantic search
            results = self.search.search(
                query_embedding=query_embedding,
                k=self.config.top_k,
                threshold=self.config.similarity_threshold
            )
            
            # Format results
            return {
                "query": query,
                "relevant_knowledge": [
                    {
                        "text": result.metadata.get("text", ""),
                        "similarity": float(result.score),
                        "metadata": {k: v for k, v in result.metadata.items() if k != "text"}
                    }
                    for result in results
                ]
            }
            
        except Exception as e:
            logging.error(f"Error retrieving knowledge: {e}")
            return None
    
    def process_query(self, query: str) -> str:
        """Process a query using RAG (Retrieval-Augmented Generation).
        
        Args:
            query: The query to process.
            
        Returns:
            Generated response based on retrieved knowledge.
        """
        try:
            # Retrieve relevant knowledge
            knowledge = self.retrieve_knowledge(query)
            
            # Prepare context from retrieved knowledge
            context = self._prepare_context(knowledge)
            
            # Generate response using RAG
            prompt = self.config.rag_template.format(
                context=context,
                query=query
            )
            
            response = self.generator.generate(
                prompt=prompt,
                system_message=SYSTEM_MESSAGES["knowledge_retrieval"]
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            # Fall back to basic method if distllm fails
            return super().process_query(query)
    
    def _prepare_knowledge(self, knowledge: Dict[str, Any]) -> List[str]:
        """Convert knowledge dictionary to list of text chunks.
        
        Args:
            knowledge: Dictionary containing biological knowledge.
            
        Returns:
            List of text chunks suitable for embedding.
        """
        # Convert dictionary to text format
        texts = []
        
        # Add general description if available
        if "description" in knowledge:
            texts.append(knowledge["description"])
        
        # Process structured data
        for key, value in knowledge.items():
            if key == "description":
                continue
                
            if isinstance(value, str):
                texts.append(f"{key}: {value}")
            elif isinstance(value, list):
                texts.append(f"{key}: {', '.join(str(item) for item in value)}")
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    texts.append(f"{key} - {sub_key}: {sub_value}")
        
        return texts
    
    def _prepare_context(self, knowledge: Optional[Dict[str, Any]]) -> str:
        """Format retrieved knowledge for generation.
        
        Args:
            knowledge: Dictionary containing retrieved knowledge.
            
        Returns:
            Formatted context string.
        """
        if not knowledge or "relevant_knowledge" not in knowledge:
            return "No relevant information found."
        
        # Format the context from the relevant knowledge
        context_parts = []
        for i, item in enumerate(knowledge["relevant_knowledge"]):
            text = item.get("text", "")
            metadata = item.get("metadata", {})
            
            context_parts.append(f"[{i+1}] {text}")
            
            # Add metadata if available
            metadata_str = ", ".join([f"{k}: {v

from typing import Dict, Any, Optional, List
import os
import torch
import json
import logging
from pathlib import Path

try:
    from distllm.rag.search import SemanticSearch
    from distllm.embed import Embedder
    from distllm.embed.encoders import AutoEncoder
    from distllm.generate.generators import VLLMGenerator
    from distllm.embed.poolers import MeanPooler
    from distllm.embed.embedders import SemanticChunkEmbedder
except ImportError:
    logging.warning("distllm is not installed. DistllmParametricMemory will not be available.")

from src.layers.layer_a.base import ParametricMemory
from src.layers.layer_a.config import DistllmConfig
from src.config import SYSTEM_MESSAGES


class DistllmParametricMemory(ParametricMemory):
    """Implementation of Parametric Memory using distllm library.
    
    This implementation uses the distributed inference capabilities of distllm
    to efficiently process and retrieve biological knowledge.
    """
    
    def __init__(self, config: Optional[DistllmConfig] = None):
        """Initialize DistllmParametricMemory with optional configuration.
        
        Args:
            config: Configuration for distllm components. If None, default config is used.
        """
        self.config = config or DistllmConfig()
        super().__init__(self.config.pretrained_model)
        self._initialize_distllm_components()
        self.knowledge_store = {}
    
    def _initialize_model(self):
        """Override base initialization to use distllm instead of OpenAI."""
        # We'll initialize our models in _initialize_distllm_components instead
        pass
    
    def _initialize_distllm_components(self):
        """Initialize distllm components for embedding and generation."""
        try:
            # Initialize encoder
            self.encoder = AutoEncoder.from_pretrained(
                pretrained_model_name_or_path=self.config.pretrained_model,
                device=self.config.device
            )
            
            # Initialize pooler
            self.pooler = MeanPooler()
            
            # Initialize embedder
            self.embedder = SemanticChunkEmbedder(
                encoder=self.encoder,
                pooler=self.pooler,
                chunk_size=self.config.chunk_size,
                chunk_overlap=self.config.chunk_overlap
            )
            
            # Initialize semantic search
            os.makedirs(self.config.storage_path, exist_ok=True)
            index_path = os.path.join(self.config.storage_path, f"{self.config.index_name}.faiss")
            
            # Check if index exists, otherwise create new one
            if os.path.exists(index_path):
                self.search = SemanticSearch.load(index_path)
            else:
                self.search = SemanticSearch(
                    dim=self.encoder.get_dimension(),
                    device=self.config.device
                )
            
            # Initialize generator
            self.generator = VLLMGenerator(
                model_name=self.config.pretrained_model,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                top_p=self.config.top_p
            )
            
            # Load existing knowledge if available
            knowledge_path = os.path.join(self.config.storage_path, "knowledge_store.json")
            if os.path.exists(knowledge_path):
                with open(knowledge_path, 'r') as f:
                    self.knowledge_store = json.load(f)
                    
            logging.info("DistllmParametricMemory initialized successfully")
            
        except Exception as e:
            logging.error(f"Error initializing distllm components: {e}")
            raise
    
    def store_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Store biological knowledge using embeddings.
        
        Args:
            knowledge: Dictionary containing biological knowledge to store.
        """
        try:
            # Convert knowledge to text format for embedding
            texts = self._prepare_knowledge(knowledge)
            
            # Generate embeddings
            embeddings = []
            for text in texts:
                embedding = self.embedder.embed_text(text)
                embeddings.append(embedding)
            
            # Add to semantic search index
            metadata = [{**knowledge, "text": text} for text in texts]
            self.search.add_embeddings(
                embeddings=embeddings,
                metadata=metadata
            )
            
            # Save to knowledge store
            for key, value in knowledge.items():
                self.knowledge_store[key] = value
            
            # Persist knowledge store
            os.makedirs(self.config.storage_path, exist_ok=True)
            knowledge_path = os.path.join(self.config.storage_path, "knowledge_store.json")
            with open(knowledge_path, 'w') as f:
                json.dump(self.knowledge_store, f)
            
            # Save index
            self.search.save(os.path.join(self.config.storage_path, f"{self.config.index_name}.faiss"))
            
            logging.info(f"Stored knowledge with {len(texts)} text chunks")
            
        except Exception as e:
            logging.error(f"Error storing knowledge: {e}")
            raise
    
    def retrieve_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve relevant biological knowledge using semantic search.
        
        Args:
            query: The query string to search for relevant knowledge.
            
        Returns:
            Dictionary containing relevant knowledge or None if an error occurs.
        """
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed_text(query)
            
            # Perform semantic search
            results = self.search.search(
                query_embedding=query_embedding,
                k=self.config.top_k,
                threshold=self.config.similarity_threshold
            )
            
            # Format results
            return {
                "query": query,
                "relevant_knowledge": [
                    {
                        "text": result.metadata.get("text", ""),
                        "similarity": float(result.score),
                        "metadata": {k: v for k, v in result.metadata.items() if k != "text"}
                    }
                    for result in results
                ]
            }
            
        except Exception as e:
            logging.error(f"Error retrieving knowledge: {e}")
            return None
    
    def process_query(self, query: str) -> str:
        """Process a query using RAG (Retrieval-Augmented Generation).
        
        Args:
            query: The query to process.
            
        Returns:
            Generated response based on retrieved knowledge.
        """
        try:
            # Retrieve relevant knowledge
            knowledge = self.retrieve_knowledge(query)
            
            # Prepare context from retrieved knowledge
            context = self._prepare_context(knowledge)
            
            # Generate response using RAG
            prompt = self.config.rag_template.format(
                context=context,
                query=query
            )
            
            response = self.generator.generate(
                prompt=prompt,
                system_message=SYSTEM_MESSAGES["knowledge_retrieval"]
            )
            
            return response
            
        except Exception as e:
            logging.error(f"Error processing query: {e}")
            # Fall back to basic method if distllm fails
            return super().process_query(query)
    
    def _prepare_knowledge(self, knowledge: Dict[str, Any]) -> List[str]:
        """Convert knowledge dictionary to list of text chunks.
        
        Args:
            knowledge: Dictionary containing biological knowledge.
            
        Returns:
            List of text chunks suitable for embedding.
        """
        # Convert dictionary to text format
        texts = []
        
        # Add general description if available
        if "description" in knowledge:
            texts.append(knowledge["description"])
        
        # Process structured data
        for key, value in knowledge.items():
            if key == "description":
                continue
                
            if isinstance(value, str):
                texts.append(f"{key}: {value}")
            elif isinstance(value, list):
                texts.append(f"{key}: {', '.join(str(item) for item in value)}")
            elif isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    texts.append(f"{key} - {sub_key}: {sub_value}")
        
        return texts
    
    def _prepare_context(self, knowledge: Optional[Dict[str, Any]]) -> str:
        """Format retrieved knowledge for generation.
        
        Args:
            knowledge: Dictionary containing retrieved knowledge.
            
        Returns:
            Formatted context string.
        """
        if not knowledge or "relevant_knowledge" not in knowledge:
            return "No relevant information found."
        
        # Format the context from the relevant knowledge
        context_parts = []
        for i, item in enumerate(knowledge["relevant_knowledge"]):
            text = item.get("text", "")
            metadata = item.get("metadata", {})
            
            context_parts.append(f"[{i+1}] {text}")
            
            # Add metadata if available
            metadata_str = ", ".join([f"{k}: {v}" for k, v in metadata.items()])
            if metadata_str:
                context_parts.append(f"Metadata: {metadata_str}")
            
            context_parts.append("")  # Add blank line between entries
        
        return "\n".join(context_parts)

