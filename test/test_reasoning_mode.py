#!/usr/bin/env python3
import argparse
from bio_reasoning.coordinator import Coordinator
import json

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Test reasoning mode selection"
    )
    parser.add_argument("--query", type=str, required=True, help="Biological query to test")
    args = parser.parse_args()

    # Initialize the coordinator
    coordinator = Coordinator()

    # Process the query
    result = coordinator.process_query(args.query)

    # Print the results
    print(f"\nQuery: {args.query}")
    print(f"Reasoning Mode: {result['reasoning_mode']}")
    print("\nLayer Results:")
    #print(f"Layer A: {json.dumps(result['layer_a'], indent=4)}")
    #print(f"Layer B: {json.dumps(result['layer_b'], indent=4)}")
    #print(f"Layer C: {json.dumps(result['layer_c'], indent=4)}")

    # Print the processed query
    print("\nProcessed Query:")
    print(f"Layer A Processed Query: {result['layer_a']['processed_query']}") if result['layer_a'] and 'processed_query' in result['layer_a'] else "No processed query available"
    #print(f"Layer B Processed Query: {result['layer_b']['processed_query']}") if result['layer_b'] and 'processed_query' in result['layer_b'] else "No processed query available"   
    #print(f"Layer C Processed Query: {result['layer_c']['processed_query']}") if result['layer_c'] and 'processed_query' in result['layer_c'] else "No processed query available"

    # Print the knowledge, analysis, and synthesis
    print("\nKnowledge, Analysis, and Synthesis:")
    #print(f"Layer A Knowledge: {json.dumps(result['layer_a']['knowledge'], indent=4)}") if result['layer_a'] and 'knowledge' in result['layer_a'] else "No knowledge available"
    #print(f"Layer B Analysis: {json.dumps(result['layer_b']['analysis'], indent=4)}") if result['layer_b'] and 'analysis' in result['layer_b'] else "No analysis available"
    #print(f"Layer C Results : {json.dumps(result['layer_c']['results'], indent=4)}") if result['layer_c'] and 'results' in result['layer_c'] else "No results available"
    

if __name__ == "__main__":
    main()
