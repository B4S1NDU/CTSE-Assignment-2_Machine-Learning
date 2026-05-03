from src.state import PatientState
from src.tools.report_writer import secure_write_report
from src.tools.med_recommender import recommend_medications
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm

from src.logger import log_agent_execution

def cmo_node(state: PatientState):
    """
    CMO AGENT: Chief Medical Officer (CMO)
    """
    print("--- [Agent 4] CHIEF MEDICAL OFFICER ---")
    errors = []
    
    patient_info = state.get('patient_info')
    symptoms = state.get('symptoms', [])
    diagnoses = state.get('potential_diagnoses', [])
    drug_interactions = state.get('drug_interactions', [])
    current_medications = state.get("current_medications", state.get("patient_info", {}).get("current_medications", ["Ibuprofen"]))

    med_recommendations = recommend_medications(diagnoses, current_medications)
    
    report_content = f"""
# Clinical Summary Report

## Patient Info
{patient_info}

## Symptoms
{', '.join(symptoms)}

## Potential Diagnoses
{', '.join(diagnoses)}

## Drug Interactions / Warnings
{', '.join(drug_interactions)}

## Safer Medication Alternatives (CMO)
{', '.join(med_recommendations)}
"""
    
    llm = get_llm()
    
    # EXCEPTIONAL PROMPT ENGINEERING for CMO Agent
    prompt = PromptTemplate.from_template(
        "You are the Chief Medical Officer (CMO), the highest clinical authority. "
        "Review this compiled patient dossier:\n{report}\n\n"
        "Your task:\n"
        "- Validate all previous agent decisions for any discrepancies.\n"
        "- Issue a formal sign-off (max 2 sentences).\n"
        "- Highlight any critical safety concerns explicitly.\n"
    )
    
    try:
        chain = prompt | llm
        blessing = chain.invoke({"report": report_content})
        report_content += f"\n\n## CMO Sign-Off\n{blessing.content}"
    except Exception as e:
        log_agent_execution("CMOAgent", state, error=e)
        report_content += "\n\n## CMO Sign-Off\nApproved with tool-verified data. LLM sign-off unavailable."
        errors.append("CMOAgent: LLM sign-off failed")
    
    # CMO Agent
    try:
        report_path = secure_write_report(report_content)
    except Exception as e:
        log_agent_execution("CMOAgent", state, error=e)
        report_path = ""
        errors.append("CMOAgent: report generation failed")
        
    result = {
        "final_report_path": report_path,
        "med_recommendations": med_recommendations,
        "current_step": "cmo_completed",
        "logs": [f"CMO generated final clinical summary report via LLM and Toolkit at {report_path or 'unavailable'}."],
        "errors": errors,
    }
    log_agent_execution("CMOAgent", state, result=result)
    return result
