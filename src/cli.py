import argparse
from src.coordinator import BiologicalReasoningCoordinator

def format_result(result):
    """Format the result dictionary into a readable string."""
    output = []
    output.append(f"Query: {result['query']}")
    output.append(f"Reasoning Mode: {result['reasoning_mode']}")
    
    if 'error' in result:
        output.append(f"Error: {result['error']}")
        return '\n'.join(output)
    
    if 'result' in result:
        result_data = result['result']
        output.append("\nFindings:")
        
        # Add knowledge from Layer A if available
        if 'knowledge' in result_data:
            output.append("\nBackground Knowledge:")
            output.append(str(result_data['knowledge']))
        
        # Add sequence analysis if available
        if 'sequence_analysis' in result_data:
            output.append("\nSequence Analysis:")
            output.append(str(result_data['sequence_analysis']))
        
        # Add target data if available
        if 'target_data' in result_data:
            output.append("\nTarget Analysis:")
            output.append(str(result_data['target_data']))
        
        # Summarize literature
        if 'literature' in result_data:
            output.append("\nRelevant Literature:")
            if 'pubmed' in result_data['literature']:
                pubmed_count = len(result_data['literature']['pubmed'])
                output.append(f"- Found {pubmed_count} relevant PubMed articles")
            if 'biorxiv' in result_data['literature']:
                biorxiv_count = len(result_data['literature']['biorxiv'])
                output.append(f"- Found {biorxiv_count} relevant BioRxiv preprints")
    
    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Biological Reasoning System CLI")
    parser.add_argument("--query", help="Biological query to process")
    parser.add_argument("--mode", choices=["phylogenetic", "teleonomic", "mechanistic"], 
                       help="Reasoning mode to use")
    args = parser.parse_args()
    
    # Initialize the coordinator
    coordinator = BiologicalReasoningCoordinator()
    
    if args.query:
        # Process the query
        result = coordinator.process_query(args.query)
        print(format_result(result))
    else:
        # Interactive mode
        print("Biological Reasoning System CLI\nType 'exit' or 'quit' to quit")
        
        while True:
            query = input("\nEnter your biological query: ")
            if query.lower() in ['exit', 'quit']:
                break
            
            result = coordinator.process_query(query)
            print(format_result(result))

if __name__ == "__main__":
    main() 