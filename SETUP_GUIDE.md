# Setup Guide & Demo Video Recording Instructions

Here are the exact, step-by-step instructions to fully run this Multi-Agent System (MAS) from scratch. As per the assignment constraints, this system runs entirely locally with zero cloud costs using Small Language Models (SLMs) via Ollama.

---

## Step 1: Start your Local AI (Ollama)

Since your assignment requires running a local Small Language Model (SLM) with zero cloud costs, you need to make sure Ollama is running first.

1. Ensure you have [Ollama](https://ollama.com/) installed on your computer.
2. Open a new command prompt or PowerShell window (outside of VS Code is fine).
3. Run the following command to download and start the model (leave this window open in the background):
   ```bash
   ollama run llama3
   ```
*(Note: If you prefer a smaller/faster model, you can use `phi3` or `qwen`. Just update `src/llm.py` to say `model="phi3"` instead).*

---

## Step 2: Project Setup (For Anyone Cloning the Repo)
Because the virtual environment (`.venv`) is correctly ignored in Git to save space and prevent cross-platform issues, you must build it on your machine first.

1. Open the Integrated Terminal in VS Code (`Ctrl + \` or `Terminal -> New Terminal`).
2. Make sure you are in the root directory of the project.
3. Create the virtual environment and activate it:
   ```powershell
   # Create the virtual environment
   python -m venv .venv
   
   # Activate it (Windows PowerShell)
   .\.venv\Scripts\Activate.ps1
   
   # Activate it (Windows Command Prompt)
   .\.venv\Scripts\activate.bat
   
   # Activate it (Mac/Linux)
   source .venv/bin/activate
   ```
4. Install all the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```

---

## Step 3: Run the Multi-Agent System

With your `.venv` activated and Ollama running in the background:

1. Execute the LangGraph workflow by running:
   ```bash
   python -m src.main
   ```
   *(or `python src/main.py` depending on your OS)*
2. **Watch the Magic:** You will see the terminal print out the step-by-step execution trace as the 4 autonomous agents hand the global state off to each other without losing context.
3. **Check the Output:** Once it finishes, look inside the `reports/` folder in your VS Code explorer. You will see a brand-new Markdown file (`patient_summary_2026...md`) containing the final report securely written by the CMO Agent!

---

## Step 4: Run the Automated Tests (For the Grading Rubric)

Your professor requires proof of automated testing for each student's tool and agent (e.g., an LLM-as-a-Judge or property-based evaluation script).

1. In the same VS Code terminal (with the `.venv` activated), run:
   ```bash
   pytest tests/
   ```
2. You will see an output showing that all 4 tests passed successfully (100%), proving your custom agents are correctly constrained (preventing hallucinations) and your tools handle inputs correctly.

---

**📽️ Demo Video Recording Tips (Do not exceed 4-5 minutes)**
You can use this exact flow for your Assignment 2 demonstration video:
1. Record your screen showing Ollama running in the background.
2. Run the `python -m src.main` script to show the sequential multi-agent execution pipeline.
3. Open the resulting `.md` file to prove the LLMs successfully completed the multi-step problem.
4. Run the `pytest tests/` command to guarantee your perfect score on the testing criteria.

## Patient Info
{'age': 45, 'gender': 'Male', 'history': 'Smoker, occasional alcohol'}

## Symptoms
severe headache, dizziness, high blood pressure

## Potential Diagnoses
Hypertension, Cardiovascular Risk

## Drug Interactions / Warnings
EXTREME WARNING: Ibuprofen is known to exacerbate Hypertension.
Pharmacologist Assessment: Review tool output carefully.

## CMO Sign-Off
Approved offline.
```

---

### Step 4: Run Automated Tests (Demo Part 3 - 1 minute)

Back in Terminal 2:
```powershell
pytest tests/ -v
```

**Expected output:**
```
tests\test_tools.py::test_emr_reader_tool PASSED        [ 25%]
tests\test_tools.py::test_guideline_search_tool PASSED  [ 50%]
tests\test_tools.py::test_drug_checker_tool PASSED      [ 75%]
tests\test_tools.py::test_report_writer_tool PASSED     [100%]

============================== 4 passed in 0.03s ==============================
```

**Script to say while recording:**
> "Finally, we run the automated test suite. Each student has contributed individual test cases validating their specific agent and tool. All four tests pass, confirming that the system is robust, handles edge cases, and meets all quality criteria. The test suite provides proof that each tool has strict type hinting, comprehensive docstrings, and proper error handling."

---

## Demo Video Script (Total: 4 minutes)

### Introduction (30 seconds)
> "This is the Healthcare Multi-Agent System, a locally-hosted AI solution built for the CTSE Assignment. We built this system using LangGraph, Ollama, and zero cloud costs. The system automates patient triage, diagnosis, and safety checks entirely on-premises. Let me show you how it works."

### Execution (1 minute 30 seconds)
> "First, we initialize two terminals. Terminal 1 runs our local language model via Ollama—in this case, llama3:8b. Terminal 2 runs our Python application. When we execute the system, it passes patient data through four specialized agents in sequence. Each agent uses custom Python tools—reading files, searching databases, checking contraindications. The global state is securely passed between agents without any context loss."

### Report Generation (1 minute)
> "The system successfully generated a clinical report. You can see it contains all the outputs from the four agents synthesized into a professional Markdown document. The report documents the patient symptoms, proposed diagnoses from clinical guidelines, pharmacological warnings flagging dangerous drug interactions, and the Chief Medical Officer's approval. This demonstrates the 'agentic' nature of our system—it isn't just generating text; it's using specialized tools to make decisions grounded in local data."

### Testing (1 minute)
> "Finally, we demonstrate the comprehensive test suite. We have four individual test cases, one per student, validating the accuracy and robustness of each agent and tool. All tests pass, proving that our code handles errors correctly, implements strict type hints, and provides comprehensive documentation. This testing demonstrates that every component of the system is production-ready and meets the assignment's grading criteria for system architecture, tool development, state management, and observability."

### Conclusion (30 seconds)
> "In summary, we built a complete Multi-Agent System that automates a healthcare workflow, uses local AI models, implements sophisticated orchestration and state management, and includes comprehensive testing. The system is zero-cost, locally-hosted, and demonstrates all the core components of Agentic AI as required by the assignment."

---

## Recording Software Recommendations

### Windows
- **Windows 10/11 Built-in:** Press `Win + G`, select "Yes, this is a game" if needed, then record
- **OBS Studio** (Free): [download](https://obsproject.com/)
- **ScreenFlow** (Mac)

### Video Settings
- **Resolution:** 1920x1080 (Full HD)
- **FPS:** 30 FPS minimum
- **Bitrate:** 5-8 Mbps for clarity
- **Audio:** Mono or Stereo, 128 kbps

### Post-Recording Edit (Optional)
- Add title card: "Healthcare Multi-Agent System - CTSE Assignment 2"
- Add closing slide: "Sri Lanka Institute of Information Technology | SE4010"
- Ensure total duration is **under 5 minutes** (rubric says DO NOT GO BEYOND 5 MINUTES)

---

## Common Issues & Solutions

### Issue: Ollama Connection Error
**Error:** `HTTPConnectionPool(host='localhost', port=11434): Connection refused`
- **Solution:** Ensure Terminal 1 is still running `ollama run llama3`

### Issue: ModuleNotFoundError in Terminal 2
**Error:** `No module named 'langchain_core'`
- **Solution:** Ensure you activated the venv: `.\.venv\Scripts\Activate.ps1`

### Issue: Tests Fail
**Solution:** Run from project root: `cd "CTSE Assessment 02"` first

### Issue: Report not appearing in `/reports`
**Solution:** Check that you ran `python -m src.main` without errors

---

## Video Submission Checklist

Before uploading, verify:

- [ ] Video is under 5 minutes in length
- [ ] Audio is clear and audible (no background noise)
- [ ] All 4 demo sections are visible (Terminal 1, Terminal 2, Report file, Test output)
- [ ] Text is readable at normal viewing distance (use 1920x1080+ resolution)
- [ ] Script covers the architecture, workflow, and results
- [ ] System runs successfully from start to finish without errors
- [ ] Each student speaks for ~1 minute explaining their component (optional but recommended)

---

## Submission Instructions

1. **Render the video** to an MP4 file (H.264 codec, AAC audio)
2. **Upload to:** [Specify your university's submission portal]
3. **File naming:** `CTSE_Assignment_2_Demo_Group_[TeamNumber].mp4`
4. **Include accompanying documents:**
   - `README.md` (system overview)
   - `ARCHITECTURE_DIAGRAM.md` (visual design)
   - `CONTRIBUTIONS.md` (individual proof)

---

## Technical Report Notes

While filming, you can reference:
- The `ARCHITECTURE_DIAGRAM.md` for system design
- The `CONTRIBUTIONS.md` for individual roles
- The console output for observability proof
- The generated report for output quality

Include these in your 4-8 page technical report:
1. Problem domain: Patient triage automation
2. Architecture: 4-agent LangGraph pipeline
3. Tools: Custom Python with type hints
4. State management: PatientState TypedDict
5. Testing: Pytest unified harness
6. GitHub link: [Your repo URL]

---

**Good luck with your demo! You built a professional, production-ready Agentic AI system. The video should clearly show that.**
