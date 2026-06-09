import os
import mysql.connector
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from datetime import datetime, timedelta

os.environ["GROQ_API_KEY"] = ""
os.environ["OPENAI_API_KEY"] = "fake-key"   # CrewAI requirement

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

# ── Step 1: Connect to MySQL ──────────────────────────────────
def get_pending_orders():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="rajasthan_business_db"
    )
    cursor = conn.cursor(dictionary=True)
    
    # Fetch orders pending for 7+ days
    cursor.execute("""
        SELECT 
            o.order_id,
            o.buyer_name,
            o.order_value,
            o.order_date,
            o.status,
            DATEDIFF(CURDATE(), o.order_date) AS days_pending
        FROM orders o
        WHERE o.status = 'pending'
          AND DATEDIFF(CURDATE(), o.order_date) >= 7
        ORDER BY o.order_value DESC
    """)
    
    orders = cursor.fetchall()
    conn.close()
    return orders

# ── Step 2: Classify urgency ──────────────────────────────────
def classify_urgency(order: dict) -> str:
    if order["days_pending"] >= 30 or order["order_value"] >= 50000:
        return "🔴 HIGH"
    elif order["days_pending"] >= 14 or order["order_value"] >= 25000:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"

# ── Step 3: Draft Hinglish WhatsApp message ───────────────────
def draft_whatsapp_message(order: dict, urgency: str) -> str:
    prompt = f"""
You are an assistant for Agrawal Metal Works, a copper/brass manufacturer in Bhiwadi, Rajasthan.

Draft a polite, professional WhatsApp message in Hinglish (mix of Hindi and English, casual but respectful) 
for a pending order follow-up.

Order details:
- Buyer: {order['buyer_name']}
- Order Value: ₹{order['order_value']:,}
- Days Pending: {order['days_pending']} days
- Urgency: {urgency}

Rules:
- Keep it under 3 sentences
- Be polite, not aggressive
- Use "ji" for respect
- End with a question to prompt reply
- No emojis except at start
"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content.strip()

# ── Step 4: Run the agent ─────────────────────────────────────
def run_followup_agent():
    print("="*60)
    print("AUTONOMOUS FOLLOW-UP AGENT — AGRAWAL METAL WORKS")
    print("="*60)
    
    pending_orders = get_pending_orders()
    
    if not pending_orders:
        print("✅ No pending orders found. All clear!")
        return
    
    print(f"\n📋 Found {len(pending_orders)} pending orders\n")
    
    messages_to_send = []
    
    for order in pending_orders:
        urgency = classify_urgency(order)
        message = draft_whatsapp_message(order, urgency)
        
        print(f"{'─'*50}")
        print(f"Order ID   : {order['order_id']}")
        print(f"Buyer      : {order['buyer_name']}")
        print(f"Value      : ₹{order['order_value']:,}")
        print(f"Pending    : {order['days_pending']} days")
        print(f"Urgency    : {urgency}")
        print(f"\nDrafted Message:")
        print(f"  {message}")
        
        messages_to_send.append({
            "order": order,
            "urgency": urgency,
            "message": message
        })
    
    print(f"\n{'='*60}")
    print(f"SUMMARY: {len(messages_to_send)} messages ready to send")
    
    total_value = sum(o["order"]["order_value"] for o in messages_to_send)
    print(f"Total Value at Risk: ₹{total_value:,}")
    
    print(f"\n⚠️  APPROVE ALL MESSAGES? (yes/no): ", end="")
    if input().strip().lower() == "yes":
        print("\n✅ Messages approved — would trigger WhatsApp API/Make.com here")
        for item in messages_to_send:
            print(f"  → Sent to: {item['order']['buyer_name']}")
    else:
        print("\n❌ Batch cancelled. Review individually.")

if __name__ == "__main__":
    run_followup_agent()