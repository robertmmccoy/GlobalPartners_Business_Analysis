import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Restaurant / Location Performance")

df = run_query("""
    SELECT restaurant_id, total_orders, total_revenue, avg_order_value
    FROM globalpartners_gold.restaurant_performance
""")

top_rest = df.sort_values("total_revenue", ascending=False).iloc[0]
st.metric("Top Restaurant by Revenue", top_rest["restaurant_id"])

chart = alt.Chart(df).mark_bar().encode(
    x="restaurant_id:N",
    y="total_revenue:Q",
    tooltip=["restaurant_id", "total_revenue", "total_orders", "avg_order_value"]
)

st.altair_chart(chart, use_container_width=True)
st.dataframe(df)
