import os
from datetime import datetime
from typing import Optional

from src.logger import log_tool_call

def secure_write_report(content: str) -> str:
    """
    Securely writes the generated clinical medical report to disk.
    
    Args:
        content: The synthesized final markdown report from the CMO Agent.
        
    Returns:
        str: Absolute filepath indicating where the secure report was successfully generated.
        
    Raises:
        IOError: If permissions are denied or there is an issue saving the output locally.
        ValueError: If content formatting is empty or invalid.
    """
    try:
        if not content or not isinstance(content, str):
            raise ValueError("Report content must be a valid, non-empty string.")
            
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"reports/patient_summary_{timestamp}.md"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        log_tool_call("secure_write_report", (content[:50] + "...",), {}, result=filepath)
        return filepath
    except IOError as e:
        error = IOError(f"Could not save report to reports/ dir. Ensure you have permissions.")
        log_tool_call("secure_write_report", (content[:50] + "...",), {}, error=error)
        raise error from e
    except Exception as e:
        log_tool_call("secure_write_report", (content[:50] + "...",), {}, error=e)
        raise
