import pytest
import os
import tempfile
import shutil
from typing import Dict, Any
from unittest.mock import patch, MagicMock

from src.layers.layer_a.distllm_impl import DistllmParametricMemory
from src.layers.layer_a.config import DistllmConfig


class TestDistllmParametricMemory:
    """Tests for the DistllmParametricMemory implementation."""
    
    @pytest.fixture
    def temp_storage_path(self):
        """Create a temporary directory for storage during tests."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def mock_config(self, temp_storage_path):
        """Create a test configuration."""
        return DistllmConfig(
            pretrained_model="Salesforce/SFR-Embedding-Mistral",
            device="cpu",
            storage_path=temp_storage_path
        )
    
    @pytest.fixture
    def mock_embedder(self):
        """Mock the embedder component."""
        mock = MagicMock()
        mock.embed_text.return_value = [0.1, 0.2, 0.3, 0.4]  # Dummy embedding
        return mock
    
    @pytest.fixture
    def mock_encoder(self):
        """Mock the encoder component."""
        mock = MagicMock()
        mock.get_dimension.return_value = 4  # Dummy dimension
        return mock
    
    @pytest.fixture
    def mock_search(self):
        """Mock the semantic search component."""
        class MockResult:
            def __init__(self, text, score, metadata):
                self.metadata = {"text": text, **metadata}
                self.score = score
        
        mock = MagicMock()
        mock.search.return_value = [
            MockResult("TP53 is a tumor suppressor gene.", 0.95, {"gene": "TP53"}),
            MockResult("TP53 is involved in cell cycle regulation.", 0.85, {"gene": "TP53", "pathway": "cell cycle"})
        ]
        return mock
    
    @pytest.fixture
    def mock_generator(self):
        """Mock the generator component."""
        mock = MagicMock()
        mock.generate.return_value = "TP53 is a tumor suppressor gene that helps prevent cancer."
        return mock
    
    @pytest.mark.skip(reason="Requires distllm to be installed")
    def test_initialization(self, mock_config):
        """Test initialization with proper configuration."""
        with patch('distllm.embed.encoders.AutoEncoder.from_pretrained') as mock_encoder:
            with patch('distllm.embed.poolers.MeanPooler') as mock_pooler:
                with patch('distllm.embed.embedders.SemanticChunkEmbedder') as mock_embedder:
                    with patch('distllm.rag.search.SemanticSearch') as mock_search:
                        with patch('distllm.generate.generators.VLLMGenerator') as mock_generator:
                            memory = DistllmParametricMemory(mock_config)
                            assert memory.config == mock_config
                            assert mock_encoder.called
                            assert mock_pooler.called
                            assert mock_embedder.called
                            assert mock_search.called
                            assert mock_generator.called
    
    @pytest.mark.skip(reason="Requires distllm to be installed")
    def test_store_knowledge(self, mock_config, mock_embedder, mock_encoder, mock_search, mock_generator):
        """Test storing knowledge."""
        with patch('src.layers.layer_a.distllm_impl.AutoEncoder.from_pretrained', return_value=mock_encoder):
            with patch('src.layers.layer_a.distllm_impl.MeanPooler', return_value=MagicMock()):
                with patch('src.layers.layer_a.distllm_impl.SemanticChunkEmbedder', return_value=mock_embedder):
                    with patch('src.layers.layer_a.distllm_impl.SemanticSearch', return_value=mock_search):
                        with patch('src.layers.layer_a.distllm_impl.VLLMGenerator', return_value=mock_generator):
                            memory = DistllmParametricMemory(mock_config)
                            
                            # Test storing knowledge
                            knowledge = {
                                "gene": "TP53",
                                "function": "tumor suppression",
                                "pathways": ["apoptosis", "cell cycle regulation"]
                            }
                            
                            memory.store_knowledge(knowledge)
                            
                            # Check that embeddings were created and added to search index
                            assert mock_embedder.embed_text.called
                            assert mock_search.add_embeddings.called
                            
                            # Check that knowledge was saved to the knowledge store
                            assert "gene" in memory.knowledge_store
                            assert memory.knowledge_store["gene"] == "TP53"
    
    @pytest.mark.skip(reason="Requires distllm to be installed")
    def test_retrieve_knowledge(self, mock_config, mock_embedder, mock_encoder, mock_search, mock_generator):
        """Test retrieving knowledge."""
        with patch('src.layers.layer_a.distllm_impl.AutoEncoder.from_pretrained', return_value=mock_encoder):
            with patch('src.layers.layer_a.distllm_impl.MeanPooler', return_value=MagicMock()):
                with patch('src.layers.layer_a.distllm_impl.SemanticChunkEmbedder', return_value=mock_embedder):
                    with patch('src.layers.layer_a.distllm_impl.SemanticSearch', return_value=mock_search):
                        with patch('src.layers.layer_a.distllm_impl.VLLMGenerator', return_value=mock_generator):
                            memory = DistllmParametricMemory(mock_config)
                            
                            # Test retrieving knowledge
                            result = memory.retrieve_knowledge("What is TP53?")
                            
                            # Check that the query was embedded
                            assert mock_embedder.embed_text.called
                            
                            # Check that search was performed
                            assert mock_search.search.called
                            
                            # Check that results were properly formatted
                            assert result["query"] == "What is TP53?"
                            assert len(result["relevant_knowledge"]) == 2
                            assert "TP53" in result["relevant_knowledge"][0]["text"]
    
    @pytest.mark.skip(reason="Requires distllm to be installed")
    def test_process_query(self, mock_config, mock_embedder, mock_encoder, mock_search, mock_generator):
        """Test processing a query."""
        with patch('src.layers.layer_a.distllm_impl.AutoEncoder.from_pretrained', return_value=mock_encoder):
            with patch('src.layers.layer_a.distllm_impl.MeanPooler', return_value=MagicMock()):
                with patch('src.layers.layer_a.distllm_impl.SemanticChunkEmbedder', return_value=mock_embedder):
                    with patch('src.layers.layer_a.distllm_impl.SemanticSearch', return_value=mock_search):
                        with patch('src.layers.layer_a.distllm_impl.VLLMGenerator', return_value=mock_generator):
                            memory = DistllmParametricMemory(mock_config)
                            
                            # Test processing a query
                            response = memory.process_query("What is the function of TP53?")
                            
                            # Check that knowledge was retrieved
                            assert mock_embedder.embed_text.called
                            assert mock_search.search.called
                            
                            # Check that generation was performed
                            assert mock_generator.generate.called
                            
                            # Check that response was returned
                            assert "TP53" in response
                            assert "tumor suppressor" in response

