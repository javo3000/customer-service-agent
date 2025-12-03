"""
LangGraph workflow definition for the customer service agent.
Defines the linear execution flow: Orchestrator -> Tool Node -> Generate.
"""
from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes.orchestrator import orchestrator
from src.agent.nodes.tool_node import tool_node
from src.agent.nodes.generate import generate

# Initialize the graph with AgentState
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("orchestrator", orchestrator)
workflow.add_node("tool_node", tool_node)
workflow.add_node("generate", generate)

# Define linear edges
# 1. Start -> Orchestrator
workflow.set_entry_point("orchestrator")

# 2. Orchestrator -> Tool Node
# The tool node handles conditional execution internally, so we always route to it.
workflow.add_edge("orchestrator", "tool_node")

# 3. Tool Node -> Generate
workflow.add_edge("tool_node", "generate")

# 4. Generate -> End
workflow.add_edge("generate", END)

# Compile the graph
graph = workflow.compile()
