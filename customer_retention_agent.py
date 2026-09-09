"""
Customer Retention Agent
------------------------
Reads clients.csv, flags clients who haven't been contacted recently
(at risk of churn), and uses Groq (Llama 3.3 70B via LangChain) to draft
a personalized re-engagement message for each one. Drafts are saved to
retention_messages.txt.

Companion to inventory_reorder_agent.py — same pattern (read data ->
flag a risk -> draft an outreach message with an LLM), applied to
client relationships instead of stock levels.

Expected clients.csv columns:
    client_name, last_contact_date, contact_email
"""

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import pandas as pd
import datetime
import os

# Load GROQ_API_KEY from a local .env file
load_dotenv()

# Groq's hosted Llama 3.3 70B model — same model used across this repo's agents
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

CLIENTS_FILE = "clients.csv"
OUTPUT_FILE = "retention_messages.txt"

# A client is considered "at risk" if they haven't been contacted in this many days
DAYS_SINCE_CONTACT_THRESHOLD = 30


def load_at_risk_clients(path: str) -> pd.DataFrame:
    """Return clients not contacted within the risk threshold."""
    clients = pd.read_csv(path, parse_dates=["last_contact_date"])

    # How many days since we last spoke to each client
    today = pd.Timestamp(datetime.date.today())
    clients["days_since_contact"] = (today - clients["last_contact_date"]).dt.days

    return clients[clients["days_since_contact"] >= DAYS_SINCE_CONTACT_THRESHOLD]


def draft_retention_message(row: pd.Series) -> str:
    """Ask the LLM to write a short, warm check-in message for one client."""
    prompt = f"""You are a relationship manager at an Indian manufacturing business.

Write a short, warm check-in message to a client we haven't spoken to in a while.

Client: {row['client_name']}
Days since last contact: {row['days_since_contact']}

Requirements:
- Under 80 words
- Friendly, not salesy
- Reference that it's been a while
- Ask if they have any upcoming requirements
- End with "Regards," and leave the sender name blank
"""
    response = llm.invoke(prompt)
    return response.content


def run():
    print("\n" + "=" * 60)
    print("CUSTOMER RETENTION AGENT")
    print("=" * 60 + "\n")

    # Step 1: find clients who are overdue for contact
    at_risk = load_at_risk_clients(CLIENTS_FILE)

    if at_risk.empty:
        print("✅ All clients have been contacted recently. Nothing to do.")
        return

    messages = []

    # Step 2: draft one message per at-risk client
    for _, row in at_risk.iterrows():
        print(f"💬 Drafting retention message for: {row['client_name']}")
        message_text = draft_retention_message(row)
        messages.append(
            f"To: {row.get('contact_email', 'client@example.com')}\n"
            f"Client: {row['client_name']} ({row['days_since_contact']} days since contact)\n\n"
            f"{message_text}\n"
            + "-" * 60
        )

    # Step 3: save all drafts to a single file for review before sending
    output = "\n\n".join(messages)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"\n✅ {len(at_risk)} retention message(s) drafted and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
