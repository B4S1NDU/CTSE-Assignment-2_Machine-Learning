import os
from datetime import datetime

def secure_write_report(content: str) -> str:
    """
    STUDENT 4 TOOL: Securely writes the generated clinical medical report to disk.
    
    Args:
        content (str): The synthesized final markdown report from the CMO Agent.
        
    Returns:
        str: Absolute filepath indicating where the secure report was successfully generated.
        
    Raises:
        IOError: If permissions are denied or there is an issue saving the output locally.
        ValueError: If content formatting is empty or invalid.
    """
    if not content or not isinstance(content, str):
        raise ValueError("Report content must be a valid, non-empty string.")
        
    print("[*] Tool: Writing secure clinical report to disk...")
    
    try:
        os.makedirs("reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = f"reports/patient_summary_{timestamp}.md"
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
            
        return filepath
    except IOError as e:
        print(f"[!] Error: Failed to secure local disk write: {str(e)}")
        raise IOError(f"Could not save report to reports/ dir. Ensure you have permissions.") from e
