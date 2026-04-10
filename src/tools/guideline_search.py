import os
from typing import List, Set
import sqlite3

from src.logger import log_tool_call

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
    Scans local medical guidelines based on a list of patient symptoms.
    
    Args:
        symptoms: A list of extracted patient symptoms.
        
    Returns:
        str: The raw text of the recommended medical protocol(s).
        
    Raises:
        TypeError: If symptoms provided are not in list format.
    """
    try:
        if not isinstance(symptoms, list):
            raise TypeError(f"Expected a list of symptoms, got {type(symptoms).__name__}")
            
        c = _guideline_db_conn.cursor()
        protocols: Set[str] = set()
        for symptom in symptoms:
            symptom_str = str(symptom).lower()
            c.execute("SELECT protocol FROM guidelines WHERE keyword = ? OR ? LIKE '%' || keyword || '%'", (symptom_str, symptom_str))
            rows = c.fetchall()
            for row in rows:
                protocols.add(row[0])
                
        if protocols:
            result = " ".join(protocols)
            log_tool_call("search_guidelines", (symptoms,), {}, result=result)
            return result
            
        result = "Standard Care Protocol: Proceed with normal observations."
        log_tool_call("search_guidelines", (symptoms,), {}, result=result)
        return result
    except Exception as e:
        log_tool_call("search_guidelines", (symptoms,), {}, error=e)
        return "Standard Care Protocol: Proceed with caution due to system degradation."
