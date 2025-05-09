#!/usr/bin/env python3
import argparse
from bio_reasoning.coordinator import Coordinator


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
    print(f"Layer A: {result['layer_a']}")
    print(f"Layer B: {result['layer_b']}")
    print(f"Layer C: {result['layer_c']}")


if __name__ == "__main__":
    main()
