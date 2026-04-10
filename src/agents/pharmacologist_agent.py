from src.state import PatientState
from src.tools.drug_checker import check_drug_interactions
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm

def pharmacologist_node(state: PatientState):
    """
    STUDENT 3 AGENT: Pharmacologist
    """
    print("--- [Agent 3] PHARMACOLOGIST ---")
    
    diagnoses = state.get("potential_diagnoses", [])
    meds = state.get("patient_info", {}).get("current_medications", ["Ibuprofen"])
    
    interactions = check_drug_interactions(diagnoses, meds)
    
    llm = get_llm()
    
    # EXCEPTIONAL PROMPT ENGINEERING for Student 3 Agent
    prompt = PromptTemplate.from_template(
        "You are a strict, risk-averse Clinical Pharmacologist with deep focus on patient safety. "
        "Review these system warnings derived from offline databases: {warnings}\n\n"
        "Your task:\n"
        "- Synthesize the warnings into a single, definitive pharmacological safety assessment.\n"
        "- Do NOT sugarcoat or minimize severe risks (e.g., Hypertension + Ibuprofen).\n"
        "- Max length: 1 strict sentence."
    )
    
    try:
        chain = prompt | llm
        assessment = chain.invoke({"warnings": interactions})
        final_interactions = interactions + [f"Pharmacologist Assessment: {assessment.content}"]
    except Exception as e:
        final_interactions = interactions + ["Pharmacologist Assessment: Review tool output carefully."]
        
    return {
        "drug_interactions": final_interactions,
        "current_step": "pharmacology_completed",
        "logs": ["Pharmacologist Agent queried Database and rendered safety assessment."]
    }
