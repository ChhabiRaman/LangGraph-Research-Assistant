"""
Nodes for the interview graph in the research assistant system.
Contains functions for asking questions, searching, generating answers, and saving interviews.
"""

from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_community.document_loaders import WikipediaLoader
from pydantic import BaseModel

from configs.settings import (
    llm, google_serper, QUESTION_INSTRUCTIONS, SEARCH_INSTRUCTIONS,
    ANSWER_INSTRUCTIONS, SECTION_WRITER_INSTRUCTIONS
)
from models.states import InterviewState

class SearchQuery(BaseModel):
    """Model for search queries."""
    search_query: str

def ask_question(state: InterviewState) -> Dict[str, Any]:
    """Node for asking questions during the interview."""
    messages = state["messages"]
    analyst = state["analyst"]

    system_prompt = QUESTION_INSTRUCTIONS.format(goals=analyst.persona)
    question = llm.invoke([SystemMessage(content=system_prompt)] + messages)

    return {"messages": [question]}

def search_google(state: InterviewState) -> Dict[str, Any]:
    """Node for performing Google searches."""
    messages = state["messages"]
    
    query = llm.with_structured_output(SearchQuery).invoke([SystemMessage(content=SEARCH_INSTRUCTIONS)] + messages)
    context = google_serper.results(query=query.search_query)

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document href="{doc["link"]}"/>\n{doc["snippet"]}\n</Document>'
            for doc in context['organic'][:2]
        ]
    )

    return {'context': [formatted_search_docs]}

def search_wikipedia(state: InterviewState) -> Dict[str, Any]:
    """Node for performing Wikipedia searches."""
    messages = state['messages']

    query = llm.with_structured_output(SearchQuery).invoke([SystemMessage(content=SEARCH_INSTRUCTIONS)] + messages)
    wiki_docs = WikipediaLoader(query=query.search_query, load_max_docs=2).load()

    formatted_search_docs = "\n\n---\n\n".join(
        [
            f'<Document source="{doc.metadata["source"]}" page="{doc.metadata.get("page", "")}"/>\n{doc.page_content}\n</Document>'
            for doc in wiki_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def generate_answer(state: InterviewState) -> Dict[str, Any]:
    """Node for generating answers to interview questions."""
    analyst = state["analyst"]
    context = state["context"]
    messages = state["messages"]

    system_prompt = ANSWER_INSTRUCTIONS.format(goals=analyst.persona, context=context)
    answer = llm.invoke([SystemMessage(content=system_prompt)] + messages)

    # Name the message as coming from the expert
    answer.name = "expert"

    return {"messages": [answer]}

def save_interview(state: InterviewState) -> Dict[str, Any]:
    """Node for saving the interview."""
    from langchain_core.messages import get_buffer_string
    
    messages = state["messages"]
    interview = get_buffer_string(messages)
    
    return {"interview": interview}

def write_section(state: InterviewState) -> Dict[str, Any]:
    """Node for writing a section of the report."""
    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    system_message = SECTION_WRITER_INSTRUCTIONS.format(focus=analyst.description)
    section = llm.invoke(
        [SystemMessage(content=system_message)] + 
        [HumanMessage(content=f"Use this source to write your section: {context}")]
    )          
    
    return {"sections": [section.content]}

def route_messages(state: InterviewState, name: str = "expert") -> str:
    """Router for determining the next step in the interview process."""
    messages = state["messages"]
    max_num_turns = state.get('max_num_turns', 2)

    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )

    if num_responses >= max_num_turns:
        return 'save_interview'

    last_question = messages[-2]
    
    if "Thank you so much for your help" in last_question.content:
        return 'save_interview'
    return "ask_question" 