import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Sales Trends & Seasonality")

# ---------------- Weekly Sales ----------------
weekly = run_query("""
    SELECT
        year,
        week,
        total_orders,
        total_revenue,
        avg_order_value
    FROM globalpartners_gold.sales_weekly
""")

st.subheader("Weekly Revenue Trend")
weekly_chart = alt.Chart(weekly).mark_line(point=True).encode(
    x=alt.X("week:O", title="Week"),
    y=alt.Y("total_revenue:Q", title="Total Revenue"),
    color="year:N",
    tooltip=["year", "week", "total_orders", "total_revenue", "avg_order_value"]
)

st.altair_chart(weekly_chart, use_container_width=True)

# ---------------- KPIs ----------------
c1, c2, c3 = st.columns(3)
c1.metric("Avg Weekly Revenue", f"${weekly['total_revenue'].mean():,.2f}")
c2.metric("Avg Weekly Orders", f"{weekly['total_orders'].mean():,.0f}")
c3.metric("Avg Order Value", f"${weekly['avg_order_value'].mean():.2f}")

# ---------------- Table ----------------
st.subheader("Weekly Sales Data")
st.dataframe(weekly)
