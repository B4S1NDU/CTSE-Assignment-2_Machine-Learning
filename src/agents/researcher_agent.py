from src.state import PatientState
from src.tools.guideline_search import search_guidelines
from langchain_core.prompts import PromptTemplate
from src.llm import get_llm

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
    
    try:
        chain = prompt | llm
        response = chain.invoke({"symptoms": ', '.join(symptoms), "guidelines": guideline_text})
        potential_diagnoses = [d.strip() for d in response.content.split(",") if d.strip()]
    except Exception as e:
        print(f"LLM execution failed: {e}")
        potential_diagnoses = ["Error: Could not determine diagnoses"]
        
    return {
        "potential_diagnoses": potential_diagnoses,
        "current_step": "research_completed",
        "logs": [f"Researcher Agent evaluated guidelines and proposed diagnoses: {potential_diagnoses}"]
    }
