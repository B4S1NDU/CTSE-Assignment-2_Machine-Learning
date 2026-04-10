from langgraph.graph import StateGraph, END
from src.state import PatientState
from src.agents.triage_agent import triage_node
from src.agents.researcher_agent import researcher_node
from src.agents.pharmacologist_agent import pharmacologist_node
from src.agents.cmo_agent import cmo_node

def build_graph():
    """
    Orchestration: Defines the sequential workflow of the Multi-Agent System.
    """
    workflow = StateGraph(PatientState)

    # Add the 4 agent nodes
    workflow.add_node("triage", triage_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("pharmacologist", pharmacologist_node)
    workflow.add_node("cmo", cmo_node)

    # Define the execution flow (Sequential Pipeline)
    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "researcher")
    workflow.add_edge("researcher", "pharmacologist")
    workflow.add_edge("pharmacologist", "cmo")
    workflow.add_edge("cmo", END)

    return workflow.compile()
