import boto3
import pandas as pd
import os

# Paste your keys directly for now
client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id="",
    aws_secret_access_key=""
)

def ask_claude(role, task):
    response = client.converse(
        modelId="amazon.nova-micro-v1:0",
        system=[{"text": f"You are a {role}."}],
        messages=[{"role": "user", "content": [{"text": task}]}]
    )
    return response["output"]["message"]["content"][0]["text"]

# Load data
orders = pd.read_csv("orders.csv")
inventory = pd.read_csv("inventory.csv")

top_buyers = orders.groupby("buyer_name")["order_value"]\
             .sum().sort_values(ascending=False).head(3)
pending = orders[orders["status"]=="pending"]\
          [["buyer_name","order_value","order_date"]]
low_stock = inventory[
    inventory["current_stock"] < inventory["reorder_level"]
][["product_name","current_stock","reorder_level"]]

business_data = f"""
TOP BUYERS: {top_buyers.to_string()}
PENDING ORDERS: {pending.to_string()}
LOW STOCK: {low_stock.to_string()}
"""

print("="*60)
print("AGRAWAL METAL WORKS — 3-AGENT SYSTEM")
print("="*60)

# Agent 1 — Researcher
print("\n[AGENT 1 - RESEARCHER] Analyzing data...")
research = ask_claude(
    "Business Data Researcher for Indian manufacturing",
    f"Find top 3 critical insights from this data:\n{business_data}"
)
print(research)

# Agent 2 — Analyst
print("\n[AGENT 2 - ANALYST] Creating strategies...")
strategy = ask_claude(
    "Business Strategy Analyst",
    f"Based on these findings:\n{research}\n\nCreate 3 specific strategies with timelines."
)
print(strategy)

# Agent 3 — Writer
print("\n[AGENT 3 - WRITER] Writing report...")
report = ask_claude(
    "Business Report Writer for factory owners",
    f"""Using these findings and strategies:
{research}
{strategy}

Write a weekly report under 150 words:
WEEKLY BUSINESS REPORT
EXECUTIVE SUMMARY:
TOP 3 ACTIONS THIS WEEK:
1.
2.
3.
URGENT ALERTS:"""
)

print("\n" + "="*60)
print("FINAL REPORT:")
print("="*60)
print(report)