from src.graph import build_graph
import pprint
import logging

from src.logger import logger

def main():
    print("Initializing Healthcare MAS...")
    logger.info("System Initialized.")
    
    # Compile the LangGraph
    app = build_graph()
    
    # Initial State
    initial_state = {
        "raw_emr_path": "data/mock_patient.json",
        "patient_info": {},
        "symptoms": [],
        "potential_diagnoses": [],
        "drug_interactions": [],
        "final_report_path": "",
        "current_step": "start",
        "logs": ["System initialized"]
    }
    
    # Execute the graph locally
    print("\nStarting execution trace:\n")
    logger.info(f"Starting pipeline execution with state: {initial_state}")
    
    try:
        final_state = app.invoke(initial_state)
        
        print("\n--- Final State Output ---")
        pprint.pprint(final_state)
        logger.info(f"Pipeline finished. Final State: {final_state}")
        print(f"\nReport generated at: {final_state.get('final_report_path')}")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {e}", exc_info=True)
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
