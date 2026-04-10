import pytest
from src.state import PatientState
from src.agents.triage_agent import triage_node
from src.agents.researcher_agent import researcher_node
from src.agents.pharmacologist_agent import pharmacologist_node
from src.agents.cmo_agent import cmo_node

# To evaluate the agents properly, we use simple property-based testing and keyword checks
# simulating an "LLM-as-a-judge" methodology without relying exclusively on LLM availability.

@pytest.fixture
def mock_initial_state() -> PatientState:
    return {
        "raw_emr_path": "data/mock_patient.json",
        "patient_info": {},
        "symptoms": [],
        "potential_diagnoses": [],
        "drug_interactions": [],
        "final_report_path": "",
        "current_step": "start",
        "logs": []
    }

def test_triage_agent_output(mock_initial_state):
    """
    STUDENT 1 TEST: Evaluate Triage Agent output constraints and accuracy
    """
    result_state = triage_node(mock_initial_state)
    
    # 1. Structural constraints
    assert "patient_info" in result_state
    assert "symptoms" in result_state
    
    # 2. Content accuracy check
    assert isinstance(result_state["symptoms"], list), "Symptoms should be extracted as a list"
    assert "current_step" in result_state
    assert result_state["current_step"] == "triage_completed"
    assert len(result_state["logs"]) > 0

def test_researcher_agent_output(mock_initial_state):
    """
    STUDENT 2 TEST: Evaluate Researcher Agent accuracy and constraints
    """
    mock_initial_state["symptoms"] = ["headache", "elevated blood pressure"]
    result_state = researcher_node(mock_initial_state)
    
    # Structural and property constraints
    assert "potential_diagnoses" in result_state
    diagnoses = result_state["potential_diagnoses"]
    assert isinstance(diagnoses, list), "Diagnoses should be a list"
    assert len(diagnoses) > 0, "Researcher must provide at least one diagnosis"
    
    # Constraints check (prevent hallucination of unrelated conditions)
    # E.g., shouldn't contain "cancer" based on generic symptoms if not in guidelines

def test_pharmacologist_agent_output(mock_initial_state):
    """
    STUDENT 3 TEST: Evaluate Pharmacologist Agent output for safety assertions
    """
    mock_initial_state["potential_diagnoses"] = ["Hypertension"]
    mock_initial_state["patient_info"] = {"current_medications": ["Ibuprofen"]}
    
    result_state = pharmacologist_node(mock_initial_state)
    
    # Safety Check: Severe warnings should be logged for contraindications
    interactions = result_state["drug_interactions"]
    assert isinstance(interactions, list)
    assert any("WARNING" in msg.upper() for msg in interactions), "Pharmacologist missed a critical drug interaction constraint."

def test_cmo_agent_output(mock_initial_state):
    """
    STUDENT 4 TEST: Evaluate CMO Agent output securely writes and formats report
    """
    mock_initial_state["patient_info"] = {"name": "Test Patient", "age": 45}
    mock_initial_state["symptoms"] = ["headache"]
    mock_initial_state["potential_diagnoses"] = ["Hypertension"]
    mock_initial_state["drug_interactions"] = ["WARNING: Ibuprofen check"]
    
    result_state = cmo_node(mock_initial_state)
    
    # Formatting and System Constraints Check
    assert "final_report_path" in result_state
    assert result_state["final_report_path"].endswith(".md")
    assert result_state["current_step"] == "cmo_completed"
