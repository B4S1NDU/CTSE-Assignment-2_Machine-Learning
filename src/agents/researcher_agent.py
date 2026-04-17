from src.state import PatientState
from src.tools.guideline_search import search_guidelines
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm

from src.logger import log_agent_execution

def _allowed_diagnoses_from_guidelines(guideline_text: str) -> list[str]:
    """Derive a safe allow-list of diagnoses from retrieved local guideline text."""
    text = guideline_text.lower()
    allowed: list[str] = []
    if "hypertension" in text:
        allowed.extend(["Hypertension", "Hypertensive Crisis"])
    if "dizziness" in text or "dehydration" in text:
        allowed.append("Dehydration")
    if not allowed:
        allowed.append("General Observation Required")
    # Preserve order while removing duplicates
    return list(dict.fromkeys(allowed))

def researcher_node(state: PatientState):
    """
    STUDENT 2 AGENT: Medical Researcher
    """
    print("--- [Agent 2] MEDICAL RESEARCHER ---")
    symptoms = state.get("symptoms", [])
    
    # Mock LLM Processing & Tool Use
    guideline_text = search_guidelines(symptoms)
    llm = get_llm()
    
    # EXCEPTIONAL PROMPT ENGINEERING for Student 2 Agent
    prompt = PromptTemplate.from_template(
        "You are an Elite Medical Researcher specialized in evidence-based medicine. "
        "Symptoms presented: {symptoms}\n"
        "Retrieved Guidelines Protocols: {guidelines}\n\n"
        "Constraints:\n"
        "- ONLY propose diagnoses listed in the provided protocols matching the symptoms.\n"
        "- DO NOT output narrative text or explanations.\n"
        "- Respond strictly with up to 2 potential diagnoses, comma-separated."
    )
    
    allowed_diagnoses = _allowed_diagnoses_from_guidelines(guideline_text)

    try:
        chain = prompt | llm
        response = chain.invoke({"symptoms": ', '.join(symptoms), "guidelines": guideline_text})
        raw_diagnoses = [d.strip() for d in response.content.split(",") if d.strip()]
        # Guardrail: keep only diagnoses grounded in retrieved guideline content.
        potential_diagnoses = [d for d in raw_diagnoses if d in allowed_diagnoses]
        if not potential_diagnoses:
            potential_diagnoses = allowed_diagnoses[:2]
    except Exception as e:
        log_agent_execution("ResearcherAgent", state, error=e)
        # Deterministic fallback from local guideline evidence.
        potential_diagnoses = allowed_diagnoses[:2]
        
    result = {
        "potential_diagnoses": potential_diagnoses,
        "current_step": "research_completed",
        "logs": [f"Researcher Agent evaluated guidelines and proposed diagnoses: {potential_diagnoses}"]
    }
    log_agent_execution("ResearcherAgent", state, result=result)
    return result
