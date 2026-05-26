import pandas as pd
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Sarthak*123',
    database='rajasthan_business_db'
)

tables = ['orders','inventory','clients','customers','products']
for t in tables:
    df = pd.read_sql(f"SELECT * FROM {t}", conn)
    df.to_csv(f'{t}.csv', index=False)
    print(f"✅ {t}.csv exported — {len(df)} rows")

conn.close()
print("All done!")