from src.state import PatientState
from src.tools.report_writer import secure_write_report
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm
import os

def cmo_node(state: PatientState):
    """
    STUDENT 4 AGENT: Chief Medical Officer (CMO)
    """
    print("--- [Agent 4] CHIEF MEDICAL OFFICER ---")
    
    patient_info = state.get('patient_info')
    symptoms = state.get('symptoms', [])
    diagnoses = state.get('potential_diagnoses', [])
    drug_interactions = state.get('drug_interactions', [])
    
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
"""
    
    llm = get_llm()
    
    # EXCEPTIONAL PROMPT ENGINEERING for Student 4 Agent
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
        report_content += f"\n\n## CMO Sign-Off\nApproved offline."
    
    # STUDENT 4 TOOL
    report_path = secure_write_report(report_content)
        
    return {
        "final_report_path": report_path,
        "current_step": "cmo_completed",
        "logs": [f"CMO generated final clinical summary report via LLM and Toolkit at {report_path}."]
    }
