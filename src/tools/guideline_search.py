import os
from typing import List

def search_guidelines(symptoms: List[str]) -> str:
    """
    STUDENT 2 TOOL: Scans local medical guidelines based on a list of patient symptoms.
    
    Args:
        symptoms (List[str]): Extracted patient symptoms from the triage stage.
        
    Returns:
        str: The raw text of the recommended medical protocol.
        
    Raises:
        TypeError: If symptoms provided are not in list format.
    """
    if not isinstance(symptoms, list):
        raise TypeError(f"Expected a list of symptoms, got {type(symptoms).__name__}")
        
    print(f"[*] Tool: Searching guidelines for symptoms: {symptoms}")
    symptoms_str = " ".join(str(s).lower() for s in symptoms)
    
    try:
        # Mock offline directory search logic
        if "blood pressure" in symptoms_str or "headache" in symptoms_str:
            return "Hypertension Protocol: Monitor closely. Avoid NSAIDs (like Ibuprofen) as they can elevate blood pressure."
        elif "dizziness" in symptoms_str:
            return "Dizziness Protocol: Check for dehydration or hypertensive crisis."
            
        return "Standard Care Protocol: Proceed with normal observations."
    except Exception as e:
        print(f"[!] Error during guideline search: {str(e)}")
        return "Standard Care Protocol: Proceed with caution due to system degradation."
