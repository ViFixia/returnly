from langgraph.graph import StateGraph, END
from state import AuditorState
from nodes import extraction_node, research_node, auditor_node

# 1. Initialize the Graph with our shared memory (State)
workflow = StateGraph(AuditorState)

# 2. Add our Nodes to the graph
# The string name (e.g., "extract") is how we refer to the node in edges
workflow.add_node("extract", extraction_node)
workflow.add_node("research", research_node)
workflow.add_node("audit", auditor_node)

# 3. Define the Workflow Connections (Edges)
# This is the "Logistics Plan" for the agent's reasoning flow
workflow.set_entry_point("extract")     # Start here
workflow.add_edge("extract", "research") # Then go here
workflow.add_edge("research", "audit")   # Then go here
workflow.add_edge("audit", END)          # Then finish

# 4. Compile the Graph
# This turns the blueprint into an executable "app"
app = workflow.compile()

print("--- Senior Co-worker Graph Compiled Successfully ---")

# (We will add the execution code in Step 5)
# --- Step 5: Execute the Workflow ---
if __name__ == "__main__":
    # 1. Provide the initial input (the start of the state)
    initial_input = {
        "image_path": "receipt.jpg",
        "items": [],
        "logs": []
    }

    print("\n🚀 Starting Agentic Audit Workflow...\n")

    # 2. Run the graph
    # This will step through extractor -> researcher -> auditor
    final_state = app.invoke(initial_input)

    # 3. Display the "Senior Co-worker" results
    print("\n" + "="*50)
    print("📋 FINAL AUDIT REPORT")
    print("="*50)
    print(final_state["audit_report"])

    print("\n" + "="*50)
    print("🔍 VERIFICATION TRACE (Logs)")
    print("="*50)
    for i, log in enumerate(final_state["logs"], 1):
        print(f"{i}. {log}")
    print("="*50 + "\n")