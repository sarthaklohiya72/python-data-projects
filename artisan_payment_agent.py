"""
Artisan Payment Agent
----------------------
Reads artisans.csv, finds artisans with an outstanding pending payment,
and uses Groq (Llama 3.3 70B via LangChain) to draft a short payment
status message for each one. Drafts are saved to artisan_payment_notices.txt.

Completes the risk-agent set alongside inventory_reorder_agent.py (stock),
customer_retention_agent.py (client relationships), and
production_risk_agent.py (production delays) — this one covers artisan
payments, using the `artisans` table referenced in the repo's
rajasthan_business_db schema.

Expected artisans.csv columns:
    artisan_name, work_type, pending_payment, last_payment_date, contact_number
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

ARTISANS_FILE = "artisans.csv"
OUTPUT_FILE = "artisan_payment_notices.txt"


def load_pending_payments(path: str) -> pd.DataFrame:
    """Return artisans who have a pending payment greater than zero."""
    artisans = pd.read_csv(path)
    return artisans[artisans["pending_payment"] > 0]


def draft_payment_message(row: pd.Series) -> str:
    """Ask the LLM to write a short payment status message for one artisan."""
    prompt = f"""You are a payments coordinator at an Indian manufacturing business
that works with independent artisans.

Write a short, respectful message to an artisan about their pending payment.

Artisan: {row['artisan_name']}
Work type: {row['work_type']}
Pending amount: ₹{row['pending_payment']:,.0f}
Last payment date: {row.get('last_payment_date', 'unknown')}

Requirements:
- Under 70 words
- Respectful and reassuring tone (this is money owed to them, not from them)
- Confirm the amount and give an expected payment timeline
- End with "Regards," and leave the sender name blank
"""
    response = llm.invoke(prompt)
    return response.content


def run():
    print("\n" + "=" * 60)
    print("ARTISAN PAYMENT AGENT")
    print("=" * 60 + "\n")

    # Step 1: find artisans who are owed money
    pending = load_pending_payments(ARTISANS_FILE)

    if pending.empty:
        print("✅ No pending artisan payments. Everyone is paid up.")
        return

    notices = []

    # Step 2: draft one message per artisan with a pending payment
    for _, row in pending.iterrows():
        print(f"💰 Drafting payment notice for: {row['artisan_name']}")
        message_text = draft_payment_message(row)
        notices.append(
            f"Artisan: {row['artisan_name']} ({row['work_type']})\n"
            f"Pending: ₹{row['pending_payment']:,.0f} | Contact: {row.get('contact_number', 'n/a')}\n\n"
            f"{message_text}\n"
            + "-" * 60
        )

    # Step 3: save all notices to a single file for review before sending
    output = "\n\n".join(notices)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"\n✅ {len(pending)} payment notice(s) drafted and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
