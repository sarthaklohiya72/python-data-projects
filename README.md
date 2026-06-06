# Python Data Projects — Sarthak Lohiya

AI, data, and automation projects built for Indian manufacturing businesses.
Part of a 6-month compressed roadmap to build an AI consulting business targeting
SME manufacturers in Rajasthan and Delhi NCR.

**Built by:** Sarthak Lohiya — BTech CS (AI), Poornima College of Engineering, Jaipur  
**GitHub:** github.com/sarthaklohiya72  
**LinkedIn:** linkedin.com/in/sarthak-lohiya-6a8675275

---

## Tech Stack

- **Language:** Python 3.12 (Anaconda)
- **AI/LLM:** Groq API — llama-3.3-70b-versatile (free)
- **Agentic:** LangChain, LangGraph, AutoGen
- **ML:** scikit-learn, XGBoost, pandas
- **APIs:** Flask, FastAPI
- **UI:** Streamlit
- **Database:** MySQL (rajasthan_business_db)
- **Automation:** Make.com
- **Visualization:** Tableau Public

---

## Projects

### 1. Pandas Business Intelligence Report
**File:** `pandas_analysis.py`  
Exports MySQL data to CSV and generates business insights using pandas.
- Top buyers by revenue
- Pending orders analysis
- Low stock alerts
- Profit analysis

---

### 2. Machine Learning Models
**Files:** `ml_models/`

| Model | Purpose |
|-------|---------|
| Linear Regression | Revenue prediction |
| Logistic Regression | Churn classification |
| Decision Tree | Churn classification |
| K-Means Clustering | Buyer segmentation |
| XGBoost | Churn prediction |

**Streamlit UI:** `churn_app.py` — live churn predictor with form input

---

### 3. AI Email Generator
**File:** `email_generator.py`  
Generates professional buyer follow-up emails for textile exporters using Groq API + Streamlit UI.

---

### 4. Flask REST API
**File:** `app.py`  
4 endpoints serving live business data as JSON:
- `GET /` — health check
- `GET /top-buyers` — top buyers by revenue
- `GET /pending-orders` — all pending orders
- `GET /low-stock` — products below reorder level

---

### 5. FastAPI App
**File:** `fastapi_app.py`  
5 endpoints with Pydantic models and auto-docs at `/docs`:
- Includes `/predict-churn` endpoint
- Auto-generated Swagger UI

---

### 6. LangChain AI Chains
**File:** `langchain_basics.py`  
- Email generator chain
- Business insight chain
- Conversation with memory
- All using Groq API

---

### 7. LangGraph Autonomous Agent
**File:** `langgraph_agent.py`  
Autonomous 3-node workflow that generates a weekly business report with zero human input:

collect_data → analyze_data → generate_report

Uses Groq + pandas CSV data.

---

### 8. AutoGen Multi-Agent System
**File:** `autogen_agent.py`  
Microsoft AutoGen 2-agent conversation system:
- **BusinessAnalyst** — identifies top 3 problems in business data
- **ActionPlanner** — creates 3-step action plan with timelines and rupee impact
- **FactoryOwner** (UserProxy) — receives recommendations automatically
- Uses Groq via OpenAI-compatible endpoint

---

### 9. Agrawal Metal Works — Weekly Report Agent
**File:** `agrawal_report_agent.py`  
LangGraph 3-agent system built specifically for a real copper/brass manufacturer in Bhiwadi, Rajasthan:
- **Operations Agent** — analyzes factory risks and inventory
- **Sales Agent** — finds revenue opportunities and client priorities
- **Report Agent** — writes executive summary in under 2 minutes
- Report auto-saved to `.txt` file every week

Previously took a manager 2 hours every Monday.
Now takes 2 minutes. **100 minutes saved per week.**

---

### 10. Make.com Automations
3 live automations running for manufacturing businesses:
1. **Low Stock Alert** — Google Sheets → Filter → Gmail alert
2. **AI Email Generator** — Google Forms → Groq AI → Gmail Draft
3. **Meeting Reminder** — Google Sheets → Email reminder

---

### 11. Rajasthan Manufacturing Analytics Dashboard (Tableau)
URL:-
https://public.tableau.com/app/profile/sarthak.lohiya/viz/Rajasthan-Manufacturing-Dashboard/Dashboard1?publish=yes

---

## Database

**`rajasthan_business_db`** — MySQL database with 8 tables:
`orders`, `products`, `inventory`, `customers`, `clients`, `artisans`, `production`, `followups`

Real Indian business names. Used as foundation for all projects above.

---

## Folder Structure
python-data-projects/
├── pandas_analysis.py
├── email_generator.py
├── app.py                    # Flask API
├── fastapi_app.py
├── langchain_basics.py
├── langgraph_agent.py
├── autogen_agent.py
├── agrawal_report_agent.py
├── churn_app.py              # Streamlit UI
├── ml_models/
│   ├── linear_regression.py
│   ├── logistic_regression.py
│   ├── decision_tree.py
│   ├── kmeans_clustering.py
│   └── xgboost_churn.py
├── data/
│   ├── orders.csv
│   ├── inventory.csv
│   └── clients.csv
└── README.md
---

## Setup

```bash
git clone https://github.com/sarthaklohiya72/python-data-projects
cd python-data-projects
pip install -r requirements.txt
```

Create `.env` file:
GROQ_API_KEY=your_groq_api_key

---

## About

Building AI consulting services for small and medium manufacturers in Rajasthan.
Target industries: Textile, Marble, Handicraft, Copper/Brass.

*Day 17 of 180 — 4 June 2026*