from typing import List
import sqlite3

def init_drug_db():
    conn = sqlite3.connect(":memory:")
    c = conn.cursor()
    c.execute("CREATE TABLE interactions (medication TEXT, condition TEXT, warning TEXT)")
    c.execute("INSERT INTO interactions VALUES ('ibuprofen', 'hypertension', 'EXTREME WARNING: Ibuprofen is known to exacerbate Hypertension.')")
    c.execute("INSERT INTO interactions VALUES ('aspirin', 'peptic ulcer', 'WARNING: Aspirin increases risk of gastrointestinal bleeding.')")
    conn.commit()
    return conn

_drug_db_conn = init_drug_db()

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
        diags_lower = [str(d).lower for d in diagnoses if d]
        
        c = _drug_db_conn.cursor()
        for med in meds_lower:
            for diag in diagnoses:
                diag_lower = str(diag).lower()
                c.execute("SELECT warning FROM interactions WHERE medication = ? AND condition = ?", (med, diag_lower))
                rows = c.fetchall()
                for row in rows:
                    interactions.append(row[0])
            
        if not interactions:
            interactions.append("No known severe interactions found in local database.")
            
        return interactions
    except Exception as e:
        return [f"SYSTEM WARNING: Drug database query failed. Do not prescribe ({str(e)})"]
