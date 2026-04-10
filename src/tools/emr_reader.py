import json
from typing import Dict, Any

def read_emr(filepath: str) -> Dict[str, Any]:
    """
    STUDENT 1 TOOL: Extracts patient data from an Electronic Medical Record (EMR) system.
    
    Args:
        filepath (str): The absolute or relative path to the local patient JSON file.
        
    Returns:
        Dict[str, Any]: A dictionary containing patient_info, symptoms, and medications.
        
    Raises:
        FileNotFoundError: If the exact EMR file is not located.
        ValueError: If the file contains invalid JSON data.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("EMR data must be a JSON object (dictionary).")
            return data
    except FileNotFoundError:
        print(f"[!] Error: The EMR file at {filepath} was not found.")
        return {"patient_info": {}, "symptoms": [], "current_medications": []}
    except json.JSONDecodeError as e:
        print(f"[!] Error: Failed to decode EMR JSON: {str(e)}")
        raise ValueError(f"Invalid JSON format in {filepath}") from e
