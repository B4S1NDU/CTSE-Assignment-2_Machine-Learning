from src.state import PatientState
from src.tools.emr_reader import read_emr
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm
import json
import logging

def triage_node(state: PatientState):
    """
    STUDENT 1 AGENT: Triage Specialist
    """
    logger = logging.getLogger("TriageAgent")
    print("--- [Agent 1] TRIAGE SPECIALIST ---")
    logger.info(f"Triage Node Triggered. Input state tracking: {state.get('raw_emr_path', 'Unknown')}")
    
    # Use Tool
    emr_data = read_emr(state["raw_emr_path"])
    
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
        print(f"LLM execution failed: {e}")
        acknowledgement = "Error: LLM failed to process EMR data."
        
    patient_info = emr_data.get("patient_info", {})
    symptoms = emr_data.get("symptoms", [])
    
    return {
        "patient_info": patient_info,
        "symptoms": symptoms,
        "current_step": "triage_completed",
        "logs": [f"Triage Agent extracted patient info and symptoms using EMR Tool.", f"LLM Acknowledgment: {acknowledgement}"]
    }
