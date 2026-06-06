from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

# Create fake SAP export
df = pd.DataFrame({
    "Order_ID": ["ORD001", "ORD002", "ORD003"],
    "Customer": ["Raj Traders", "Mehta Exports", "Singh & Co"],
    "Product": ["Brass Rod", "Copper Sheet", "Brass Fitting"],
    "Quantity_Tons": [45, 120, 30],
    "Status": ["Delivered", "Pending", "In Transit"],
    "Amount_INR": [2250000, 6000000, 1500000]
})
df.to_csv("sap_export.csv", index=False)
sap_data = df.to_string(index=False)

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)

prompt = ChatPromptTemplate.from_template("""
Tum ek SAP data assistant ho. Niche diya gaya data use karke question ka jawab do.
Same language mein jawab do jisme question pucha gaya hai.

SAP Data:
{data}

Question: {question}
""")

chain = prompt | llm | StrOutputParser()

questions = [
    "Kaun sa order abhi bhi pending hai?",
    "Mehta Exports ka order kitne tons ka tha?",
    "Sabse zyada amount ka order kiska hai?"
]

print("=== SAP Export Q&A Agent (Hindi) ===\n")
for q in questions:
    print(f"Q: {q}")
    print(f"A: {chain.invoke({'data': sap_data, 'question': q})}\n")
