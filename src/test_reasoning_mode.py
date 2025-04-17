#!/usr/bin/env python3
import argparse
from coordinator import BiologicalReasoningCoordinator

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Test the reasoning mode determination")
    parser.add_argument("--query", required=True, help="Biological query to analyze")
    args = parser.parse_args()

    # Initialize the coordinator
    coordinator = BiologicalReasoningCoordinator()

    # Determine the reasoning mode
    reasoning_mode = coordinator.determine_reasoning_mode(args.query)

    # Print the result
    print(f"\nQuery: {args.query}")
    print(f"Selected Reasoning Mode: {reasoning_mode}")

if __name__ == "__main__":
    main() 