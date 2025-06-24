from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum, auto

class ReasoningStatus(Enum):
    """Possible states of the reasoning process."""
    INITIALIZED = auto()
    RUNNING = auto()
    COMPLETED = auto()
    ERROR = auto()
    CONVERGED = auto()
    DIVERGED = auto()

@dataclass
class LayerResult:
    """Results from a single layer execution."""
    layer_name: str
    output: Dict[str, Any]
    confidence: float
    execution_time: float
    error: Optional[str] = None

@dataclass
class ReasoningState:
    """Tracks the state of the reasoning process."""
    query: str
    status: ReasoningStatus = ReasoningStatus.INITIALIZED
    layer_results: List[LayerResult] = field(default_factory=list)
    current_layer: Optional[str] = None
    confidence: float = 0.0
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_layer_result(self, result: LayerResult):
        """Add a layer result to the state."""
        self.layer_results.append(result)
        self._update_confidence()
        self._check_convergence()
    
    def _update_confidence(self):
        """Update the overall confidence based on layer results."""
        if not self.layer_results:
            self.confidence = 0.0
            return
        
        # Simple average of layer confidences
        total_confidence = sum(r.confidence for r in self.layer_results)
        self.confidence = total_confidence / len(self.layer_results)
    
    def _check_convergence(self):
        """Check if the reasoning has converged."""
        if len(self.layer_results) < 2:
            return
        
        # Check if the last two results are similar enough
        last_result = self.layer_results[-1]
        prev_result = self.layer_results[-2]
        
        # Simple similarity check - in practice, this would be more sophisticated
        if abs(last_result.confidence - prev_result.confidence) < 0.1:
            self.status = ReasoningStatus.CONVERGED
        elif len(self.layer_results) >= 3:
            # If we've gone through multiple iterations without convergence
            self.status = ReasoningStatus.DIVERGED
    
    def get_layer_result(self, layer_name: str) -> Optional[LayerResult]:
        """Get the result for a specific layer."""
        for result in self.layer_results:
            if result.layer_name == layer_name:
                return result
        return None
    
    def is_complete(self) -> bool:
        """Check if the reasoning process is complete."""
        return self.status in [ReasoningStatus.COMPLETED, 
                             ReasoningStatus.CONVERGED,
                             ReasoningStatus.DIVERGED,
                             ReasoningStatus.ERROR]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the reasoning state."""
        return {
            'query': self.query,
            'status': self.status.name,
            'confidence': self.confidence,
            'current_layer': self.current_layer,
            'layer_count': len(self.layer_results),
            'error': self.error,
            'metadata': self.metadata
        } 