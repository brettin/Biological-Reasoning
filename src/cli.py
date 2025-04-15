import argparse
from src.coordinator import BiologicalReasoningCoordinator

def main():
    parser = argparse.ArgumentParser(description="Biological Reasoning System CLI")
    parser.add_argument("--query", type=str, help="Biological query to process")
    parser.add_argument("--mode", type=str, choices=["phylogenetic", "teleonomic", "mechanistic"],
                      help="Force a specific reasoning mode")
    args = parser.parse_args()
    
    # Initialize the coordinator
    coordinator = BiologicalReasoningCoordinator()
    
    if args.query:
        # Process the query
        result = coordinator.process_query(args.query)
        print("\nResults:")
        print(f"Query: {result['query']}")
        print(f"Reasoning Mode: {result['reasoning_mode']}")
        print(f"Result: {result['result']}")
    else:
        # Interactive mode
        print("Biological Reasoning System CLI")
        print("Type 'exit' or 'quit' to quit")
        
        while True:
            query = input("\nEnter your biological query: ").lower()
            if query in ['exit', 'quit']:
                break
            
            result = coordinator.process_query(query)
            print("\nResults:")
            print(f"Query: {result['query']}")
            print(f"Reasoning Mode: {result['reasoning_mode']}")
            print(f"Result: {result['result']}")

if __name__ == "__main__":
    main() 