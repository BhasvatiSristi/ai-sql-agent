import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from openai import OpenAI
import os

import setup_db


client = OpenAI()

SYSTEM_PROMPT = """
You are a professional AI SQL Agent for an e-commerce analytics system.

IMPORTANT BUSINESS LOGIC:
- Revenue = price + freight_value
- Only count orders where order_status = 'delivered'

DATABASE:
olist_orders_dataset(order_id, customer_id, order_status, order_purchase_timestamp)
olist_customers_dataset(customer_id,customer_city, customer_state)
olist_order_items_dataset(order_id, product_id, price, freight_value)
olist_products_dataset(product_id, product_category_name)

RULES:
- Only generate SELECT queries
- Never modify data
- Use correct joins
- Use GROUP BY
- Use LIMIT

OUTPUT FORMAT:
SQL_QUERY:
<sql>
ANSWER:
<plain English>
"""

def ask_llm(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

def run_sql(sql):
    conn = sqlite3.connect("olist.db")
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

st.set_page_config(page_title="AI Data Analyst", layout="wide")

st.title("🧠 AI Data Analyst — SQL Agent")
st.write("Ask questions about the e-commerce data in natural language")

question = st.text_input("Ask your data question:")

if st.button("Run Query"):
    if question:
        llm_output = ask_llm(question)

        sql = llm_output.split("SQL_QUERY:")[1].split("ANSWER:")[0]
        sql = sql.replace("```sql", "").replace("```", "").strip()

        answer = llm_output.split("ANSWER:")[1]

        df = run_sql(sql)

        st.subheader("Result")
        st.dataframe(df)

        st.subheader("Generated SQL")
        st.code(sql)