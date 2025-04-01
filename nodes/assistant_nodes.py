"""
Nodes for the main research assistant graph.
Contains functions for creating analysts, handling human feedback, and writing reports.
"""

from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.constants import Send

from configs.settings import (
    llm, ANALYST_INSTRUCTIONS, REPORT_WRITER_INSTRUCTIONS,
    INTRO_CONCLUSION_INSTRUCTIONS
)
from models.states import AnalystState, AssistantGraphState
from models.analyst import Analysts

def create_analysts(state: AnalystState) -> Dict[str, Any]:
    """Node for creating a set of AI analyst personas."""
    topic = state["topic"]
    max_analysts = state["max_analysts"]
    human_feedback = state.get("human_suggestion", '')

    system_prompt = ANALYST_INSTRUCTIONS.format(
        topic=topic, 
        max_analysts=max_analysts, 
        human_feedback=human_feedback
    )

    message = [SystemMessage(content=system_prompt)] + [HumanMessage(content="Generate a set of analysts")]
    response = llm.with_structured_output(Analysts).invoke(message)

    return {"analysts": response.analysts}

def human_feedback(state: AnalystState) -> None:
    """Node for handling human feedback on analyst creation."""
    pass

def initiate_all_interviews(state: AssistantGraphState) -> str | List[Send]:
    """Node for initiating all interviews with analysts."""
    human_feedback = state.get("human_suggestion", None)

    if human_feedback:
        return "create_analysts"
    else:
        topic = state["topic"]
        analysts = state["analysts"]
        messages = [HumanMessage(f"So you said you were writing an article on {topic}?")]

        return [
            Send("conduct_interview", {
                "analyst": analyst,
                "topic": topic,
                "max_num_turns": 2,
                "messages": messages
            }) for analyst in analysts
        ]

def write_report(state: AssistantGraphState) -> Dict[str, Any]:
    """Node for writing the final report."""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    system_message = REPORT_WRITER_INSTRUCTIONS.format(
        topic=topic, 
        context=formatted_str_sections
    )    
    report = llm.invoke([
        SystemMessage(content=system_message)
    ] + [HumanMessage(content=f"Write a report based upon these memos.")]) 
    
    return {"content": report.content}

def write_intro(state: AssistantGraphState) -> Dict[str, Any]:
    """Node for writing the report introduction."""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(
        topic=topic, 
        formatted_str_sections=formatted_str_sections
    )    
    intro = llm.invoke([
        instructions
    ] + [HumanMessage(content=f"Write the report introduction")]) 
    
    return {"introduction": intro.content}

def write_conclusion(state: AssistantGraphState) -> Dict[str, Any]:
    """Node for writing the report conclusion."""
    sections = state["sections"]
    topic = state["topic"]

    formatted_str_sections = "\n\n".join([f"{section}" for section in sections])
    
    instructions = INTRO_CONCLUSION_INSTRUCTIONS.format(
        topic=topic, 
        formatted_str_sections=formatted_str_sections
    )    
    conclusion = llm.invoke([
        instructions
    ] + [HumanMessage(content=f"Write the report conclusion")]) 
    
    return {"conclusion": conclusion.content}

def finalize_report(state: AssistantGraphState) -> Dict[str, Any]:
    """Node for finalizing the complete report."""
    content = state["content"]
    if content.startswith("## Insights"):
        content = content.strip("## Insights")
    if "## Sources" in content:
        try:
            content, sources = content.split("\n## Sources\n")
        except:
            sources = None
    else:
        sources = None

    final_report = state["introduction"] + "\n\n---\n\n" + content + "\n\n---\n\n" + state["conclusion"]
    if sources is not None:
        final_report += "\n\n## Sources\n" + sources
    return {"final_report": final_report} 