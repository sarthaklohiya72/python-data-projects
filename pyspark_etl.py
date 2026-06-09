import pandas as pd
import random, os

random.seed(42)
products = ["Copper Coil 3mm", "Brass Sheet 2mm", "Copper Rod 5mm", "Brass Tube 10mm"]
buyers   = ["Sharma Textiles", "Gupta Traders", "Rajasthan Hardware", "Delhi Metals", "Jaipur Tools"]
statuses = ["delivered", "pending", "in_transit"]

data = [{
    "order_id"   : f"ORD{i+1:04d}",
    "product"    : random.choice(products),
    "buyer"      : random.choice(buyers),
    "quantity"   : random.randint(1, 50),
    "order_value": round(random.uniform(5000, 80000), 2),
    "status"     : random.choice(statuses),
    "month"      : random.randint(1, 12)
} for i in range(1000)]

df = pd.DataFrame(data)
print(f"Dataset: {len(df)} orders loaded\n")

print("--- Revenue by Product ---")
print(df.groupby("product")["order_value"].agg(["sum","count","mean"]).sort_values("sum", ascending=False).to_string())

print("\n--- Pending Orders by Buyer ---")
print(df[df["status"]=="pending"].groupby("buyer")["order_value"].agg(["sum","count"]).sort_values("sum", ascending=False).to_string())

print("\n--- Priority Flags ---")
df["priority"] = pd.cut(df["order_value"], bins=[0,25000,50000,float("inf")], labels=["LOW","MEDIUM","HIGH"])
print(df["priority"].value_counts().to_string())

os.makedirs("data_output", exist_ok=True)
df.to_csv("data_output/orders_processed.csv", index=False)
print(f"\n✅ ETL Complete — data_output/orders_processed.csv written")
print(f"Total Revenue: ₹{df['order_value'].sum():,.0f}")