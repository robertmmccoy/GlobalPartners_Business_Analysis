import streamlit as st
from utils.athena import run_query

st.set_page_config(
    page_title="GlobalPartners Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- Sidebar – Global Filters ----------------
st.sidebar.title("Global Filters")

date_range = st.sidebar.date_input("Date Range", [], key="global_date_range")

restaurants = run_query("""
    SELECT DISTINCT restaurant_id
    FROM globalpartners_gold.restaurant_performance
""")
restaurant_filter = st.sidebar.multiselect(
    "Restaurants",
    restaurants["restaurant_id"].tolist(),
    key="global_restaurant_filter"
)

categories = run_query("""
    SELECT DISTINCT item_category
    FROM globalpartners_gold.menu_category_performance
""")
category_filter = st.sidebar.multiselect(
    "Menu Categories",
    categories["item_category"].tolist(),
    key="global_category_filter"
)

loyalty = run_query("""
    SELECT DISTINCT loyalty_flag
    FROM globalpartners_gold.loyalty_impact
""")
loyalty_filter = st.sidebar.multiselect(
    "Loyalty Status",
    loyalty["loyalty_flag"].tolist(),
    key="global_loyalty_filter"
)

# ---------------- Home ----------------
st.title("GlobalPartners Analytics Dashboard")
st.write("High-level view of sales, customers, loyalty, and discounts.")

daily = run_query("""
    SELECT
        SUM(total_revenue) AS total_revenue,
        SUM(total_orders) AS total_orders,
        AVG(avg_order_value) AS avg_order_value
    FROM globalpartners_gold.sales_daily
""")

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${daily['total_revenue'][0]:,.2f}")
col2.metric("Total Orders", f"{daily['total_orders'][0]:,}")
col3.metric("Avg Order Value", f"${daily['avg_order_value'][0]:.2f}")

st.write("---")
st.write("Use the sidebar pages to explore:")
st.write("- Sales Trends & Seasonality")
st.write("- Category & Restaurant Performance")
st.write("- Customer Segmentation (RFM)")
st.write("- CLV (Segments & Daily)")
st.write("- Loyalty Program Impact")
st.write("- Discount Effectiveness")
st.write("- Churn Indicators")
