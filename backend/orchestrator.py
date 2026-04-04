from langgraph.graph import StateGraph
from backend.agents import (
    planner_agent,
    developer_agent,
    reviewer_agent,
    tester_agent,
    debugger_agent
)

def build_graph():
    graph = StateGraph(dict)

    # Add nodes
    graph.add_node("planner", planner_agent)
    graph.add_node("developer", developer_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("tester", tester_agent)
    graph.add_node("debugger", debugger_agent)

    # Entry point
    graph.set_entry_point("planner")

    # Flow
    graph.add_edge("planner", "developer")
    graph.add_edge("developer", "reviewer")
    graph.add_edge("reviewer", "tester")
    graph.add_edge("tester", "debugger")

    return graph.compile()