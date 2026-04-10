from typing import List
import json

def check_drug_interactions(diagnoses: List[str], current_medications: List[str]) -> List[str]:
    """
    STUDENT 3 TOOL: Queries a local mock drug database for severe contraindications.
    
    Args:
        diagnoses (List[str]): Proposed differential diagnoses from Medical Researcher.
        current_medications (List[str]): List of current prescribed drugs.
        
    Returns:
        List[str]: A list of critical warning messages to warn the human doctor.
        
    Raises:
        ValueError: If diagnoses or current_medications are missing or invalid format.
    """
    if not isinstance(diagnoses, list) or not isinstance(current_medications, list):
        raise ValueError("Both diagnoses and current medications must be lists of strings.")
        
    print(f"[*] Tool: Checking interactions for {current_medications} given diagnoses {diagnoses}")
    
    interactions = []
    
    try:
        meds_lower = [str(m).lower() for m in current_medications if m]
        diags_lower = [str(d).lower() for d in diagnoses if d]
        
        # Mock offline database check resolving severe side effects
        if "ibuprofen" in meds_lower and any("hypertension" in d for d in diags_lower):
            interactions.append("EXTREME WARNING: Ibuprofen is known to exacerbate Hypertension.")
            
        if not interactions:
            interactions.append("No known severe interactions found in local database.")
            
        return interactions
    except Exception as e:
        return [f"SYSTEM WARNING: Drug database query failed. Do not prescribe ({str(e)})"]
