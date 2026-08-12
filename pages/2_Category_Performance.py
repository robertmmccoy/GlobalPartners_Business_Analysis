import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Menu Category Performance")

df = run_query("""
    SELECT item_category, total_orders, total_revenue, avg_order_value
    FROM globalpartners_gold.menu_category_performance
""")

top_cat = df.sort_values("total_revenue", ascending=False).iloc[0]
st.metric("Top Category by Revenue", top_cat["item_category"])

chart = alt.Chart(df).mark_bar().encode(
    x="item_category:N",
    y="total_revenue:Q",
    tooltip=["item_category", "total_revenue", "total_orders", "avg_order_value"]
)

st.altair_chart(chart, use_container_width=True)
st.dataframe(df)
