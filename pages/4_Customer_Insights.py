import streamlit as st
import altair as alt
from utils.athena import run_query

st.title("Customer Segmentation – RFM")

# Load RFM data
df = run_query("""
    SELECT
        user_id,
        last_order_date,
        frequency,
        monetary,
        recency_days,
        rfm_segment
    FROM globalpartners_gold.customer_rfm
""")

# Handle empty dataset gracefully
if df.empty:
    st.warning("No RFM data available. Please verify your ETL job or table contents.")
    st.stop()

# Format monetary values
df["monetary"] = df["monetary"].round(2)

# KPIs
c1, c2, c3 = st.columns(3)
c1.metric("Avg Recency (days)", f"{df['recency_days'].mean():.1f}")
c2.metric("Avg Frequency", f"{df['frequency'].mean():.1f}")
c3.metric("Avg Monetary", f"${df['monetary'].mean():,.2f}")

# Scatter plot: Frequency vs Monetary
st.subheader("Frequency vs Monetary Value")

scatter = (
    alt.Chart(df)
    .mark_circle(size=70)
    .encode(
        x=alt.X("frequency:Q", title="Frequency"),
        y=alt.Y("monetary:Q", title="Monetary ($)"),
        color=alt.Color("rfm_segment:N", title="RFM Segment"),
        tooltip=[
            "user_id",
            "frequency",
            alt.Tooltip("monetary:Q", format="$.2f"),
            "recency_days",
            "rfm_segment"
        ]
    )
)

st.altair_chart(scatter, use_container_width=True)

# Display table
st.subheader("Customer-Level RFM Data")

df_display = df.copy()
df_display["monetary"] = df_display["monetary"].apply(lambda x: f"${x:,.2f}")

st.dataframe(df_display)
