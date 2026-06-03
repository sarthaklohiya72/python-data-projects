from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import pandas as pd
import os
os.environ["OPENAI_API_KEY"] = "fake-key"
os.environ["OPENAI_BASE_URL"] = "https://bedrock-runtime.us-east-1.amazonaws.com"

from crewai import Agent, Task, Crew, Process

llm = "bedrock/amazon.nova-micro-v1:0"

# Load business data
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
TOP BUYERS:
{top_buyers.to_string()}

PENDING ORDERS:
{pending.to_string()}

LOW STOCK:
{low_stock.to_string()}
"""

researcher = Agent(
    role="Business Data Researcher",
    goal="Analyze business data and find top 3 critical insights",
    backstory="Expert business analyst for Indian manufacturing businesses.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

analyst = Agent(
    role="Business Strategy Analyst",
    goal="Create actionable strategies from research findings",
    backstory="Senior strategy consultant for Indian manufacturing companies.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role="Business Report Writer",
    goal="Write clear reports that factory owners understand",
    backstory="Writes weekly reports for factory owners in Rajasthan.",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

research_task = Task(
    description=f"Analyze this data and find top 3 critical insights:\n{business_data}",
    agent=researcher,
    expected_output="3 critical findings with specific numbers"
)

strategy_task = Task(
    description="Based on research findings create 3 specific strategies with timelines.",
    agent=analyst,
    expected_output="3 specific strategies with timelines"
)

report_task = Task(
    description="""Write a weekly business report under 150 words.
    Format:
    WEEKLY BUSINESS REPORT
    EXECUTIVE SUMMARY (2 lines)
    TOP 3 ACTIONS THIS WEEK:
    1.
    2.
    3.
    URGENT ALERTS:""",
    agent=writer,
    expected_output="Weekly report under 150 words"
)

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, strategy_task, report_task],
    process=Process.sequential,
    verbose=True
)

print("\n" + "="*60)
print("AGRAWAL METAL WORKS — 3-AGENT BUSINESS CREW")
print("="*60 + "\n")

result = crew.kickoff()

print("\n" + "="*60)
print("FINAL WEEKLY REPORT:")
print("="*60)
print(result)