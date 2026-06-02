from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain.tools import tool
from dotenv import load_dotenv
import pandas as pd
import os
from typing import TypedDict, List

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── Define Tools ───────────────────────────────────
@tool
def get_top_buyers(n: int = 5) -> str:
    """Get top buyers by revenue from business data"""
    df = pd.read_csv("orders.csv")
    result = df.groupby("buyer_name")["order_value"]\
               .sum()\
               .sort_values(ascending=False)\
               .head(n)
    return result.to_string()

@tool
def get_pending_orders() -> str:
    """Get all pending orders with days pending"""
    df = pd.read_csv("orders.csv")
    pending = df[df["status"] == "pending"]\
              [["buyer_name", "order_value", "order_date"]]
    return pending.to_string()

@tool
def get_low_stock() -> str:
    """Get products that need reordering"""
    df = pd.read_csv("inventory.csv")
    low = df[df["current_stock"] < df["reorder_level"]]\
          [["product_name", "current_stock", "reorder_level"]]
    return low.to_string()

@tool
def generate_business_insight(data: str) -> str:
    """Generate business insight from data"""
    response = llm.invoke(
        f"Give 3 actionable bullet points for this data: {data}"
    )
    return response.content

# ── Define State ───────────────────────────────────
class AgentState(TypedDict):
    messages: List[str]
    data_collected: str
    final_report: str

# ── Define Nodes ───────────────────────────────────
def collect_data(state: AgentState) -> AgentState:
    """Agent collects all business data"""
    print("🔍 Agent collecting business data...")

    buyers = get_top_buyers.invoke({"n": 3})
    pending = get_pending_orders.invoke({})
    stock = get_low_stock.invoke({})

    data = f"""
TOP BUYERS:
{buyers}

PENDING ORDERS:
{pending}

LOW STOCK:
{stock}
"""
    state["data_collected"] = data
    state["messages"].append("Data collected successfully")
    print("✅ Data collected")
    return state

def analyze_data(state: AgentState) -> AgentState:
    """Agent analyzes the collected data"""
    print("🧠 Agent analyzing data...")

    insight = generate_business_insight.invoke(
        {"data": state["data_collected"]}
    )
    state["messages"].append(f"Analysis: {insight}")
    print("✅ Analysis done")
    return state

def generate_report(state: AgentState) -> AgentState:
    """Agent generates final business report"""
    print("📝 Agent generating report...")

    report_prompt = f"""
    Create a brief weekly business report based on:
    {state["data_collected"]}

    Previous analysis: {state["messages"][-1]}

    Format as:
    1. Executive Summary (2 lines)
    2. Key Actions This Week (3 bullets)
    3. Alerts (any urgent items)
    """

    response = llm.invoke(report_prompt)
    state["final_report"] = response.content
    print("✅ Report generated")
    return state

# ── Build Graph ────────────────────────────────────
workflow = StateGraph(AgentState)

workflow.add_node("collect_data", collect_data)
workflow.add_node("analyze_data", analyze_data)
workflow.add_node("generate_report", generate_report)

workflow.set_entry_point("collect_data")
workflow.add_edge("collect_data", "analyze_data")
workflow.add_edge("analyze_data", "generate_report")
workflow.add_edge("generate_report", END)

app = workflow.compile()

# ── Run Agent ──────────────────────────────────────
print("\n" + "="*50)
print("AGRAWAL METAL WORKS — WEEKLY BUSINESS AGENT")
print("="*50 + "\n")

result = app.invoke({
    "messages": [],
    "data_collected": "",
    "final_report": ""
})

print("\n" + "="*50)
print("FINAL REPORT:")
print("="*50)
print(result["final_report"])