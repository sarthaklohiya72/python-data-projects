import autogen
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

# ── Config using Groq ──────────────────────────────
config_list = [
    {
        "model": "llama-3.3-70b-versatile",
        "api_key": os.getenv("GROQ_API_KEY"),
        "base_url": "https://api.groq.com/openai/v1",
        "api_type": "groq"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.7
}

# ── Load Business Data ─────────────────────────────
orders = pd.read_csv("orders.csv")
inventory = pd.read_csv("inventory.csv")

top_buyers = orders.groupby("buyer_name")["order_value"]\
             .sum().sort_values(ascending=False).head(3)

pending = orders[orders["status"] == "pending"]\
          [["buyer_name", "order_value", "order_date"]]

low_stock = inventory[
    inventory["current_stock"] < inventory["reorder_level"]
][["product_name", "current_stock", "reorder_level"]]

business_context = f"""
AGRAWAL METAL WORKS — BUSINESS DATA

TOP BUYERS:
{top_buyers.to_string()}

PENDING ORDERS (urgent):
{pending.to_string()}

LOW STOCK ALERT:
{low_stock.to_string()}
"""

# ── Define Agents ──────────────────────────────────
analyst = autogen.AssistantAgent(
    name="BusinessAnalyst",
    llm_config=llm_config,
    system_message="""You are an expert business analyst 
    for Indian manufacturing companies.
    
    When given business data you:
    1. Identify the top 3 problems
    2. Quantify the impact of each problem
    3. Suggest specific solutions
    
    Always be specific with numbers and names.
    Keep responses under 150 words."""
)

planner = autogen.AssistantAgent(
    name="ActionPlanner",
    llm_config=llm_config,
    system_message="""You are a business action planner
    for small manufacturing businesses in India.
    
    When given an analysis you:
    1. Create a 3-step action plan
    2. Assign timeline to each action (today/week/month)
    3. Estimate expected outcome in rupees or hours saved
    
    Be practical and specific.
    Keep responses under 150 words."""
)

user_proxy = autogen.UserProxyAgent(
    name="FactoryOwner",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("DONE"),
    code_execution_config=False,
    system_message="""You are a factory owner in 
    Rajasthan who needs practical business advice.
    After receiving the action plan say DONE."""
)

# ── Run ────────────────────────────────────────────
print("\n" + "="*60)
print("AUTOGEN — AUTONOMOUS BUSINESS ANALYST")
print("="*60 + "\n")

user_proxy.initiate_chat(
    analyst,
    message=f"""Analyze this business data and 
    give me your top 3 findings:
    
    {business_context}"""
)

print("\n" + "="*60)
print("ACTION PLAN FROM PLANNER:")
print("="*60 + "\n")

user_proxy.initiate_chat(
    planner,
    message=f"""Based on this business situation:
    
    {business_context}
    
    Create a specific 3-step action plan 
    for this week."""
)