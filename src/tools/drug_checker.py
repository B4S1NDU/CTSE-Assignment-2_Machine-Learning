import sqlite3
from typing import List

from src.logger import log_tool_call

def init_drug_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE interactions (medication TEXT, condition TEXT, warning TEXT)")
    c.execute("INSERT INTO interactions VALUES ('ibuprofen', 'hypertension', 'EXTREME WARNING: Ibuprofen is known to exacerbate Hypertension.')")
    c.execute("INSERT INTO interactions VALUES ('aspirin', 'peptic ulcer', 'WARNING: Aspirin increases risk of gastrointestinal bleeding.')")
    conn.commit()
    return conn

_drug_db_conn = init_drug_db()

def _normalize_condition(condition: str) -> str:
    """Normalize diagnosis variants to canonical DB conditions."""
    normalized = condition.strip().lower()
    condition_aliases = {
        "high blood pressure": "hypertension",
        "hypertensive crisis": "hypertension",
    }
    return condition_aliases.get(normalized, normalized)

def check_drug_interactions(diagnoses: List[str], current_medications: List[str]) -> List[str]:
    """
    Queries a local mock drug database for severe contraindications based on proposed
    diagnoses and current medications.
    
    Args:
        diagnoses: Proposed differential diagnoses from the Medical Researcher.
        current_medications: List of current prescribed drugs.
        
    Returns:
        List[str]: A list of critical warning messages to warn the healthcare provider,
            or a message indicating no severe interactions were found.
        
    Raises:
        ValueError: If diagnoses or current_medications are missing or invalid format.
    """
    try:
        if not isinstance(diagnoses, list) or not isinstance(current_medications, list):
            raise ValueError("Both diagnoses and current medications must be lists of strings.")
            
        interactions: List[str] = []
        
        meds_lower = [str(m).lower() for m in current_medications if m]
        
        c = _drug_db_conn.cursor()
        for med in meds_lower:
            for diag in diagnoses:
                diag_lower = _normalize_condition(str(diag))
                c.execute("SELECT warning FROM interactions WHERE medication = ? AND condition = ?", (med, diag_lower))
                rows = c.fetchall()
                for row in rows:
                    if row[0] not in interactions:
                        interactions.append(row[0])
                
        if not interactions:
            interactions.append("No known severe interactions found in local database.")
            
        log_tool_call("check_drug_interactions", (diagnoses, current_medications), {}, result=interactions)
        return interactions
    except Exception as e:
        log_tool_call("check_drug_interactions", (diagnoses, current_medications), {}, error=e)
        return [f"SYSTEM WARNING: Drug database query failed. Do not prescribe ({str(e)})"]
