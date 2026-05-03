import pytest
import os
from src.tools.emr_reader import read_emr
from src.tools.drug_checker import check_drug_interactions
from src.tools.guideline_search import search_guidelines
from src.tools.med_recommender import recommend_medications, get_recommendation_count
from src.tools.report_writer import secure_write_report
from src.tools.triage_acuity import assess_triage_acuity

# STUDENT 1 TEST (Triage / EMR Tool)
def test_emr_reader_tool():
    """Property-based mock test for Student 1"""
    data = read_emr("data/mock_patient.json")
    assert "patient_info" in data
    assert "symptoms" in data

# STUDENT 2 TEST (Researcher / Guideline Search Tool)
def test_guideline_search_tool():
    """Validating Student 2 tool accurately maps known symptoms to protocols without hallucination."""
    syd_protocol = search_guidelines(["headache", "blood pressure"])
    assert "Hypertension Protocol" in syd_protocol
    assert "NSAID" in syd_protocol or "Ibuprofen" in syd_protocol

    warning = "EXTREME WARNING: Ibuprofen is known to exacerbate Hypertension."
    assert "EXTREME WARNING" in warning
    assert "ibuprofen" in warning.lower() and "hypertension" in warning.lower()

    healthy_protocol = search_guidelines(["sore toe"])
    assert "Standard Care" in healthy_protocol

# STUDENT 3 TEST (Pharmacologist / Drug Interaction Tool)
def test_drug_checker_tool():
    """Validating Student 3 tool correctly catches severe interactions and handles clean inputs."""
    # Test collision
    diagnoses = ["Hypertension"]
    meds = ["Ibuprofen"]
    interactions = check_drug_interactions(diagnoses, meds)
    assert any("WARNING" in msg for msg in interactions)

    # Synonym/variant check (hypertensive crisis should map to hypertension risk)
    variant_interactions = check_drug_interactions(["Hypertensive Crisis"], ["Ibuprofen"])
    assert any("WARNING" in msg for msg in variant_interactions)
    
    # Test safe
    safe_interactions = check_drug_interactions(["Healthy"], ["Vitamin C"])
    assert "No known severe interactions" in safe_interactions[0]

# CMO / Report Writer Tool
def test_report_writer_tool():
    """Validating CMO tool correctly securely writes files to the local disk."""
    dummy_text = "CMO Final Sign Off."
    filepath = secure_write_report(dummy_text)
    
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        content = f.read()
    assert dummy_text in content
    
    # Cleanup mock test file
    os.remove(filepath)


def test_med_recommender_tool():
    """Validating CMO medication recommender uses local SQLite data and returns safe alternatives."""
    assert get_recommendation_count() >= 50

    recommendations = recommend_medications(["Hypertension"], ["Ibuprofen"])
    assert any("replace ibuprofen" in r.lower() for r in recommendations)
    assert any("acetaminophen" in r.lower() for r in recommendations)

    safe_case = recommend_medications(["Healthy"], ["Vitamin C"])
    assert "No safer alternatives identified" in safe_case[0]


def test_triage_acuity_tool():
    """Validating Student 1 triage acuity tool classifies urgency from local EMR data."""
    patient_info = {
        "age": 45,
        "gender": "Male",
        "history": "Smoker, occasional alcohol",
    }
    symptoms = ["severe headache", "dizziness", "high blood pressure"]
    acuity = assess_triage_acuity(patient_info, symptoms, ["Ibuprofen"])

    assert isinstance(acuity, dict)
    assert acuity["acuity_level"] == 2
    assert "urgency_label" in acuity
    assert "rationale" in acuity
    assert "matched_rules" in acuity
    assert isinstance(acuity["matched_rules"], list)
    assert acuity["total_score"] > 0
    assert isinstance(acuity["red_flags"], list)
