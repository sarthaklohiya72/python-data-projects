"""
Production Risk Agent
----------------------
Reads production.csv, flags batches that are overdue against their
expected completion date, and uses Groq (Llama 3.3 70B via LangChain)
to draft an internal alert for the ops/production team on each one.
Alerts are saved to production_alerts.txt.

Completes the "read data -> flag a risk -> draft a message" trio
alongside inventory_reorder_agent.py (stock risk) and
customer_retention_agent.py (relationship risk) — this one covers
production/delivery risk, using the `production` table referenced in
the repo's rajasthan_business_db schema.

Expected production.csv columns:
    batch_id, product_name, status, start_date, expected_completion_date
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

PRODUCTION_FILE = "production.csv"
OUTPUT_FILE = "production_alerts.txt"


def load_overdue_batches(path: str) -> pd.DataFrame:
    """Return production batches that are incomplete and past their expected date."""
    production = pd.read_csv(path, parse_dates=["expected_completion_date"])

    today = pd.Timestamp(datetime.date.today())

    # Overdue = not yet completed AND past the expected completion date
    is_incomplete = production["status"].str.lower() != "completed"
    is_past_due = production["expected_completion_date"] < today

    overdue = production[is_incomplete & is_past_due].copy()
    overdue["days_overdue"] = (today - overdue["expected_completion_date"]).dt.days

    return overdue


def draft_production_alert(row: pd.Series) -> str:
    """Ask the LLM to write a short internal alert for one overdue batch."""
    prompt = f"""You are a production coordinator at an Indian metal manufacturing factory.

Write a short internal alert for the ops team about a delayed production batch.

Batch ID: {row['batch_id']}
Product: {row['product_name']}
Status: {row['status']}
Days overdue: {row['days_overdue']}

Requirements:
- Under 80 words
- Direct and factual, not alarmist
- Recommend one concrete next step
- End with "— Production Risk Agent"
"""
    response = llm.invoke(prompt)
    return response.content


def run():
    print("\n" + "=" * 60)
    print("PRODUCTION RISK AGENT")
    print("=" * 60 + "\n")

    # Step 1: find batches that are overdue
    overdue = load_overdue_batches(PRODUCTION_FILE)

    if overdue.empty:
        print("✅ No overdue batches. Production is on schedule.")
        return

    alerts = []

    # Step 2: draft one alert per overdue batch
    for _, row in overdue.iterrows():
        print(f"⚠️  Drafting alert for batch: {row['batch_id']} ({row['product_name']})")
        alert_text = draft_production_alert(row)
        alerts.append(
            f"Batch: {row['batch_id']} — {row['product_name']}\n"
            f"Status: {row['status']} | {row['days_overdue']} day(s) overdue\n\n"
            f"{alert_text}\n"
            + "-" * 60
        )

    # Step 3: save all alerts to a single file for the ops team to review
    output = "\n\n".join(alerts)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"\n✅ {len(overdue)} production alert(s) drafted and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
