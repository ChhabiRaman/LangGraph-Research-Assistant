"""
Main entry point for the research assistant system.
"""

from dotenv import load_dotenv, find_dotenv
from langgraph.checkpoint.memory import MemorySaver

from graphs.assistant_graph import create_assistant_graph

# Load environment variables
load_dotenv(find_dotenv())

def main():
    """Main function to run the research assistant."""
    # Create and compile the graph
    memory = MemorySaver()
    graph_research_assistant = create_assistant_graph().compile(
        interrupt_before=["human_feedback"], 
        checkpointer=memory
    )

    # Initialize parameters
    max_analysts = 2
    topic = "The impact of AI on the future of work"
    thread = {"configurable": {"thread_id": "1"}}

    # First pass - create analysts
    for event in graph_research_assistant.stream(
        {"topic": topic, "max_analysts": max_analysts}, 
        thread, 
        stream_mode="values"
    ):
        # Review analysts
        analysts = event.get('analysts', '')
        if analysts:
            for analyst in analysts:
                print(f"Name: {analyst.name}")
                print(f"Affiliation: {analyst.affiliation}")
                print(f"Role: {analyst.role}")
                print(f"Description: {analyst.description}")
                print("-" * 50)

    # Second pass - handle human feedback
    graph_research_assistant.update_state(
        thread, 
        {"human_suggestion": "Add in someone from HR to add workforce perspective"}, 
        as_node="human_feedback"
    )

    for event in graph_research_assistant.stream(None, thread, stream_mode="values"):
        analysts = event.get('analysts', '')
        if analysts:
            for analyst in analysts:
                print(f"Name: {analyst.name}")
                print(f"Affiliation: {analyst.affiliation}")
                print(f"Role: {analyst.role}")
                print(f"Description: {analyst.description}")
                print("-" * 50)

    # Third pass - continue with interviews
    graph_research_assistant.update_state(
        thread, 
        {"human_suggestion": None}, 
        as_node="human_feedback"
    )

    for event in graph_research_assistant.stream(None, thread, stream_mode="updates"):
        print("--Node--")
        node_name = next(iter(event.keys()))
        print(node_name)

    # Get final report
    final_state = graph_research_assistant.get_state(thread)
    report = final_state.values.get('final_report')
    print(report)

if __name__ == "__main__":
    main()