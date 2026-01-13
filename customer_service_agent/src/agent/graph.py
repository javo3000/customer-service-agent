"""
LangGraph workflow definition for the customer service agent.
Defines conditional execution flow with rerouting capability.

Flow:
  START → Orchestrator → Tool Node → Generate → [Context Sufficient?]
                                                    ↓
                                              Yes → END
                                              No (retry=0) → Orchestrator (web search)
                                              No (retry≥1) → END (ask user)
"""
from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes.orchestrator import orchestrator
from src.agent.nodes.tool_node import tool_node
from src.agent.nodes.generate import generate


def should_reroute(state: AgentState) -> str:
    """
    Determines whether to reroute back to orchestrator for web search
    or proceed to END.
    
    Returns:
        "orchestrator" if needs_web_search flag is set and retry allowed
        END otherwise
    """
    needs_web_search = state.get("needs_web_search", False)
    retry_count = state.get("retry_count", 0)
    
    # If generate node set the web search flag and we haven't exceeded retry limit
    if needs_web_search and retry_count <= 1:
        return "orchestrator"
    
    return END


# Initialize the graph with AgentState
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("orchestrator", orchestrator)
workflow.add_node("tool_node", tool_node)
workflow.add_node("generate", generate)

# Define edges
# 1. Start → Orchestrator
workflow.set_entry_point("orchestrator")

# 2. Orchestrator → Tool Node
workflow.add_edge("orchestrator", "tool_node")

# 3. Tool Node → Generate
workflow.add_edge("tool_node", "generate")

# 4. Generate → Conditional (reroute or end)
workflow.add_conditional_edges(
    "generate",
    should_reroute,
    {
        "orchestrator": "orchestrator",
        END: END
    }
)

# Compile the graph
graph = workflow.compile()

