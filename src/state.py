from typing import Annotated, TypedDict, List
import operator

class PatientState(TypedDict):
    """
    State Management mechanism for the Healthcare MAS.
    This demonstrates how global state is securely passed from one agent to the next.
    """
    raw_emr_path: str
    patient_info: dict
    symptoms: List[str]
    potential_diagnoses: List[str]
    drug_interactions: List[str]
    final_report_path: str
    
    # Observability - tracking agent execution
    current_step: str
    logs: Annotated[List[str], operator.add]
