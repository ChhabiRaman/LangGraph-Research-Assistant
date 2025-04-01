"""
Graph definition for the interview process.
"""

from langgraph.graph import StateGraph, START, END

from models.states import InterviewState
from nodes.interview_nodes import (
    ask_question, search_google, search_wikipedia,
    generate_answer, save_interview, write_section,
    route_messages
)

def create_interview_graph() -> StateGraph:
    """Creates and configures the interview graph."""
    research_interview = StateGraph(InterviewState)
    
    # Add nodes
    research_interview.add_node("ask_question", ask_question)
    research_interview.add_node("search_google", search_google)
    research_interview.add_node("search_wikipedia", search_wikipedia)
    research_interview.add_node("generate_answer", generate_answer)
    research_interview.add_node("save_interview", save_interview)
    research_interview.add_node("write_section", write_section)
    
    # Add edges
    research_interview.add_edge(START, "ask_question")
    research_interview.add_edge("ask_question", "search_google")
    research_interview.add_edge("ask_question", "search_wikipedia")
    research_interview.add_edge("search_google", "generate_answer")
    research_interview.add_edge("search_wikipedia", "generate_answer")
    research_interview.add_conditional_edges(
        "generate_answer",
        route_messages,
        {"ask_question": "ask_question", "save_interview": "save_interview"}
    )
    research_interview.add_edge("save_interview", "write_section")
    research_interview.add_edge("write_section", END)
    
    return research_interview 