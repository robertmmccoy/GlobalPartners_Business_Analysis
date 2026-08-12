import streamlit as st
from utils.athena import run_query

st.title("Executive Summary")

rev = run_query("""
    SELECT SUM(total_revenue) AS rev
    FROM globalpartners_gold.sales_daily
""")["rev"][0]

orders = run_query("""
    SELECT SUM(total_orders) AS orders
    FROM globalpartners_gold.sales_daily
""")["orders"][0]

st.write(f"**Total Revenue:** ${rev:,.2f}")
st.write(f"**Total Orders:** {orders:,}")

st.write("""
### Key Insights
- CLV, RFM, and loyalty metrics support targeted marketing and retention.
- Restaurant and category performance highlight where revenue is concentrated.
- Time-series views show seasonality and growth patterns.
- Discount effectiveness and churn indicators support pricing and re-engagement strategies.
""")
