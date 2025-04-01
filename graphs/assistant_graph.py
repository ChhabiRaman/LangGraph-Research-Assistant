"""
Graph definition for the main research assistant.
"""

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from models.states import AssistantGraphState
from nodes.assistant_nodes import (
    create_analysts, human_feedback, initiate_all_interviews,
    write_report, write_intro, write_conclusion, finalize_report
)
from graphs.interview_graph import create_interview_graph

def create_assistant_graph() -> StateGraph:
    """Creates and configures the main research assistant graph."""
    research_assistant = StateGraph(AssistantGraphState)
    
    # Add nodes
    research_assistant.add_node("create_analysts", create_analysts)
    research_assistant.add_node("human_feedback", human_feedback)
    research_assistant.add_node("conduct_interview", create_interview_graph().compile())
    research_assistant.add_node("write_report", write_report)
    research_assistant.add_node("write_intro", write_intro)
    research_assistant.add_node("write_conclusion", write_conclusion)
    research_assistant.add_node("finalize_report", finalize_report)
    
    # Add edges
    research_assistant.add_edge(START, "create_analysts")
    research_assistant.add_edge("create_analysts", "human_feedback")
    research_assistant.add_conditional_edges(
        "human_feedback",
        initiate_all_interviews,
        ["create_analysts", "conduct_interview"]
    )
    research_assistant.add_edge("conduct_interview", "write_intro")
    research_assistant.add_edge("conduct_interview", "write_conclusion")
    research_assistant.add_edge("conduct_interview", "write_report")
    research_assistant.add_edge(["write_intro", "write_conclusion", "write_report"], "finalize_report")
    research_assistant.add_edge("finalize_report", END)
    
    return research_assistant 