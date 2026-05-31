from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from typing import Optional

app = FastAPI(
    title="Rajasthan Business AI API",
    description="Real-time business insights for manufacturing businesses",
    version="1.0.0"
)

# ── Data Models ────────────────────────────────────
class PredictionRequest(BaseModel):
    buyer_name: str
    product_name: str
    quantity: int

class EmailRequest(BaseModel):
    buyer_name: str
    fabric_type: str
    quantity: int
    tone: Optional[str] = "Professional"

# ── Endpoints ──────────────────────────────────────
@app.get("/")
def home():
    return {
        "message": "Rajasthan Business AI API",
        "built_by": "Sarthak Lohiya",
        "endpoints": [
            "/top-buyers",
            "/pending-orders",
            "/low-stock",
            "/monthly-revenue",
            "/docs"
        ]
    }

@app.get("/top-buyers")
def top_buyers():
    df = pd.read_csv("orders.csv")
    result = df.groupby("buyer_name")["order_value"]\
               .sum()\
               .sort_values(ascending=False)\
               .head(5)\
               .reset_index()\
               .to_dict(orient="records")
    return {"top_buyers": result}

@app.get("/pending-orders")
def pending_orders():
    df = pd.read_csv("orders.csv")
    pending = df[df["status"] == "pending"]\
              [["buyer_name","product_name",
                "order_value","order_date"]]\
              .to_dict(orient="records")
    return {
        "count": len(pending),
        "pending_orders": pending
    }

@app.get("/low-stock")
def low_stock():
    df = pd.read_csv("inventory.csv")
    low = df[df["current_stock"] < df["reorder_level"]].copy()
    low["units_needed"] = low["reorder_level"] - low["current_stock"]
    result = low[["product_name","current_stock",
                  "reorder_level","units_needed"]]\
             .to_dict(orient="records")
    return {
        "alert_count": len(result),
        "low_stock_items": result
    }

@app.get("/monthly-revenue")
def monthly_revenue():
    df = pd.read_csv("orders.csv")
    df["month"] = pd.to_datetime(df["order_date"]).dt.month_name()
    result = df.groupby("month")["order_value"]\
               .sum()\
               .reset_index()\
               .to_dict(orient="records")
    return {"monthly_revenue": result}

@app.post("/predict-churn")
def predict_churn(req: PredictionRequest):
    # Simple rule-based churn predictor
    # In real version this calls your sklearn model
    days_since_order = 45  # from your data
    risk = "HIGH" if days_since_order > 60 else \
           "MEDIUM" if days_since_order > 30 else "LOW"
    return {
        "buyer": req.buyer_name,
        "churn_risk": risk,
        "days_since_last_order": days_since_order,
        "recommendation": "Send follow-up immediately" \
                          if risk == "HIGH" else "Monitor"
    }