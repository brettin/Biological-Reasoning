from typing import Dict, Any, Optional, List
import openai
from abc import ABC, abstractmethod
from bio_reasoning.config import (
    MODEL_NAME,
    MODEL_BASE_URL,
    MODEL_API_KEY,
    SYSTEM_MESSAGES,
)
from bio_reasoning.utils import call_model_with_retry
from .base import Layer


class ParametricMemory(ABC):
    """Abstract base class for different types of parametric memory.
    
    This is an internal implementation detail of LayerA and should not be exposed
    outside of this module.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name

    @abstractmethod
    def retrieve(self, query: str) -> Dict[str, Any]:
        """Retrieve knowledge from the memory store."""
        pass


class InMemoryKnowledgeStore(ParametricMemory):
    """A simple in-memory knowledge store."""

    def retrieve(self, query: str) -> Dict[str, Any]:
        """Retrieve knowledge from the in-memory store."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["knowledge_retrieval"]},
            {"role": "user", "content": f"Query: {query}"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "query": query,
                "knowledge": result["content"],
                "source": "in_memory",
            }
        else:
            print(f"Error retrieving knowledge: {result['content']}")
            return {}


class LayerA(Layer):
    """Layer A: Parametric memory for biological knowledge.
    
    This layer manages multiple parametric memory stores internally and provides a unified
    interface for knowledge retrieval.
    """

    def __init__(self, name: str, model_name: str = MODEL_NAME):
        super().__init__(name)
        self.model_name = model_name
        self._knowledge_stores: List[ParametricMemory] = []

    def add_knowledge_store(self, store: ParametricMemory) -> None:
        """Add a new knowledge store to the layer."""
        self._knowledge_stores.append(store)

    def prepare_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare the input for knowledge retrieval."""
        return {
            "query": query,
            "context": context or {},
            "model_name": self.model_name
        }

    def execute(self, prepared_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute knowledge retrieval using all registered stores."""
        try:
            # Retrieve knowledge from all stores
            all_knowledge = {}
            for store in self._knowledge_stores:
                result = store.retrieve(prepared_input["query"])
                if result:
                    store_name = store.__class__.__name__.lower()
                    all_knowledge[store_name] = result

            # Instead of making another API call, synthesize the results
            synthesis = "Knowledge retrieval results:\n"
            for store_name, result in all_knowledge.items():
                synthesis += f"\n{store_name}:\n{result.get('knowledge', 'No knowledge available')}\n"

            return {
                "query": prepared_input["query"],
                "processed_query": synthesis,
                "knowledge": all_knowledge,
            }
        except Exception as e:
            print(f"Error performing knowledge retrieval: {e}")
            return {}

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the knowledge retrieval output."""
        return isinstance(output, dict) and "query" in output and "processed_query" in output

    def format_results(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Format the knowledge retrieval results."""
        return {
            "query": output["query"],
            "processed_query": output["processed_query"],
            "knowledge": output["knowledge"],
            "source": self.name
        }
