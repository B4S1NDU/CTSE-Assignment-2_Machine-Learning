import os
from typing import List
import sqlite3

def init_guideline_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE guidelines (keyword TEXT, protocol TEXT)")
    c.execute("INSERT INTO guidelines VALUES ('blood pressure', 'Hypertension Protocol: Monitor closely. Avoid NSAIDs (like Ibuprofen) as they can elevate blood pressure.')")
    c.execute("INSERT INTO guidelines VALUES ('headache', 'Hypertension Protocol: Monitor closely. Avoid NSAIDs (like Ibuprofen) as they can elevate blood pressure.')")
    c.execute("INSERT INTO guidelines VALUES ('dizziness', 'Dizziness Protocol: Check for dehydration or hypertensive crisis.')")
    conn.commit()
    return conn

_guideline_db_conn = init_guideline_db()

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
        c = _guideline_db_conn.cursor()
        protocols = set()
        for symptom in symptoms:
            symptom_str = str(symptom).lower()
            c.execute("SELECT protocol FROM guidelines WHERE keyword = ? OR ? LIKE '%' || keyword || '%'", (symptom_str, symptom_str))
            rows = c.fetchall()
            for row in rows:
                protocols.add(row[0])
                
        if protocols:
            return " ".join(protocols)
            
        return "Standard Care Protocol: Proceed with normal observations."
    except Exception as e:
        print(f"[!] Error during guideline search: {str(e)}")
        return "Standard Care Protocol: Proceed with caution due to system degradation."
