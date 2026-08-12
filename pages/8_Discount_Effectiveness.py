import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Pricing & Discount Effectiveness")

# Load discount effectiveness data using actual Athena columns
df = run_query("""
    SELECT
        is_discounted,
        total_orders,
        total_revenue,
        discount_type,
        avg_order_value,
        total_revenue_all,
        total_orders_all,
        conversion_rate,
        revenue_share
    FROM globalpartners_gold.discount_effectiveness
""")

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Avg Conversion Rate", f"{df['conversion_rate'].mean():.2%}")
c2.metric("Avg Revenue Share", f"{df['revenue_share'].mean():.2%}")
c3.metric("Avg Order Value", f"${df['avg_order_value'].mean():.2f}")

# Bar chart: Revenue by Discount Type
st.subheader("Revenue by Discount Type")
rev_chart = alt.Chart(df).mark_bar().encode(
    x="discount_type:N",
    y="total_revenue:Q",
    color="discount_type:N",
    tooltip=[
        "discount_type",
        "total_orders",
        "total_revenue",
        "avg_order_value",
        "conversion_rate",
        "revenue_share"
    ]
)

st.altair_chart(rev_chart, use_container_width=True)

# Scatter plot: Conversion Rate vs Revenue Share
st.subheader("Conversion Rate vs Revenue Share")
scatter = alt.Chart(df).mark_circle(size=70).encode(
    x=alt.X("conversion_rate:Q", title="Conversion Rate"),
    y=alt.Y("revenue_share:Q", title="Revenue Share"),
    color="discount_type:N",
    tooltip=[
        "discount_type",
        "conversion_rate",
        "revenue_share",
        "total_orders",
        "total_revenue"
    ]
)

st.altair_chart(scatter, use_container_width=True)

# Table
st.subheader("Discount Effectiveness Details")
st.dataframe(df)
