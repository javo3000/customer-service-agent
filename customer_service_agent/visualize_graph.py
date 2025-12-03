"""
Script to visualize the LangGraph workflow.
Generates a mermaid diagram of the graph structure.
"""
import sys
sys.path.insert(0, 'src')

from agent.graph import graph

def visualize_graph():
    try:
        # Generate mermaid diagram
        mermaid_png = graph.get_graph().draw_mermaid_png()
        
        # Save to file
        output_path = "graph_visualization.png"
        with open(output_path, "wb") as f:
            f.write(mermaid_png)
            
        print(f"Graph visualization saved to {output_path}")
        
    except Exception as e:
        print(f"Error generating visualization: {e}")
        # Fallback: Print mermaid text
        print("\nMermaid Diagram Source:")
        print(graph.get_graph().draw_mermaid())

if __name__ == "__main__":
    visualize_graph()
