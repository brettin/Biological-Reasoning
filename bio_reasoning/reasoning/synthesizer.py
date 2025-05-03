from typing import Dict, Any, List
from bio_reasoning.reasoning.state import ReasoningState, LayerResult

class ResultSynthesizer:
    """Combines and synthesizes results from different layers."""
    
    def __init__(self):
        self.conflict_resolution_strategies = {
            'majority_vote': self._resolve_by_majority,
            'confidence_weighted': self._resolve_by_confidence,
            'hierarchical': self._resolve_hierarchically
        }
    
    def synthesize(self, state: ReasoningState) -> Dict[str, Any]:
        """Synthesize results from all layers."""
        if not state.layer_results:
            return {'error': 'No layer results to synthesize'}
        
        # Group results by type
        grouped_results = self._group_results(state.layer_results)
        
        # Resolve conflicts within each group
        resolved_results = {}
        for result_type, results in grouped_results.items():
            resolved_results[result_type] = self._resolve_conflicts(results)
        
        # Combine all results
        final_result = {
            'query': state.query,
            'confidence': state.confidence,
            'status': state.status.name,
            'results': resolved_results,
            'layer_summary': self._create_layer_summary(state.layer_results)
        }
        
        return final_result
    
    def _group_results(self, results: List[LayerResult]) -> Dict[str, List[LayerResult]]:
        """Group results by their type."""
        grouped = {}
        for result in results:
            result_type = self._determine_result_type(result)
            if result_type not in grouped:
                grouped[result_type] = []
            grouped[result_type].append(result)
        return grouped
    
    def _determine_result_type(self, result: LayerResult) -> str:
        """Determine the type of a result based on its content."""
        # This is a simple implementation - in practice, this would be more sophisticated
        if 'sequence' in result.output:
            return 'sequence_analysis'
        elif 'image' in result.output:
            return 'image_analysis'
        elif 'literature' in result.output:
            return 'literature'
        elif 'knowledge' in result.output:
            return 'knowledge'
        else:
            return 'other'
    
    def _resolve_conflicts(self, results: List[LayerResult]) -> Dict[str, Any]:
        """Resolve conflicts between results of the same type."""
        if not results:
            return {}
        
        # Choose resolution strategy based on result type
        strategy = self._choose_resolution_strategy(results)
        return self.conflict_resolution_strategies[strategy](results)
    
    def _choose_resolution_strategy(self, results: List[LayerResult]) -> str:
        """Choose the appropriate conflict resolution strategy."""
        # Simple implementation - in practice, this would be more sophisticated
        if len(results) > 2:
            return 'majority_vote'
        elif any(r.confidence > 0.8 for r in results):
            return 'confidence_weighted'
        else:
            return 'hierarchical'
    
    def _resolve_by_majority(self, results: List[LayerResult]) -> Dict[str, Any]:
        """Resolve conflicts by majority vote."""
        # Count occurrences of each result
        result_counts = {}
        for result in results:
            key = str(result.output)
            if key not in result_counts:
                result_counts[key] = 0
            result_counts[key] += 1
        
        # Find the most common result
        most_common = max(result_counts.items(), key=lambda x: x[1])
        return results[0].output  # Return the first instance of the most common result
    
    def _resolve_by_confidence(self, results: List[LayerResult]) -> Dict[str, Any]:
        """Resolve conflicts by confidence-weighted average."""
        total_confidence = sum(r.confidence for r in results)
        if total_confidence == 0:
            return results[0].output
        
        # Weight results by confidence
        weighted_result = {}
        for result in results:
            weight = result.confidence / total_confidence
            for key, value in result.output.items():
                if key not in weighted_result:
                    weighted_result[key] = 0
                weighted_result[key] += value * weight
        
        return weighted_result
    
    def _resolve_hierarchically(self, results: List[LayerResult]) -> Dict[str, Any]:
        """Resolve conflicts using a hierarchical approach."""
        # Sort results by confidence
        sorted_results = sorted(results, key=lambda x: x.confidence, reverse=True)
        
        # Start with the highest confidence result
        final_result = sorted_results[0].output.copy()
        
        # Add additional information from other results if not conflicting
        for result in sorted_results[1:]:
            for key, value in result.output.items():
                if key not in final_result:
                    final_result[key] = value
        
        return final_result
    
    def _create_layer_summary(self, results: List[LayerResult]) -> Dict[str, Any]:
        """Create a summary of layer results."""
        return {
            'total_layers': len(results),
            'successful_layers': len([r for r in results if not r.error]),
            'failed_layers': len([r for r in results if r.error]),
            'average_confidence': sum(r.confidence for r in results) / len(results) if results else 0,
            'execution_times': {r.layer_name: r.execution_time for r in results}
        } 