# agrawal_meeting_v2.py
from autogen import AssistantAgent, UserProxyAgent
import os
from dotenv import load_dotenv

load_dotenv()

config_list = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": os.getenv("GROQ_API_KEY"),
    "base_url": "https://api.groq.com/openai/v1",
    "api_type": "openai"
}]

llm_config = {"config_list": config_list, "temperature": 0}

# Agent 1 — Meeting Analyzer
analyzer = AssistantAgent(
    name="MeetingAnalyzer",
    system_message="""You are an AI assistant for Agrawal Metal Works.
    Given raw meeting notes, extract:
    1. Key decisions made
    2. Action items with owner and deadline
    3. Follow-up email draft in professional Hindi/English
    Format output clearly with headers.""",
    llm_config=llm_config
)

# Agent 2 — Proxy (runs the task)
proxy = UserProxyAgent(
    name="Manager",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
    code_execution_config=False
)

# Sample meeting notes
meeting_notes = """
Date: 5 June 2026
Attendees: Rajesh Agrawal (MD), Sunil (Factory Head), Priya (Sales)

Discussion:
- Factory 2 coil stock running low, need to reorder 50 tons copper by 10 June
- Mehta Exports delayed payment of 6 lakh, follow up needed
- New order from Singh & Co for 30 tons brass fitting confirmed
- SAP training for factory staff to be scheduled next week
- Sarthak to demo AI meeting tool next Thursday
"""

proxy.initiate_chat(
    analyzer,
    message=f"Analyze these meeting notes and give structured output:\n\n{meeting_notes}"
)