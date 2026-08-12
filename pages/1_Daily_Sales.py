import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Sales Trends – Daily")

df = run_query("""
    SELECT order_date, total_orders, total_revenue, avg_order_value
    FROM globalpartners_gold.sales_daily
    ORDER BY order_date
""")

c1, c2, c3 = st.columns(3)
c1.metric("Total Revenue", f"${df['total_revenue'].sum():,.2f}")
c2.metric("Total Orders", f"{df['total_orders'].sum():,}")
c3.metric("Avg Order Value", f"${df['avg_order_value'].mean():.2f}")

chart = alt.Chart(df).mark_line().encode(
    x="order_date:T",
    y="total_revenue:Q",
    tooltip=["order_date", "total_revenue", "total_orders"]
)

st.altair_chart(chart, use_container_width=True)
st.dataframe(df)
