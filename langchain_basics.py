from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv
import os


load_dotenv()

# ── Initialize model ───────────────────────────────
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)

# ── Chain 1: Email Generator ───────────────────────
email_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a professional email writer 
     for Indian textile exporters. Write concise 
     emails under 100 words."""),
    ("human", """Write a {tone} follow-up email to 
     {buyer} about {quantity} meters of {fabric}. 
     Include a call to action.""")
])

email_chain = email_prompt | llm | StrOutputParser()

# Test email chain
email = email_chain.invoke({
    "tone": "professional",
    "buyer": "Sharma Exports",
    "quantity": 500,
    "fabric": "Silk Dupatta"
})
print("EMAIL GENERATED:")
print(email)
print("\n" + "="*50 + "\n")

# ── Chain 2: Business Insight Generator ───────────
insight_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a business analyst for 
     Indian manufacturing companies. Provide brief, 
     actionable insights in 3 bullet points."""),
    ("human", """Analyze this business data and give 
     insights:
     
     Top buyer: {top_buyer} - ₹{revenue}
     Pending orders: {pending_count} orders
     Low stock items: {low_stock}
     Best month: {best_month}
     
     What should this business owner do this week?""")
])

insight_chain = insight_prompt | llm | StrOutputParser()

insights = insight_chain.invoke({
    "top_buyer": "Sharma Exports",
    "revenue": "128,000",
    "pending_count": 3,
    "low_stock": "Silk Dupatta, Wool Shawl",
    "best_month": "February"
})
print("BUSINESS INSIGHTS:")
print(insights)
print("\n" + "="*50 + "\n")


# ── Chain 3: Manual conversation history ──────────
print("CONVERSATION WITH MEMORY:")

history = []

def chat(user_input):
    history.append(HumanMessage(content=user_input))
    response = llm.invoke(history)
    history.append(AIMessage(content=response.content))
    return response.content

r1 = chat("My top buyer is Sharma Exports with ₹1,28,000 revenue")
print(f"Bot: {r1}\n")

r2 = chat("They have 2 pending orders. Should I follow up?")
print(f"Bot: {r2}\n")

r3 = chat("What did I tell you about my top buyer?")
print(f"Bot: {r3}")