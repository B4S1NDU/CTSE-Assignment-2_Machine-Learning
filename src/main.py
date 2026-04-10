from src.graph import build_graph
import pprint
import logging

# Central observability via logging configuration
logging.basicConfig(
    filename='execution.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    print("Initializing Healthcare MAS...")
    logging.info("System Initialized.")
    
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
    logging.info(f"Starting pipeline execution with state: {initial_state}")
    
    final_state = app.invoke(initial_state)
    
    print("\n--- Final State Output ---")
    pprint.pprint(final_state)
    logging.info(f"Pipeline finished. Final State: {final_state}")
    print(f"\nReport generated at: {final_state.get('final_report_path')}")

if __name__ == "__main__":
    main()
