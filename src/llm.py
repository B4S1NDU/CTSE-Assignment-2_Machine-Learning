from langchain_ollama import ChatOllama

def get_llm():
    """
    Returns the local Small Language Model (SLM) running via Ollama.
    Ensure Ollama is running locally and you have pulled the model (e.g., 'ollama run llama3').
    """
    return ChatOllama(model="llama3", temperature=0.1)
