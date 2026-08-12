import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Customer Churn Indicators")

df = run_query("""
    SELECT
        user_id,
        last_order_date,
        days_since_last_order,
        first_order_date,
        avg_gap_days,
        avg_pct_change_spend,
        total_spend,
        total_orders,
        churn_tag
    FROM globalpartners_gold.customer_churn_indicators
""")

if df.empty:
    st.warning("No churn data available.")
    st.stop()

# Format currency
df["total_spend"] = df["total_spend"].round(2)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Avg Days Since Last Order", f"{df['days_since_last_order'].mean():.1f}")
c2.metric("Avg Gap Between Orders (days)", f"{df['avg_gap_days'].mean():.1f}")
c3.metric("Avg Spend Change (%)", f"{df['avg_pct_change_spend'].mean():.2f}")

# Churn distribution chart
st.subheader("Churn Risk Distribution")
chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("churn_tag:N", title="Churn Category"),
        y=alt.Y("count():Q", title="Customers"),
        color="churn_tag:N"
    )
)
st.altair_chart(chart, use_container_width=True)

# Table
st.subheader("Customer-Level Churn Indicators")
st.dataframe(df)
