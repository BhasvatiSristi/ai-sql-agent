import pandas as pd
import sqlite3
import os

if os.path.exists("olist.db"):
    print("Database already exists")
    exit()

print("Building database...")

files = {
    "olist_orders_dataset":
        "https://drive.google.com/uc?export=download&id=1K5VxzC9xicBYE7PIxFRUSEc2k4ljowNC",
    "olist_products_dataset":
        "https://drive.google.com/uc?export=download&id=1QsdJXSi2Xuf9hSk2zoRYn0HDXRiKHR_p",
    "olist_order_items_dataset":
        "https://drive.google.com/uc?export=download&id=1YBugkkeSUxdnyJ8XwiVbU9qwzKEtCN5F",
    "olist_order_payments_dataset":
        "https://drive.google.com/uc?export=download&id=1eWf0YUoeafabWbm_9pcuJM7NOEDVAH98",
    "olist_order_reviews_dataset":
        "https://drive.google.com/uc?export=download&id=1BSX-yhQXk8chqLDN7dWlivOsG3bXR-Zb",
    "olist_customers_dataset":
        "https://drive.google.com/uc?export=download&id=1o8agr-ZQQNfgtDkJqNJWMl3I-5aCYxzE",
    "olist_sellers_dataset":
        "https://drive.google.com/uc?export=download&id=1Ma4y_H0Jh3RHUDk7Nzqt6vUart9-fhdb",
    "olist_geolocation_dataset":
        "https://drive.google.com/uc?export=download&id=1kyJXRIek-tMaDxq59oyF3f1t3-qR5hkL"
}



conn = sqlite3.connect("olist.db")

for table, url in files.items():
    print("Loading", table)
    df = pd.read_csv(url)
    df.to_sql(table, conn, if_exists="replace", index=False)

conn.close()
print("Database created")
