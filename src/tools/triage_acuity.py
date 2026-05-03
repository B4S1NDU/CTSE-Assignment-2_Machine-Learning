import sqlite3
from typing import Any, Dict, List, Sequence, Tuple

from src.logger import log_tool_call


def _create_triage_connection() -> sqlite3.Connection:
    """
    Create and seed an in-memory SQLite database for triage evidence lookup.

    Returns:
        sqlite3.Connection: Seeded SQLite connection containing triage rules.
    """
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE symptom_rules (
            keyword TEXT NOT NULL,
            acuity_level INTEGER NOT NULL,
            score INTEGER NOT NULL,
            urgency_label TEXT NOT NULL,
            rationale TEXT NOT NULL,
            is_red_flag INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE history_rules (
            keyword TEXT NOT NULL,
            score INTEGER NOT NULL,
            rationale TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE age_rules (
            min_age INTEGER NOT NULL,
            score INTEGER NOT NULL,
            rationale TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE medication_rules (
            keyword TEXT NOT NULL,
            score INTEGER NOT NULL,
            rationale TEXT NOT NULL
        )
        """
    )

    symptom_rows = [
        ("chest pain", 1, 100, "emergency", "Chest pain is a red-flag symptom requiring immediate assessment.", 1),
        ("shortness of breath", 1, 100, "emergency", "Breathing difficulty is a red-flag symptom requiring immediate assessment.", 1),
        ("breathing difficulty", 1, 100, "emergency", "Breathing difficulty is a red-flag symptom requiring immediate assessment.", 1),
        ("fainting", 1, 100, "emergency", "Fainting suggests possible acute instability and needs immediate review.", 1),
        ("unconscious", 1, 100, "emergency", "Unconsciousness requires immediate escalation.", 1),
        ("confusion", 1, 100, "emergency", "New confusion is a red-flag presentation requiring urgent care.", 1),
        ("seizure", 1, 100, "emergency", "Seizure activity requires immediate clinical review.", 1),
        ("stroke", 1, 100, "emergency", "Stroke-like symptoms require immediate escalation.", 1),
        ("weakness on one side", 1, 100, "emergency", "Unilateral weakness is a stroke red flag.", 1),
        ("high blood pressure", 2, 32, "urgent", "High blood pressure needs prompt evaluation when paired with symptoms.", 0),
        ("severe headache", 2, 28, "urgent", "Severe headache can signal a more serious acute condition.", 0),
        ("dizziness", 2, 20, "urgent", "Dizziness can indicate an acute issue when combined with other findings.", 0),
        ("vomiting", 3, 16, "moderate", "Vomiting increases triage concern but is not automatically emergent.", 0),
        ("fever", 3, 15, "moderate", "Fever can raise acuity depending on context.", 0),
        ("severe pain", 2, 22, "urgent", "Severe pain may require earlier review depending on the overall picture.", 0),
        ("worsening", 3, 10, "moderate", "Worsening symptoms increase concern and should be monitored.", 0),
    ]
    cursor.executemany(
        "INSERT INTO symptom_rules VALUES (?, ?, ?, ?, ?, ?)",
        symptom_rows,
    )

    history_rows = [
        ("smoker", 10, "Smoking history increases clinical risk."),
        ("hypertension", 12, "Known hypertension increases clinical risk."),
        ("diabetes", 12, "Diabetes increases clinical risk."),
        ("heart disease", 14, "Cardiac history increases clinical risk."),
    ]
    cursor.executemany("INSERT INTO history_rules VALUES (?, ?, ?)", history_rows)

    age_rows = [
        (65, 14, "Older age increases the caution threshold."),
        (75, 18, "Advanced age increases triage concern."),
    ]
    cursor.executemany("INSERT INTO age_rules VALUES (?, ?, ?)", age_rows)

    medication_rows = [
        ("ibuprofen", 12, "Ibuprofen may worsen blood pressure concerns."),
        ("nsaid", 10, "NSAID use can be relevant in blood pressure concerns."),
    ]
    cursor.executemany("INSERT INTO medication_rules VALUES (?, ?, ?)", medication_rows)

    connection.commit()
    return connection


def _contains_keyword(text: str, keyword: str) -> bool:
    """
    Determine whether a keyword appears in free text.

    Args:
        text: Normalized free-text input.
        keyword: Keyword to search for.

    Returns:
        bool: True when the keyword appears in the text.
    """
    return keyword in text


def _lookup_symptom_rules(connection: sqlite3.Connection, symptoms: Sequence[str]) -> List[Dict[str, Any]]:
    """
    Query symptom rules for each symptom string.

    Args:
        connection: SQLite connection containing the rules.
        symptoms: Normalized symptom strings.

    Returns:
        List[Dict[str, Any]]: Matched symptom rule rows.
    """
    cursor = connection.cursor()
    matches: List[Dict[str, Any]] = []
    for symptom in symptoms:
        cursor.execute("SELECT keyword, acuity_level, score, urgency_label, rationale, is_red_flag FROM symptom_rules")
        for keyword, acuity_level, score, urgency_label, rationale, is_red_flag in cursor.fetchall():
            if _contains_keyword(symptom, keyword):
                matches.append(
                    {
                        "rule_type": "symptom",
                        "keyword": keyword,
                        "acuity_level": acuity_level,
                        "score": score,
                        "urgency_label": urgency_label,
                        "rationale": rationale,
                        "is_red_flag": bool(is_red_flag),
                    }
                )
    return matches


def _lookup_history_rules(connection: sqlite3.Connection, history_text: str) -> List[Dict[str, Any]]:
    """
    Query history-based triage rules.

    Args:
        connection: SQLite connection containing the rules.
        history_text: Normalized patient history text.

    Returns:
        List[Dict[str, Any]]: Matched history rule rows.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT keyword, score, rationale FROM history_rules")
    rows = cursor.fetchall()
    matches: List[Dict[str, Any]] = []
    for keyword, score, rationale in rows:
        if _contains_keyword(history_text, keyword):
            matches.append(
                {
                    "rule_type": "history",
                    "keyword": keyword,
                    "score": score,
                    "rationale": rationale,
                }
            )
    return matches


def _lookup_age_rules(connection: sqlite3.Connection, age: Any) -> List[Dict[str, Any]]:
    """
    Query age-based triage rules.

    Args:
        connection: SQLite connection containing the rules.
        age: Patient age from the EMR.

    Returns:
        List[Dict[str, Any]]: Matched age rule rows.
    """
    if not isinstance(age, (int, float)):
        return []

    cursor = connection.cursor()
    cursor.execute("SELECT min_age, score, rationale FROM age_rules WHERE min_age <= ? ORDER BY min_age DESC", (age,))
    rows = cursor.fetchall()
    matches: List[Dict[str, Any]] = []
    for min_age, score, rationale in rows:
        matches.append(
            {
                "rule_type": "age",
                "keyword": f"age>={min_age}",
                "score": score,
                "rationale": rationale,
            }
        )
    return matches


def _lookup_medication_rules(connection: sqlite3.Connection, medications: Sequence[str]) -> List[Dict[str, Any]]:
    """
    Query medication-based triage rules.

    Args:
        connection: SQLite connection containing the rules.
        medications: Normalized medication strings.

    Returns:
        List[Dict[str, Any]]: Matched medication rule rows.
    """
    cursor = connection.cursor()
    cursor.execute("SELECT keyword, score, rationale FROM medication_rules")
    rows = cursor.fetchall()
    matches: List[Dict[str, Any]] = []
    for medication in medications:
        for keyword, score, rationale in rows:
            if _contains_keyword(medication, keyword):
                matches.append(
                    {
                        "rule_type": "medication",
                        "keyword": keyword,
                        "score": score,
                        "rationale": rationale,
                    }
                )
    return matches


def _determine_level(total_score: int, has_red_flag: bool) -> Tuple[int, str, bool]:
    """
    Convert the accumulated score into an acuity level.

    Args:
        total_score: Aggregated score from the evidence rules.
        has_red_flag: Whether any emergency red flag was matched.

    Returns:
        Tuple[int, str, bool]: (acuity_level, urgency_label, needs_immediate_review)
    """
    if has_red_flag:
        return 1, "emergency", True
    if total_score >= 60:
        return 2, "urgent", True
    if total_score >= 25:
        return 3, "moderate", False
    if total_score >= 10:
        return 4, "low", False
    return 5, "minor", False


def assess_triage_acuity(
    patient_info: Dict[str, Any],
    symptoms: List[str],
    current_medications: List[str] | None = None,
) -> Dict[str, Any]:
    """
    Assess triage acuity using a local SQLite evidence lookup and score aggregation.

    Args:
        patient_info: Structured patient details extracted from the EMR.
        symptoms: Symptom list extracted from the EMR.
        current_medications: Optional medication list from the EMR.

    Returns:
        A dictionary containing acuity level, urgency label, matched rules, red flags,
        total score, rationale, and whether immediate review is needed.

    Raises:
        TypeError: If the provided inputs are not of the expected types.
    """
    try:
        if not isinstance(patient_info, dict):
            raise TypeError(f"Expected patient_info to be a dict, got {type(patient_info).__name__}")
        if not isinstance(symptoms, list):
            raise TypeError(f"Expected symptoms to be a list, got {type(symptoms).__name__}")
        if current_medications is not None and not isinstance(current_medications, list):
            raise TypeError(
                f"Expected current_medications to be a list or None, got {type(current_medications).__name__}"
            )

        normalized_symptoms = [str(symptom).lower() for symptom in symptoms]
        normalized_history = str(patient_info.get("history", "")).lower()
        normalized_medications = [str(medication).lower() for medication in (current_medications or [])]
        age = patient_info.get("age")

        connection = _create_triage_connection()
        symptom_matches = _lookup_symptom_rules(connection, normalized_symptoms)
        history_matches = _lookup_history_rules(connection, normalized_history)
        age_matches = _lookup_age_rules(connection, age)
        medication_matches = _lookup_medication_rules(connection, normalized_medications)

        matched_rules = symptom_matches + history_matches + age_matches + medication_matches
        red_flags = [match["keyword"] for match in symptom_matches if match.get("is_red_flag")]
        total_score = sum(int(match["score"]) for match in matched_rules)
        has_red_flag = any(match.get("is_red_flag") for match in symptom_matches)

        acuity_level, urgency_label, needs_immediate_review = _determine_level(total_score, has_red_flag)

        if matched_rules:
            top_rationales = [match["rationale"] for match in matched_rules[:3]]
            rationale = "; ".join(top_rationales)
        else:
            rationale = "No matching triage evidence was found in the local database."

        result = {
            "acuity_level": acuity_level,
            "urgency_label": urgency_label,
            "red_flags": list(dict.fromkeys(red_flags)),
            "matched_rules": matched_rules,
            "total_score": total_score,
            "needs_immediate_review": needs_immediate_review,
            "rationale": rationale,
        }
        log_tool_call("assess_triage_acuity", (patient_info, symptoms, current_medications), {}, result=result)
        connection.close()
        return result
    except Exception as e:
        error_result = {
            "acuity_level": 3,
            "urgency_label": "moderate",
            "red_flags": [],
            "matched_rules": [],
            "total_score": 0,
            "needs_immediate_review": False,
            "rationale": f"Acuity assessment fallback used because the tool failed: {str(e)}",
        }
        log_tool_call("assess_triage_acuity", (patient_info, symptoms, current_medications), {}, error=e)
        return error_result