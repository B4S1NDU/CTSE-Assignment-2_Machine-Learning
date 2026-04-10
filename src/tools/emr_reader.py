import json
from typing import Dict, Any

from src.logger import log_tool_call

def read_emr(filepath: str) -> Dict[str, Any]:
    """
    Extracts patient data from an Electronic Medical Record (EMR) system file.
    
    Args:
        filepath: The absolute or relative path to the local patient JSON file.
        
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
            log_tool_call("read_emr", (filepath,), {}, result=data)
            return data
    except FileNotFoundError as e:
        log_tool_call("read_emr", (filepath,), {}, error=e)
        return {"patient_info": {}, "symptoms": [], "current_medications": []}
    except json.JSONDecodeError as e:
        error = ValueError(f"Invalid JSON format in {filepath}")
        log_tool_call("read_emr", (filepath,), {}, error=error)
        raise error from e
    except Exception as e:
        log_tool_call("read_emr", (filepath,), {}, error=e)
        raise
