import pytest
from src.state import PatientState
from src.agents.triage_agent import triage_node
from src.agents.researcher_agent import researcher_node
from src.agents.pharmacologist_agent import pharmacologist_node
from src.agents.cmo_agent import cmo_node
from src.llm import get_llm
from langchain_core.prompts import PromptTemplate

def llm_judge(prompt_text: str) -> bool:
    try:
        llm = get_llm()
        # Add instructions to output true or false
        prompt = PromptTemplate.from_template("{text}\nRespond only with 'True' or 'False'.")
        chain = prompt | llm
        response = chain.invoke({"text": prompt_text})
        return "true" in response.content.lower()
    except Exception as e:
        # Strict evaluation behavior: skip judge-dependent assertions if LLM is unavailable.
        pytest.skip(f"LLM judge unavailable: {e}")

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

    # LLM as a judge check on logs
    logs_str = " ".join(result_state["logs"])
    judge_prompt = (
        "Does the following log include a professional 1-sentence acknowledgment of the symptoms? "
        f"Log: {logs_str}"
    )
    assert llm_judge(judge_prompt), "LLM Judge failed: Triage log lacked appropriate acknowledgment."

def test_researcher_agent_output(mock_initial_state):
    """
    STUDENT 2 TEST: Evaluate Researcher Agent accuracy and constraints
    """
    mock_initial_state["symptoms"] = ["headache", "elevated blood pressure"]
    result_state = researcher_node(mock_initial_state)
    
    # Structural and property constraints
    assert "potential_diagnoses" in result_state
    diagnoses = result_state["potential_diagnoses"]
    diagnoses_str = ", ".join(diagnoses)
    judge_prompt = f"Given these are diagnoses for headache and elevated blood pressure: '{diagnoses_str}', are they medically plausible and avoiding out-of-scope guesses like cancer? Respond True if they look reasonable based on guidelines."
    assert llm_judge(judge_prompt), "LLM Judge failed: Diagnoses contain hallucinations or unreasonable suggestions."
    assert isinstance(diagnoses, list), "Diagnoses should be a list"
    assert len(diagnoses) > 0, "Researcher must provide at least one diagnosis"
    assert all("cancer" not in d.lower() for d in diagnoses), "Out-of-scope diagnosis detected."

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
