# Healthcare Multi-Agent System (MAS) - Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                     HEALTHCARE MULTI-AGENT SYSTEM                       │
│                         (LangGraph Orchestrator)                        │
└─────────────────────────────────────────────────────────────────────────┘

                              START
                                ↓
        ┌───────────────────────────────────────────────┐
        │  STEP 0: Initialize Global State Object       │
        │  PatientState {                               │
        │    - raw_emr_path                             │
        │    - symptoms[]                               │
        │    - potential_diagnoses[]                    │
        │    - drug_interactions[]                      │
        │    - logs[] (Observability)                   │
        │  }                                            │
        └───────────────────┬───────────────────────────┘
                            ↓
        ╔═══════════════════════════════════════════════╗
        ║  AGENT 1: TRIAGE SPECIALIST (Student 1)       ║
        ║  Role: Extract & Structure Patient Data       ║
        ╚═════════════╤═══════════════════════════════╝
                      ↓
        ┌─────────────────────────────────────────────┐
        │ TOOL 1: emr_reader.py                       │
        │ • Opens local JSON file                      │
        │ • Parses unstructured EMR text               │
        │ • Returns structured dict                    │
        │ • Type Hints: Dict[str, Any] ✓               │
        │ • Error Handling: FileNotFoundError ✓        │
        │ • Docstring: Comprehensive ✓                 │
        └─────────────────────────────────────────────┘
                      ↓
        STATE UPDATE: Add patient_info, symptoms
                      ↓
        ╔═══════════════════════════════════════════════╗
        ║  AGENT 2: MEDICAL RESEARCHER (Student 2)     ║
        ║  Role: Propose Differential Diagnosis         ║
        ╚═════════════╤═══════════════════════════════╝
                      ↓
        ┌─────────────────────────────────────────────┐
        │ TOOL 2: guideline_search.py                 │
        │ • Searches local medical protocols           │
        │ • Matches symptoms to guidelines             │
        │ • Returns protocol recommendations           │
        │ • Type Hints: List[str] → str ✓              │
        │ • Error Handling: TypeError, ValueError ✓    │
        │ • Docstring: Comprehensive ✓                 │
        └─────────────────────────────────────────────┘
                      ↓
        STATE UPDATE: Add potential_diagnoses
                      ↓
        ╔═══════════════════════════════════════════════╗
        ║  AGENT 3: PHARMACOLOGIST (Student 3)         ║
        ║  Role: Check Drug-Diagnosis Interactions     ║
        ╚═════════════╤═══════════════════════════════╝
                      ↓
        ┌─────────────────────────────────────────────┐
        │ TOOL 3: drug_checker.py                     │
        │ • Queries local medication database          │
        │ • Checks contraindications                   │
        │ • Flags severe warnings                      │
        │ • Type Hints: Lists → List[str] ✓            │
        │ • Error Handling: ValueError, IOError ✓      │
        │ • Docstring: Comprehensive ✓                 │
        └─────────────────────────────────────────────┘
                      ↓
        STATE UPDATE: Add drug_interactions warnings
                      ↓
        ╔═══════════════════════════════════════════════╗
        ║  AGENT 4: CHIEF MEDICAL OFFICER (Student 4)  ║
        ║  Role: Synthesize & Report Generation        ║
        ╚═════════════╤═══════════════════════════════╝
                      ↓
        ┌─────────────────────────────────────────────┐
        │ TOOL 4: report_writer.py                    │
        │ • Formats Markdown clinical report           │
        │ • Writes to local /reports/ directory        │
        │ • Timestamps all outputs                     │
        │ • Type Hints: str → str ✓                    │
        │ • Error Handling: IOError, ValueError ✓      │
        │ • Docstring: Comprehensive ✓                 │
        └─────────────────────────────────────────────┘
                      ↓
        FINAL STATE: All fields populated + audit log
                      ↓
                      END
                      ↓
           ✓ OUTPUT: /reports/patient_summary_*.md


## Data Flow & State Management

┌──────────────────────────────────────────────────────────────┐
│ GLOBAL STATE OBJECT (Secure Handoff Between Agents)          │
│                                                              │
│ Initial → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Final    │
│   ✓        ✓         ✓         ✓         ✓        ✓        │
│ No context loss. Every agent's output appends to logs.      │
└──────────────────────────────────────────────────────────────┘


## LLM Integration (Zero-Cost Local)

┌────────────────────────────────────────────────────┐
│  Local Ollama (llama3:8b)                          │
│  Running on: http://localhost:11434                │
│  Cost: $0 (Runs on your machine)                   │
│  Connected via: src/llm.py → ChatOllama()          │
└────────────────────────────────────────────────────┘


## Testing & Evaluation Strategy

┌─────────────────────────────────────────────────────────────┐
│                   UNIFIED TEST HARNESS                      │
│                    (tests/test_tools.py)                    │
│                                                             │
│  Student 1 Test: test_emr_reader_tool()                     │
│  └─ Validates EMR extraction without crashing              │
│                                                             │
│  Student 2 Test: test_guideline_search_tool()              │
│  └─ Ensures guidelines map correctly to symptoms           │
│                                                             │
│  Student 3 Test: test_drug_checker_tool()                  │
│  └─ Verifies dangerous interactions are flagged             │
│                                                             │
│  Student 4 Test: test_report_writer_tool()                 │
│  └─ Confirms report is written securely to disk            │
└─────────────────────────────────────────────────────────────┘


## Deliverables Checklist

✓ REQUIREMENT 1: MAS Implementation using LangGraph
  └─ src/graph.py - StateGraph orchestrator

✓ REQUIREMENT 2: Implementation of 3–4 Agents
  └─ src/agents/*.py (4 agents, 1 per student)

✓ REQUIREMENT 3: Custom Python Tools
  └─ src/tools/*.py (4 tools with strict type hints)

✓ REQUIREMENT 4: Testing / Evaluation Scripts
  └─ tests/test_tools.py (pytest + property-based tests)

✓ REQUIREMENT 5: Zero-Cost & Local
  └─ src/llm.py - ChatOllama without OpenAI

✓ REQUIREMENT 6: State Management & Observability
  └─ src/state.py - PatientState with logging
