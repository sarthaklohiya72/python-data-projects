from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated
import operator
import os
from dotenv import load_dotenv
load_dotenv()

# State definition
class AgentState(TypedDict):
    messages: Annotated[list, operator.add]
    pending_action: str
    approved: bool
    result: str

# Initialize LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Node 1: Analyze situation
def analyze_node(state: AgentState) -> AgentState:
    messages = state["messages"]
    response = llm.invoke(messages)
    
    # Simulate deciding to send a payment reminder
    pending_action = "Send payment reminder to Sharma Textiles — ₹44,000 overdue 30 days"
    
    print("\n" + "="*60)
    print("AGENT ANALYSIS COMPLETE")
    print(f"Proposed Action: {pending_action}")
    print("="*60)
    
    return {
        "messages": [AIMessage(content=response.content)],
        "pending_action": pending_action,
        "approved": False,
        "result": ""
    }

# Node 2: Human approval checkpoint
def human_approval_node(state: AgentState) -> AgentState:
    print(f"\n⚠️  HUMAN APPROVAL REQUIRED")
    print(f"Action: {state['pending_action']}")
    
    user_input = input("Approve? (yes/no): ").strip().lower()
    approved = user_input == "yes"
    
    print(f"Decision: {'✅ Approved' if approved else '❌ Rejected'}")
    return {"approved": approved}

# Node 3: Execute action
def execute_node(state: AgentState) -> AgentState:
    if state["approved"]:
        result = f"✅ EXECUTED: {state['pending_action']}"
        print(f"\n{result}")
    else:
        result = "❌ ACTION CANCELLED by human"
        print(f"\n{result}")
    return {"result": result}

# Routing function
def should_execute(state: AgentState) -> str:
    return "execute" if state["approved"] else END

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("analyze", analyze_node)
workflow.add_node("human_approval", human_approval_node)
workflow.add_node("execute", execute_node)

workflow.set_entry_point("analyze")
workflow.add_edge("analyze", "human_approval")
workflow.add_conditional_edges("human_approval", should_execute, {
    "execute": "execute",
    END: END
})
workflow.add_edge("execute", END)

# Add memory persistence
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# Run the agent
config = {"configurable": {"thread_id": "agrawal_session_1"}}
initial_state = {
    "messages": [HumanMessage(content="Check pending orders and decide if any reminders need to be sent.")],
    "pending_action": "",
    "approved": False,
    "result": ""
}

print("\n🤖 Starting Human-in-the-Loop Agent...")
final_state = app.invoke(initial_state, config)

print("\n" + "="*60)
print("FINAL RESULT:", final_state["result"])
print("="*60)
# Same thread_id = same memory
config = {"configurable": {"thread_id": "agrawal_session_1"}}
follow_up = {
    "messages": [HumanMessage(content="What action did we take last time?")],
    "pending_action": "",
    "approved": False,
    "result": ""
}
result = app.invoke(follow_up, config)
print(result["messages"][-1].content)