import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Loyalty Program Impact")

# Load loyalty impact data using actual Athena column names
df = run_query("""
    SELECT
        user_id,
        total_orders,
        total_revenue,
        loyalty_orders,
        loyalty_revenue,
        loyalty_flag,
        loyalty_ratio,
        loyalty_lift
    FROM globalpartners_gold.loyalty_impact
""")

# KPIs
c1, c2 = st.columns(2)

# Total loyalty revenue
loyal_rev = df.loc[df["loyalty_flag"] == "LOYALTY", "loyalty_revenue"].sum()
c1.metric("Total Loyalty Revenue", f"${loyal_rev:,.2f}")

# Total non-loyalty revenue
non_loyal_rev = df.loc[df["loyalty_flag"] != "LOYALTY", "total_revenue"].sum()
c2.metric("Total Non-Loyalty Revenue", f"${non_loyal_rev:,.2f}")

# Bar chart: Loyalty vs Non-Loyalty revenue
st.subheader("Revenue Comparison")
chart = alt.Chart(df).mark_bar().encode(
    x="loyalty_flag:N",
    y="total_revenue:Q",
    tooltip=[
        "loyalty_flag",
        "total_orders",
        "total_revenue",
        "loyalty_orders",
        "loyalty_revenue",
        "loyalty_ratio",
        "loyalty_lift"
    ]
)

st.altair_chart(chart, use_container_width=True)

# Table
st.subheader("Loyalty Impact Details")
st.dataframe(df)
