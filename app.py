from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "Rajasthan Business AI API",
        "status": "running",
        "built_by": "Sarthak Lohiya"
    })

@app.route('/top-buyers')
def top_buyers():
    df = pd.read_csv('orders.csv')
    result = df.groupby('buyer_name')['order_value']\
               .sum()\
               .sort_values(ascending=False)\
               .head(5)\
               .to_dict()
    return jsonify(result)

@app.route('/pending-orders')
def pending():
    df = pd.read_csv('orders.csv')
    pending = df[df['status']=='pending']\
              [['buyer_name','order_value','order_date']]\
              .to_dict(orient='records')
    return jsonify(pending)

@app.route('/low-stock')
def low_stock():
    df = pd.read_csv('inventory.csv')
    low = df[df['current_stock'] < df['reorder_level']]\
          [['product_name','current_stock','reorder_level']]\
          .to_dict(orient='records')
    return jsonify(low)

if __name__ == '__main__':
    app.run(debug=True, port=5000)