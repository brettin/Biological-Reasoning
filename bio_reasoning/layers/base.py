from typing import Dict, Any, Optional
from abc import ABC, abstractmethod

class Layer(ABC):
    """Base class for all layers in the biological reasoning system.
    
    This class defines the structure and behavior for all layers in the system.
    It provides a standardized interface for layer implementations and manages
    the state of each layer.
    
    Attributes:
        name (str): The name of the layer.
        state (LayerState): The state of the layer.
    
    Layers as Objects:
    Each layer now has its own state management
    Layers control their own execution pipeline through the process method
    
    Layer Execution Control:
    Added clear methods for input preparation, execution, validation, and result formatting
    Each layer can now manage its own execution flow
    Added state tracking to monitor layer execution
    
    Layer State Management:
    Each layer has its own state object
    State is updated through the state.update method
    State can be accessed through the state.get method
    State is used to track the status of the layer
    State is used to track the last query and output
    
    """
    
    def __init__(self, name: str):
        self.name = name
        self.state = LayerState()
    
    @abstractmethod
    def prepare_input(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Prepare the input for layer execution."""
        pass
    
    @abstractmethod
    def execute(self, prepared_input: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the layer's main processing logic."""
        pass
    
    @abstractmethod
    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate the layer's output."""
        pass
    
    @abstractmethod
    def format_results(self, output: Dict[str, Any]) -> Dict[str, Any]:
        """Format the layer's results for downstream consumption."""
        pass
    
    def process(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a query through the layer."""
        try:
            # Prepare input
            prepared_input = self.prepare_input(query, context)
            
            # Execute layer logic
            output = self.execute(prepared_input)
            
            # Validate output
            if not self.validate_output(output):
                raise ValueError(f"Invalid output from layer {self.name}")
            
            # Format results
            formatted_results = self.format_results(output)
            
            # Update state
            self.state.update({
                'last_query': query,
                'last_output': formatted_results,
                'status': 'completed'
            })
            
            return formatted_results
            
        except Exception as e:
            self.state.update({
                'status': 'error',
                'error': str(e)
            })
            raise

class LayerState:
    """Tracks the state of a layer."""
    
    def __init__(self):
        self._state = {
            'status': 'initialized',
            'last_query': None,
            'last_output': None,
            'error': None
        }
    
    def update(self, updates: Dict[str, Any]):
        """Update the layer state."""
        self._state.update(updates)
    
    def get(self, key: str) -> Any:
        """Get a state value."""
        return self._state.get(key)
    
    @property
    def status(self) -> str:
        """Get the current status."""
        return self._state['status']
    
    @property
    def is_completed(self) -> bool:
        """Check if the layer has completed processing."""
        return self._state['status'] == 'completed'
    
    @property
    def has_error(self) -> bool:
        """Check if the layer has an error."""
        return self._state['status'] == 'error' 