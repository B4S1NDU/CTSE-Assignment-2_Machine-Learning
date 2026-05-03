import os
import sqlite3
from typing import List, Tuple

from src.logger import log_tool_call


def _seed_recommendations() -> List[Tuple[str, str, str, str, int]]:
    return [
        ("hypertension", "ibuprofen", "acetaminophen", "Less blood-pressure impact than NSAIDs.", 1),
        ("hypertension", "ibuprofen", "topical diclofenac gel", "Topical route reduces systemic BP effects.", 2),
        ("hypertension", "ibuprofen", "naproxen low-dose short-course", "Use only when essential with BP monitoring.", 3),
        ("hypertension", "naproxen", "acetaminophen", "Preferred first-line analgesic in hypertension.", 1),
        ("hypertension", "diclofenac", "acetaminophen", "Avoid fluid retention risk from systemic NSAIDs.", 1),
        ("hypertension", "pseudoephedrine", "saline nasal spray", "Avoid sympathomimetic BP elevation.", 1),
        ("hypertension", "pseudoephedrine", "loratadine", "Non-decongestant antihistamine option.", 2),
        ("hypertension", "etoricoxib", "acetaminophen", "COX-2 agents can worsen BP control.", 1),
        ("hypertension", "celecoxib", "acetaminophen", "Prefer non-NSAID pain management.", 1),
        ("hypertension", "indomethacin", "acetaminophen", "Indomethacin can increase BP significantly.", 1),
        ("peptic ulcer", "aspirin", "clopidogrel", "Lower GI irritation risk in aspirin-intolerant patients.", 1),
        ("peptic ulcer", "aspirin", "acetaminophen", "Avoid ulcer bleed risk from aspirin.", 2),
        ("peptic ulcer", "ibuprofen", "acetaminophen", "NSAID ulcerogenic risk avoided.", 1),
        ("peptic ulcer", "naproxen", "acetaminophen", "Prefer non-NSAID analgesics.", 1),
        ("peptic ulcer", "diclofenac", "acetaminophen", "GI mucosal injury risk reduced.", 1),
        ("peptic ulcer", "ketorolac", "acetaminophen", "Ketorolac has high GI bleeding risk.", 1),
        ("peptic ulcer", "prednisone", "budesonide", "Lower systemic GI risk profile.", 2),
        ("peptic ulcer", "dexketoprofen", "acetaminophen", "Avoid potent NSAIDs in active ulcer disease.", 1),
        ("peptic ulcer", "piroxicam", "acetaminophen", "High GI toxicity NSAID substitution.", 1),
        ("peptic ulcer", "meloxicam", "acetaminophen", "Lower ulcer rebleed risk with non-NSAID.", 1),
        ("chronic kidney disease", "ibuprofen", "acetaminophen", "Avoid NSAID nephrotoxicity.", 1),
        ("chronic kidney disease", "naproxen", "acetaminophen", "Reduced renal perfusion risk.", 1),
        ("chronic kidney disease", "diclofenac", "acetaminophen", "NSAID alternatives preferred in CKD.", 1),
        ("chronic kidney disease", "metformin", "linagliptin", "Use renal-safe glucose-lowering alternative when needed.", 2),
        ("chronic kidney disease", "gentamicin", "ceftriaxone", "Avoid aminoglycoside nephrotoxicity where possible.", 1),
        ("chronic kidney disease", "spironolactone", "furosemide", "Hyperkalemia risk mitigation in CKD.", 2),
        ("chronic kidney disease", "enalapril", "amlodipine", "Alternative if ACEi intolerance or renal decline.", 3),
        ("chronic kidney disease", "allopurinol", "febuxostat low-dose", "Dose-adjusted urate control option.", 3),
        ("chronic kidney disease", "ranitidine", "famotidine", "Renal-dosed H2 blocker alternative.", 3),
        ("chronic kidney disease", "trimethoprim", "amoxicillin", "Avoid potassium rise and creatinine effects.", 2),
        ("asthma", "aspirin", "acetaminophen", "Avoid aspirin-exacerbated respiratory disease trigger.", 1),
        ("asthma", "ibuprofen", "acetaminophen", "Lower risk of bronchospasm than NSAIDs.", 1),
        ("asthma", "naproxen", "acetaminophen", "NSAIDs may trigger bronchoconstriction.", 1),
        ("asthma", "propranolol", "metoprolol", "Cardioselective beta-blocker if beta-blockade required.", 2),
        ("asthma", "timolol", "brimonidine", "Avoid non-selective beta blocker exposure.", 1),
        ("asthma", "codeine", "dextromethorphan", "Less histamine-release concern.", 3),
        ("asthma", "morphine", "fentanyl", "Lower histamine-mediated bronchospasm potential.", 3),
        ("asthma", "carvedilol", "nebivolol", "Prefer more beta-1 selective options.", 3),
        ("asthma", "sotalol", "diltiazem", "Non-beta blocker option for rhythm control context.", 3),
        ("asthma", "labetalol", "amlodipine", "Alternative antihypertensive without beta-blockade.", 3),
        ("pregnancy", "warfarin", "enoxaparin", "Warfarin teratogenic risk avoided.", 1),
        ("pregnancy", "isotretinoin", "azelaic acid", "Teratogenic retinoid substitution.", 1),
        ("pregnancy", "valproate", "lamotrigine", "Lower teratogenic anticonvulsant strategy.", 1),
        ("pregnancy", "lisinopril", "labetalol", "ACE inhibitors contraindicated in pregnancy.", 1),
        ("pregnancy", "losartan", "methyldopa", "ARB contraindication alternative.", 1),
        ("pregnancy", "ibuprofen", "acetaminophen", "Preferred antipyretic/analgesic in pregnancy.", 1),
        ("pregnancy", "doxycycline", "amoxicillin", "Avoid fetal bone/teeth effects.", 1),
        ("pregnancy", "atorvastatin", "bile acid sequestrant", "Statins generally avoided in pregnancy.", 2),
        ("pregnancy", "spironolactone", "eplerenone", "Avoid anti-androgen effects where possible.", 3),
        ("pregnancy", "paroxetine", "sertraline", "Preferred SSRI profile in pregnancy.", 2),
        ("heart failure", "pioglitazone", "empagliflozin", "Avoid fluid retention from TZDs.", 1),
        ("heart failure", "diltiazem", "bisoprolol", "Use HF-supported rate control options.", 2),
        ("heart failure", "verapamil", "bisoprolol", "Non-dihydropyridine CCBs may worsen HF.", 2),
        ("heart failure", "ibuprofen", "acetaminophen", "NSAIDs can trigger fluid retention in HF.", 1),
        ("heart failure", "naproxen", "acetaminophen", "Avoid sodium/water retention worsening HF.", 1),
    ]


def init_recommender_db() -> sqlite3.Connection:
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(root_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, "med_recommender.db")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS recommendations (
            diagnosis TEXT NOT NULL,
            contraindicated_medication TEXT NOT NULL,
            safer_alternative TEXT NOT NULL,
            rationale TEXT NOT NULL,
            priority INTEGER NOT NULL
        )
        """
    )

    c.execute("SELECT COUNT(*) FROM recommendations")
    count = c.fetchone()[0]
    if count < 50:
        c.execute("DELETE FROM recommendations")
        c.executemany(
            "INSERT INTO recommendations (diagnosis, contraindicated_medication, safer_alternative, rationale, priority) VALUES (?, ?, ?, ?, ?)",
            _seed_recommendations(),
        )
        conn.commit()

    return conn


_recommender_db_conn = init_recommender_db()


def _normalize_diagnosis(diagnosis: str) -> str:
    normalized = diagnosis.strip().lower()
    aliases = {
        "high blood pressure": "hypertension",
        "hypertensive crisis": "hypertension",
        "ckd": "chronic kidney disease",
        "renal failure": "chronic kidney disease",
    }
    return aliases.get(normalized, normalized)


def recommend_medications(diagnoses: List[str], current_medications: List[str], top_n: int = 3) -> List[str]:
    try:
        if not isinstance(diagnoses, list) or not isinstance(current_medications, list):
            raise ValueError("Diagnoses and current medications must be lists.")

        recommendations: List[str] = []
        seen = set()
        c = _recommender_db_conn.cursor()

        normalized_diagnoses = [_normalize_diagnosis(str(d)) for d in diagnoses if d]
        medications = [str(m).strip().lower() for m in current_medications if m]

        for diagnosis in normalized_diagnoses:
            for medication in medications:
                c.execute(
                    """
                    SELECT diagnosis, contraindicated_medication, safer_alternative, rationale
                    FROM recommendations
                    WHERE LOWER(diagnosis) = ? AND LOWER(contraindicated_medication) = ?
                    ORDER BY priority ASC
                    LIMIT ?
                    """,
                    (diagnosis, medication, top_n),
                )
                rows = c.fetchall()
                for row in rows:
                    recommendation = f"For {row[0]}, replace {row[1]} with {row[2]} ({row[3]})"
                    if recommendation not in seen:
                        seen.add(recommendation)
                        recommendations.append(recommendation)

        if not recommendations:
            recommendations = ["No safer alternatives identified in local recommendation database."]

        log_tool_call("recommend_medications", (diagnoses, current_medications), {"top_n": top_n}, result=recommendations)
        return recommendations
    except Exception as e:
        log_tool_call("recommend_medications", (diagnoses, current_medications), {"top_n": top_n}, error=e)
        return [f"SYSTEM WARNING: Medication recommendation lookup failed ({str(e)})"]


def get_recommendation_count() -> int:
    c = _recommender_db_conn.cursor()
    c.execute("SELECT COUNT(*) FROM recommendations")
    return int(c.fetchone()[0])
