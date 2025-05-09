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


class Repository(ABC):
    """Abstract base class for different types of repositories.
    
    This is an internal implementation detail of LayerC and should not be exposed
    outside of this module.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name

    @abstractmethod
    def search(self, query: str) -> Dict[str, Any]:
        """Search the repository for relevant information."""
        pass


class OpenTargetsRepository(Repository):
    """Repository for OpenTargets data."""

    def search(self, query: str) -> Dict[str, Any]:
        """Search OpenTargets for relevant information."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["opentargets"]},
            {"role": "user", "content": f"Search for: {query}"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "query": query,
                "results": result["content"],
                "source": "opentargets",
            }
        else:
            print(f"Error searching OpenTargets: {result['content']}")
            return {}


class PubMedRepository(Repository):
    """Repository for PubMed data."""

    def search(self, query: str) -> Dict[str, Any]:
        """Search PubMed for relevant information."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["pubmed"]},
            {"role": "user", "content": f"Search for: {query}"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "query": query,
                "results": result["content"],
                "source": "pubmed",
            }
        else:
            print(f"Error searching PubMed: {result['content']}")
            return {}


class BioRxivRepository(Repository):
    """Repository for bioRxiv data."""

    def search(self, query: str) -> Dict[str, Any]:
        """Search bioRxiv for relevant information."""
        messages = [
            {"role": "system", "content": SYSTEM_MESSAGES["biorxiv"]},
            {"role": "user", "content": f"Search for: {query}"},
        ]
        
        result = call_model_with_retry(messages, self.model_name)
        if result["success"]:
            return {
                "query": query,
                "results": result["content"],
                "source": "biorxiv",
            }
        else:
            print(f"Error searching bioRxiv: {result['content']}")
            return {}


class LayerC(Layer):
    """Layer C: Integration and synthesis of information from multiple sources.
    
    This layer manages multiple repositories internally and provides a unified
    interface for searching and integrating information from various sources.
    """

    def __init__(self, name: str, model_name: str = MODEL_NAME):
        super().__init__(name)
        self.model_name = model_name
        self._repositories: List[Repository] = []

    def add_repository(self, repository: Repository) -> None:
        """Add a new repository to the layer."""
        self._repositories.append(repository)

    def prepare_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare the input for searching."""
        return {
            "query": query,
            "context": context or {},
            "model_name": self.model_name
        }

    def execute(self, prepared_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute search using all registered repositories."""
        try:
            # Search through all repositories
            all_results = {}
            for repository in self._repositories:
                result = repository.search(prepared_input["query"])
                if result:
                    repository_name = repository.__class__.__name__.lower()
                    all_results[repository_name] = result

            # Instead of making another API call, synthesize the results
            synthesis = "Search results:\n"
            for repo_name, result in all_results.items():
                synthesis += f"\n{repo_name}:\n{result.get('results', 'No results available')}\n"

            return {
                "query": prepared_input["query"],
                "processed_query": synthesis,
                "results": all_results,
            }
        except Exception as e:
            print(f"Error performing search: {e}")
            return {}

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the search output."""
        return isinstance(output, dict) and "query" in output and "processed_query" in output

    def format_results(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Format the search results."""
        return {
            "query": output["query"],
            "processed_query": output["processed_query"],
            "results": output["results"],
            "source": self.name
        } 