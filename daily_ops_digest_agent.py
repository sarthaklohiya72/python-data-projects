"""
Daily Ops Digest Agent
-----------------------
Ties together the four risk-check agents in this repo into one morning
digest for the factory owner:

    inventory_reorder_agent.py    -> stock below reorder level
    customer_retention_agent.py   -> clients not contacted recently
    production_risk_agent.py      -> production batches running late
    artisan_payment_agent.py      -> artisans with pending payments

Instead of running four scripts and reading four output files, this
agent reads all four source CSVs itself, counts each risk, and asks
Groq (Llama 3.3 70B via LangChain) for one short executive digest —
what needs attention today, in priority order. Saved to
daily_ops_digest.txt.

Expected files (same schemas as the individual risk agents):
    inventory.csv   -> product_name, current_stock, reorder_level
    clients.csv     -> client_name, last_contact_date
    production.csv  -> batch_id, product_name, status, expected_completion_date
    artisans.csv    -> artisan_name, pending_payment
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

OUTPUT_FILE = "daily_ops_digest.txt"


def count_low_stock(path: str = "inventory.csv") -> int:
    """Number of products below their reorder level."""
    inventory = pd.read_csv(path)
    return len(inventory[inventory["current_stock"] < inventory["reorder_level"]])


def count_overdue_clients(path: str = "clients.csv", days: int = 30) -> int:
    """Number of clients not contacted within the risk threshold."""
    clients = pd.read_csv(path, parse_dates=["last_contact_date"])
    today = pd.Timestamp(datetime.date.today())
    clients["days_since_contact"] = (today - clients["last_contact_date"]).dt.days
    return len(clients[clients["days_since_contact"] >= days])


def count_delayed_batches(path: str = "production.csv") -> int:
    """Number of production batches past their expected completion date."""
    production = pd.read_csv(path, parse_dates=["expected_completion_date"])
    today = pd.Timestamp(datetime.date.today())
    is_incomplete = production["status"].str.lower() != "completed"
    is_past_due = production["expected_completion_date"] < today
    return len(production[is_incomplete & is_past_due])


def count_pending_payments(path: str = "artisans.csv") -> int:
    """Number of artisans owed a pending payment."""
    artisans = pd.read_csv(path)
    return len(artisans[artisans["pending_payment"] > 0])


def safe_count(fn, *args) -> int:
    """Run a counter function, treating a missing/unreadable CSV as zero risk."""
    try:
        return fn(*args)
    except (FileNotFoundError, KeyError):
        return 0


def draft_digest(counts: dict) -> str:
    """Ask the LLM to turn the four risk counts into one short executive digest."""
    today = datetime.date.today().strftime("%d %B %Y")
    prompt = f"""You are an operations assistant for an Indian manufacturing business.

Today is {today}. Here are today's risk counts from four monitoring agents:

- Low stock items needing reorder: {counts['low_stock']}
- Clients overdue for contact: {counts['overdue_clients']}
- Production batches running late: {counts['delayed_batches']}
- Artisans with pending payments: {counts['pending_payments']}

Write a short "Daily Ops Digest" for the owner:
- Under 120 words
- Open with one line on overall status (calm day vs. needs attention)
- List the top priority to act on today, in one sentence
- Mention where to find details (the matching agent's output .txt file)
"""
    response = llm.invoke(prompt)
    return response.content


def run():
    print("\n" + "=" * 60)
    print("DAILY OPS DIGEST AGENT")
    print("=" * 60 + "\n")

    # Step 1: gather counts from all four risk areas
    counts = {
        "low_stock": safe_count(count_low_stock),
        "overdue_clients": safe_count(count_overdue_clients),
        "delayed_batches": safe_count(count_delayed_batches),
        "pending_payments": safe_count(count_pending_payments),
    }

    print("Risk counts today:")
    for key, value in counts.items():
        print(f"  {key}: {value}")

    # Step 2: ask the LLM to turn the counts into a short, readable digest
    print("\n📝 Drafting digest...")
    digest = draft_digest(counts)

    # Step 3: save the digest for the owner to read each morning
    with open(OUTPUT_FILE, "w") as f:
        f.write(digest)

    print(f"\n{digest}")
    print(f"\n✅ Digest saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
