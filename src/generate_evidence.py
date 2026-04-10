import os
import shutil
from datetime import datetime

from src.graph import build_graph


def _has_error_markers(final_state: dict, report_content: str) -> bool:
    """Detect fallback/error content in final state and report."""
    diagnoses = ", ".join(final_state.get("potential_diagnoses", []))
    return (
        "Error:" in diagnoses
        or "Error:" in report_content
        or "Approved offline. Error" in report_content
    )


def generate_evidence() -> tuple[str, str]:
    """
    Run the pipeline and save a clean evidence report + evidence log.

    Returns:
        tuple[str, str]: (evidence_report_path, evidence_log_path)

    Raises:
        RuntimeError: If run produced fallback/error output.
        FileNotFoundError: If generated report or log is missing.
    """
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
    report_path = final_state.get("final_report_path", "")
    if not report_path or not os.path.exists(report_path):
        raise FileNotFoundError("Pipeline did not generate a report file.")

    with open(report_path, "r", encoding="utf-8") as report_file:
        report_content = report_file.read()

    if _has_error_markers(final_state, report_content):
        raise RuntimeError(
            "Run completed with fallback/error content. Start Ollama and rerun for clean evidence."
        )

    log_path = "logs/agent_execution.log"
    if not os.path.exists(log_path):
        raise FileNotFoundError("Expected log file was not found at logs/agent_execution.log.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    evidence_report_path = f"reports/evidence_report_{timestamp}.md"
    evidence_log_path = f"logs/evidence_log_{timestamp}.log"

    shutil.copy2(report_path, evidence_report_path)
    shutil.copy2(log_path, evidence_log_path)
    return evidence_report_path, evidence_log_path


if __name__ == "__main__":
    report, log = generate_evidence()
    print(f"Evidence report saved: {report}")
    print(f"Evidence log saved: {log}")
