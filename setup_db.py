import pandas as pd
import sqlite3
import os

if os.path.exists("olist.db"):
    print("Database already exists")
    exit()

print("Building database...")

files = {
    "olist_orders_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_orders_dataset.csv",
    "olist_customers_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_customers_dataset.csv",
    "olist_order_items_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_order_items_dataset.csv",
    "olist_products_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_products_dataset.csv",
    "olist_order_payments_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_order_reviews_dataset.csv",
    "olist_sellers_dataset": "https://raw.githubusercontent.com/olistbr/brazilian-ecommerce/master/olist_sellers_dataset.csv",
}

conn = sqlite3.connect("olist.db")

for table, url in files.items():
    print("Loading", table)
    df = pd.read_csv(url)
    df.to_sql(table, conn, if_exists="replace", index=False)

conn.close()
print("Database created")
