from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
import pickle
import json
import os

# Load data
orders = pd.read_csv("orders.csv")

# Feature engineering
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["month"] = orders["order_date"].dt.month
orders["quantity"] = orders["quantity"].fillna(1)
orders["high_value"] = (orders["order_value"] > 40000).astype(int)

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
orders["buyer_encoded"] = le.fit_transform(orders["buyer_name"])

X = orders[["month","quantity","buyer_encoded"]].values
y = orders["high_value"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Save model
os.makedirs("models", exist_ok=True)
with open("models/churn_model.pkl", "wb") as f:
    pickle.dump(model, f)

# Save metrics
metrics = {
    "accuracy": round(accuracy, 4),
    "model": "RandomForest",
    "n_estimators": 100,
    "features": ["month", "quantity", "buyer_encoded"]
}

os.makedirs("metrics", exist_ok=True)
with open("metrics/metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print("="*50)
print("MODEL TRAINED AND SAVED")
print("="*50)
print(f"Accuracy: {accuracy:.2%}")
print(f"Model saved: models/churn_model.pkl")
print(f"Metrics saved: metrics/metrics.json")