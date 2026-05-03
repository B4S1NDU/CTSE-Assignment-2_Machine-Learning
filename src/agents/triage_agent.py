from src.state import PatientState
from src.tools.emr_reader import read_emr
from src.tools.triage_acuity import assess_triage_acuity
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm
import json

from src.logger import log_agent_execution

def triage_node(state: PatientState):
    """
    STUDENT 1 AGENT: Triage Specialist
    """
    print("--- [Agent 1] TRIAGE SPECIALIST ---")
    errors = []
    
    # Use Tool
    try:
        emr_data = read_emr(state.get("raw_emr_path", "data/mock_patient.json"))
    except Exception as e:
        log_agent_execution("TriageAgent", state, error=e)
        return {
            "current_step": "triage_failed",
            "logs": ["Triage Agent failed to read EMR input."],
            "errors": ["TriageAgent: EMR read failed"]
        }
    
    # Provide safe fallback data directly from tool, but also invoke LLM for assignment criteria
    llm = get_llm()
    
    # EXCEPTIONAL PROMPT ENGINEERING for Student 1 Agent
    prompt = PromptTemplate.from_template(
        "You are an expert Triage Nurse operating in a high-stakes clinical environment. "
        "Your role is to strictly acknowledge patient metrics without offering medical diagnoses. "
        "Given this raw JSON EMR data: {text} \n\n"
        "Constraints:\n"
        "- Do NOT hallucinate symptoms not listed in the JSON.\n"
        "- Do NOT diagnose the patient.\n"
        "- Respond ONLY with a professional, 1-sentence acknowledgment of the symptoms."
    )
    
    try:
        chain = prompt | llm
        response = chain.invoke({"text": json.dumps(emr_data)})
        acknowledgement = response.content
    except Exception as e:
        log_agent_execution("TriageAgent", state, error=e)
        acknowledgement = "Acknowledgment unavailable. Proceeding with tool-derived clinical data."
        errors.append("TriageAgent: LLM acknowledgment failed")
        
    patient_info = emr_data.get("patient_info", {})
    symptoms = emr_data.get("symptoms", [])
    current_medications = emr_data.get("current_medications", [])
    triage_acuity = assess_triage_acuity(patient_info, symptoms, current_medications)
    
    result = {
        "patient_info": patient_info,
        "symptoms": symptoms,
        "triage_acuity": triage_acuity,
        "current_step": "triage_completed",
        "logs": [
            f"Triage Agent extracted patient info and symptoms using EMR Tool.",
            f"Triage Acuity Assessment: Level {triage_acuity['acuity_level']} ({triage_acuity['urgency_label']}) - {triage_acuity['rationale']}",
            f"LLM Acknowledgment: {acknowledgement}"
        ]
    }
    log_agent_execution("TriageAgent", state, result=result)
    return result
