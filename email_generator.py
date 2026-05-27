import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

def generate_email(buyer, fabric, quantity, tone):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "meta-llama/llama-4-scout-17b-16e-instruct",
        "messages": [
            {"role": "system", "content": "You are a professional email writer for Indian textile exporters. Write concise, professional emails under 100 words."},
            {"role": "user", "content": f"Write a {tone} follow-up email to {buyer} who enquired about {quantity} meters of {fabric}. Include a clear call to action."}
        ],
        "max_tokens": 200
    }
    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if "choices" not in data:
        error_msg = data.get("error", {}).get("message", str(data))
        st.error(f"API Error: {error_msg}")
        st.stop()
    return data["choices"][0]["message"]["content"]

st.set_page_config(page_title="AI Email Generator", page_icon="✉️")
st.title("✉️ AI Email Generator")
st.subheader("For Textile Exporters — Rajasthan")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    buyer = st.text_input("Buyer Name", placeholder="e.g. Sharma Exports")
    fabric = st.text_input("Fabric Type", placeholder="e.g. Silk Dupatta")
with col2:
    quantity = st.number_input("Quantity (meters)", min_value=1, value=100)
    tone = st.selectbox("Email Tone", ["Professional", "Friendly", "Urgent", "Formal"])

if st.button("Generate Email ✨", type="primary"):
    if buyer and fabric:
        with st.spinner("Generating email..."):
            email = generate_email(buyer, fabric, quantity, tone)
        st.markdown("---")
        st.subheader("Generated Email:")
        st.text_area("", email, height=200)
        st.success("✅ Email generated!")
        st.code(email)
    else:
        st.error("Please fill in Buyer Name and Fabric Type")

st.markdown("---")
st.caption("Built by Sarthak Lohiya — AI Solutions Consultant")
