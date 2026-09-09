"""
Inventory Reorder Agent
------------------------
Reads inventory.csv, finds products below their reorder level, and uses
Groq (Llama 3.3 70B via LangChain) to draft a supplier reorder email for
each low-stock item. Drafts are saved to reorder_emails.txt.

Companion to agrawal_report_agent.py — that agent handles executive
reporting, this one handles the operational follow-up: turning a low
stock alert straight into a ready-to-send supplier email.

Expected inventory.csv columns:
    product_name, current_stock, reorder_level, supplier_name, supplier_email
"""

from langchain_groq import ChatGroq
from dotenv import load_dotenv
import pandas as pd
import datetime
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

INVENTORY_FILE = "inventory.csv"
OUTPUT_FILE = "reorder_emails.txt"


def load_low_stock(path: str) -> pd.DataFrame:
    inventory = pd.read_csv(path)
    return inventory[inventory["current_stock"] < inventory["reorder_level"]]


def draft_reorder_email(row: pd.Series) -> str:
    prompt = f"""You are a purchasing manager at an Indian manufacturing company.

Write a short, professional reorder email to a supplier.

Product: {row['product_name']}
Current stock: {row['current_stock']} units
Reorder level: {row['reorder_level']} units
Supplier: {row.get('supplier_name', 'Supplier')}

Requirements:
- Under 100 words
- Polite but urgent tone
- Ask for a quote and earliest delivery date
- End with "Regards," and leave the sender name blank
"""
    response = llm.invoke(prompt)
    return response.content


def run():
    print("\n" + "=" * 60)
    print("INVENTORY REORDER AGENT")
    print("=" * 60 + "\n")

    low_stock = load_low_stock(INVENTORY_FILE)

    if low_stock.empty:
        print("✅ All products are above their reorder level. Nothing to do.")
        return

    today = datetime.date.today().strftime("%d %B %Y")
    emails = []

    for _, row in low_stock.iterrows():
        print(f"📦 Drafting reorder email for: {row['product_name']}")
        email_text = draft_reorder_email(row)
        emails.append(
            f"To: {row.get('supplier_email', 'supplier@example.com')}\n"
            f"Subject: Reorder Request — {row['product_name']} ({today})\n\n"
            f"{email_text}\n"
            + "-" * 60
        )

    output = "\n\n".join(emails)

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print(f"\n✅ {len(low_stock)} reorder email(s) drafted and saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
