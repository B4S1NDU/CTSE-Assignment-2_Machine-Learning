import os
import urllib.error
import urllib.request

import pytest

from src.graph import build_graph


def _ollama_available() -> bool:
    """Return True when local Ollama API is reachable."""
    try:
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, OSError):
        return False


@pytest.mark.integration
def test_end_to_end_pipeline_generates_clean_report():
    """
    End-to-end assertion for a clean MAS run.
    Skips if Ollama is not running locally.
    """
    if not _ollama_available():
        pytest.skip("Ollama is not running on localhost:11434")

    app = build_graph()
    initial_state = {
        "raw_emr_path": "data/mock_patient.json",
        "patient_info": {},
        "symptoms": [],
        "potential_diagnoses": [],
        "drug_interactions": [],
        "final_report_path": "",
        "current_step": "start",
        "logs": ["System initialized"],
    }

    final_state = app.invoke(initial_state)

    diagnoses = ", ".join(final_state.get("potential_diagnoses", []))
    assert "Error:" not in diagnoses

    report_path = final_state.get("final_report_path", "")
    assert report_path and os.path.exists(report_path)

    with open(report_path, "r", encoding="utf-8") as report_file:
        report_content = report_file.read()

    assert "Approved offline. Error" not in report_content
    assert "## Patient Info" in report_content
    assert "## Symptoms" in report_content
    assert "## Potential Diagnoses" in report_content
    assert "## CMO Sign-Off" in report_content
    assert "Error:" not in report_content
