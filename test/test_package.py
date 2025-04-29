from bio_reasoning.coordinator import BiologicalReasoningCoordinator
import json

def test_package():
    try:
        # Initialize the coordinator
        coordinator = BiologicalReasoningCoordinator()
        print("Successfully initialized BiologicalReasoningCoordinator")
        
        # Test a simple query
        result = coordinator.process_query("What is the function of TP53?")
        print("Successfully processed query")
        print(json.dumps(result, indent=4))
        #print("Result:", result)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_package() 
