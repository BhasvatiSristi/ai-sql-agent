import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from openai import OpenAI
import setup_db

client = OpenAI()

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
/* Page */
body {
    background-color: #0e1117;
    color: #e5e7eb;
}

/* Title */
.big-title {
    font-size: 40px;
    font-weight: 700;
    color: #e5e7eb;
}

/* Cards (SQL, Explanation, Results) */
.card {
    background-color: #161b22;
    padding: 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    border: 1px solid #30363d;
    box-shadow: 0 0 0 1px rgba(255,255,255,0.02);
}

/* Input box */
.stTextInput > div > div > input {
    background-color: #0d1117;
    color: #e5e7eb;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 10px;
}

/* Input focus glow */
.stTextInput > div > div > input:focus {
    border-color: #6366f1;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.3);
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #4f46e5);
    color: white;
    border-radius: 12px;
    padding: 10px 22px;
    border: none;
    font-weight: 600;
    box-shadow: 0 6px 18px rgba(79,70,229,0.4);
}

/* Button hover */
.stButton > button:hover {
    background: linear-gradient(135deg, #4f46e5, #4338ca);
    transform: translateY(-1px);
}

/* Data table */
.stDataFrame {
    background-color: #0d1117;
    border-radius: 12px;
    border: 1px solid #30363d;
}
</style>
""", unsafe_allow_html=True)




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

st.markdown("<div class='big-title'>🧠 SQL Agent</div>", unsafe_allow_html=True)
st.write("Ask business questions and get instant data insights")

question = st.text_input("Ask a question like:")

if st.button("Run Analysis"):
    with st.spinner("Thinking..."):
        llm_output = ask_llm(question)

        sql = llm_output.split("SQL_QUERY:")[1].split("ANSWER:")[0]
        sql = sql.replace("```sql", "").replace("```", "").strip()

        answer = llm_output.split("ANSWER:")[1]

        df = run_sql(sql)

        st.markdown("<div class='card'><h3>Query Result</h3></div>", unsafe_allow_html=True)
        st.dataframe(df)

        col1, col2 = st.columns([1,1])

        with col1:
            st.markdown("<div class='card'><h3>Generated SQL</h3></div>", unsafe_allow_html=True)
            st.code(sql)

        with col2:
            st.markdown("<div class='card'><h3>AI Explanation</h3></div>", unsafe_allow_html=True)
            st.write(answer)



        if len(df.columns) >= 2:
            fig = px.bar(df, x=df.columns[0], y=df.columns[1])
            st.plotly_chart(fig, use_container_width=True)
