#!/usr/bin/env python3
import argparse
from bio_reasoning.coordinator import Coordinator
from bio_reasoning.config import get_agent_config
import json

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Test reasoning mode selection"
    )
    parser.add_argument("--query", type=str, default="What is the function of TP53?", help="Biological query to test")
    args = parser.parse_args()

    # Initialize the coordinator
    config = get_agent_config()
    coordinator = Coordinator(config=config)

    # Process the query
    result = coordinator.query(args.query)

    # Print the results
    print(f"\nQuery: {args.query}")
    print(f"Reasoning Mode: {result['reasoning_mode']}")
    print("\nLayer Results:")


    # Print the processed query
    print("\nProcessed Query:")
    print(f"Layer A Processed Query: {result['layer_a']['processed_query']}") if result['layer_a'] and 'processed_query' in result['layer_a'] else "No processed query available"

    # Print the knowledge, analysis, and synthesis
    print("\nKnowledge, Analysis, and Synthesis:")
    

if __name__ == "__main__":
    main()
