import pandas as pd

# Load data
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')
inventory = pd.read_csv('inventory.csv')

print("=" * 50)
print("BUSINESS INTELLIGENCE REPORT")
print("Rajasthan Manufacturing Business")
print("=" * 50)

# 1. Top buyers
print("\n📊 TOP BUYERS BY REVENUE:")
revenue = orders.groupby('buyer_name')['order_value'].sum()
print(revenue.sort_values(ascending=False))

# 2. Pending orders
print("\n⏳ PENDING ORDERS:")
pending = orders[orders['status']=='pending']
pending = pending.copy()
pending['order_date'] = pd.to_datetime(pending['order_date'])
pending['days_pending'] = (pd.Timestamp.now() - pending['order_date']).dt.days
print(pending[['buyer_name','order_value','days_pending']])

# 3. Monthly revenue
print("\n📅 MONTHLY REVENUE:")
orders['month'] = pd.to_datetime(orders['order_date']).dt.month_name()
monthly = orders.groupby('month')['order_value'].sum()
print(monthly)

# 4. Low stock alert
print("\n🚨 LOW STOCK ALERT:")
low = inventory[inventory['current_stock'] < inventory['reorder_level']]
low = low.copy()
low['units_needed'] = low['reorder_level'] - low['current_stock']
print(low[['product_name','current_stock','reorder_level','units_needed']])

# 5. Merge orders + products
print("\n💰 PROFIT ANALYSIS:")
merged = pd.merge(orders, products, on='product_name', how='left')
merged['profit'] = (merged['selling_price'] - merged['cost_price']) * merged['quantity']
profit = merged.groupby('product_name')['profit'].sum()
print(profit.sort_values(ascending=False))