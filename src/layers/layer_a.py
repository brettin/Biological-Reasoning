from typing import Dict, Any, Optional
import openai
from abc import ABC, abstractmethod
from src.config import MODEL_NAME, MODEL_BASE_URL, MODEL_API_KEY, SYSTEM_MESSAGES

class ParametricMemory(ABC):
    """Layer A: Parametric Memory for storing and retrieving broad biological knowledge."""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the model connection."""
        # Configure the client to use the local model endpoint
        self.client = openai.OpenAI(
            base_url=MODEL_BASE_URL,
            api_key=MODEL_API_KEY
        )
    
    @abstractmethod
    def store_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Store biological knowledge in the parametric memory."""
        pass
    
    @abstractmethod
    def retrieve_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve relevant biological knowledge based on a query."""
        pass
    
    def process_query(self, query: str) -> str:
        """Process a natural language query using the language model."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_MESSAGES["knowledge_retrieval"]},
                    {"role": "user", "content": query}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error processing query: {e}")
            return None

class BiologicalKnowledgeStore(ParametricMemory):
    """Concrete implementation of Parametric Memory for biological knowledge."""
    
    def __init__(self, model_name: str = MODEL_NAME):
        super().__init__(model_name)
        self.knowledge_base = {}
    
    def store_knowledge(self, knowledge: Dict[str, Any]) -> None:
        """Store biological knowledge in the knowledge base."""
        for key, value in knowledge.items():
            self.knowledge_base[key] = value
    
    def retrieve_knowledge(self, query: str) -> Optional[Dict[str, Any]]:
        """Retrieve relevant biological knowledge based on a query."""
        try:
            # Use the language model to determine relevant knowledge
            processed_query = self.process_query(query)
            
            # In a real implementation, this would use vector similarity search
            # For now, we'll return a simple mock response
            return {
                "query": query,
                "processed_query": processed_query,
                "relevant_knowledge": self.knowledge_base.get(query, {})
            }
        except Exception as e:
            print(f"Error retrieving knowledge: {e}")
            return None 