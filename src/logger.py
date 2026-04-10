import logging
import os
from typing import Any, Dict, Optional

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/agent_execution.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("medical_agent_system")

def log_agent_execution(agent_name: str, input_data: Any, result: Any = None, error: Optional[Exception] = None) -> None:
    """
    Log the execution of an agent.
    
    Args:
        agent_name (str): The name of the agent.
        input_data (Any): The input data provided to the agent.
        result (Any, optional): The result produced by the agent. Defaults to None.
        error (Exception, optional): An error encountered during execution. Defaults to None.
    """
    if error:
        logger.error(f"Agent '{agent_name}' failed with error: {error}. Input: {input_data}")
    else:
        logger.info(f"Agent '{agent_name}' executed. Input: {input_data} | Result: {result}")

def log_tool_call(tool_name: str, args: tuple, kwargs: dict, result: Any = None, error: Optional[Exception] = None) -> None:
    """
    Log the execution of a tool.
    
    Args:
        tool_name (str): The name of the tool.
        args (tuple): Positional arguments passed to the tool.
        kwargs (dict): Keyword arguments passed to the tool.
        result (Any, optional): The result produced by the tool. Defaults to None.
        error (Exception, optional): An error encountered during execution. Defaults to None.
    """
    if error:
        logger.error(f"Tool '{tool_name}' failed with error: {error}. Args: {args}, Kwargs: {kwargs}")
    else:
        logger.info(f"Tool '{tool_name}' executed. Args: {args}, Kwargs: {kwargs} | Result: {result}")
