from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI(
    title="Churn Prediction API",
    description="Predict high value orders for manufacturing businesses"
)

with open("models/churn_model.pkl", "rb") as f:
    model = pickle.load(f)

class OrderInput(BaseModel):
    month: int
    quantity: int
    buyer_encoded: int

class PredictionOutput(BaseModel):
    prediction: str
    probability: float
    recommendation: str

@app.get("/")
def home():
    return {
        "service": "Churn Prediction API",
        "built_by": "Sarthak Lohiya",
        "status": "running"
    }

@app.post("/predict", response_model=PredictionOutput)
def predict(order: OrderInput):
    features = np.array([[order.month, order.quantity, order.buyer_encoded]])
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]
    return PredictionOutput(
        prediction="HIGH VALUE" if pred == 1 else "REGULAR",
        probability=round(float(prob), 3),
        recommendation="Prioritize this order" if pred == 1 else "Standard processing"
    )

@app.get("/health")
def health():
    return {"status": "healthy", "model": "loaded"}