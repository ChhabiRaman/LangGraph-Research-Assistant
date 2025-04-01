"""
State models for the research assistant system.
Contains the state definitions for both the interview and overall assistant graphs.
"""

from typing import List, TypedDict, Annotated
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage
import operator

from .analyst import Analyst

class AnalystState(TypedDict):
    """State for the analyst creation process."""
    topic: str  # topic of the research
    max_analysts: int  # maximum number of analysts
    analysts: List[Analyst]  # list of analysts
    human_suggestion: str  # human suggestion

class InterviewState(MessagesState):
    """State for the interview process."""
    max_num_turns: int
    analyst: Analyst  # Analyst asking questions
    context: Annotated[list, operator.add]
    interview: str
    sections: list

class AssistantGraphState(TypedDict):
    """State for the overall research assistant graph."""
    topic: str
    max_analysts: int
    human_suggestion: str
    analysts: List[Analyst]
    sections: Annotated[list, operator.add]  # Send() API key
    introduction: str  # Introduction for the final report
    content: str  # Content for the final report
    conclusion: str  # Conclusion for the final report
    final_report: str  # Final report 