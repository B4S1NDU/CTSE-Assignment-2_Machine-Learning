import pytest
import os
from src.tools.emr_reader import read_emr
from src.tools.drug_checker import check_drug_interactions
from src.tools.guideline_search import search_guidelines
from src.tools.report_writer import secure_write_report

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
    
    # Test safe
    safe_interactions = check_drug_interactions(["Healthy"], ["Vitamin C"])
    assert "No known severe interactions" in safe_interactions[0]

# STUDENT 4 TEST (CMO / Report Writer Tool)
def test_report_writer_tool():
    """Validating Student 4 tool correctly securely writes files to the local disk."""
    dummy_text = "CMO Final Sign Off."
    filepath = secure_write_report(dummy_text)
    
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        content = f.read()
    assert dummy_text in content
    
    # Cleanup mock test file
    os.remove(filepath)
