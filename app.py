import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from openai import OpenAI

# -------------------------------
# OpenAI client (reads key from Streamlit Secrets)
# -------------------------------
client = OpenAI()

# -------------------------------
# SQL Agent System Prompt
# -------------------------------
SYSTEM_PROMPT = """
You are a professional AI SQL Agent for an e-commerce analytics system.

IMPORTANT BUSINESS LOGIC:
- Revenue = price + freight_value
- Only count orders where order_status = 'delivered'

DATABASE:
olist_orders_dataset(order_id, customer_id, order_status, order_purchase_timestamp)
olist_customers_dataset(customer_id, customer_city, customer_state)
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

# -------------------------------
# Helper functions
# -------------------------------
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


# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(page_title="AI Data Analyst", page_icon="📊", layout="wide")

st.title("🧠 AI Data Analyst Copilot")
st.write("Ask natural-language business questions and get instant insights from the e-commerce database.")

# -------------------------------
# Example Questions
# -------------------------------
st.subheader("Try one of these examples 👇")

examples = [
    "Top 5 product categories",
    "Monthly sales trend over time",
    "Top 10 sellers as per revenue",
    "Cities with highest number of customers",
    "Average order value?"
]

cols = st.columns(len(examples))
selected = None

for i, ex in enumerate(examples):
    if cols[i].button(ex):
        selected = ex

# -------------------------------
# User Input
# -------------------------------
question = st.text_input(
    "Or ask your own question:",
    value=selected if selected else ""
)

# -------------------------------
# Run Query
# -------------------------------
if st.button("Run Analysis"):
    if not question:
        st.warning("Please enter a question.")
    else:
        with st.spinner("Thinking like a data analyst..."):
            llm_output = ask_llm(question)

            # Extract SQL
            sql = llm_output.split("SQL_QUERY:")[1].split("ANSWER:")[0]
            sql = sql.replace("```sql", "").replace("```", "").strip()

            # Extract answer
            answer = llm_output.split("ANSWER:")[1].strip()

            # Run SQL
            df = run_sql(sql)

        # -------------------------------
        # Display Results
        # -------------------------------
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("🧾 Generated SQL")
            st.code(sql)

        with col2:
            st.subheader("🤖 AI Explanation")
            st.write(answer)

        st.subheader("📊 Query Result")
        st.dataframe(df)

        # -------------------------------
        # Auto Chart
        # -------------------------------
        if len(df.columns) >= 2 and df.shape[0] > 0:
            try:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1])
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass
