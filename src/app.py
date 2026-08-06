"""Streamlit dashboard for Google Search Console data."""

import plotly.express as px
import streamlit as st

from ingest import load_csv, parse_ctr, rename_columns
from transform import add_rolling_average, aggregate_monthly


@st.cache_data
def load_data():
    """Load and clean the daily Search Console export."""
    return parse_ctr(rename_columns(load_csv("Graf.csv")))


st.set_page_config(page_title="Search Console Dashboard", layout="wide")
st.title("Search Console Dashboard")

df = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Clicks", f"{df['Clicks'].sum():,}")
col2.metric("Impressions", f"{df['Impressions'].sum():,}")
col3.metric("CTR", f"{df['Clicks'].sum() / df['Impressions'].sum():.2%}")
col4.metric("Avg position", f"{df['Position'].mean():.1f}")

st.subheader("Daily clicks")
daily = add_rolling_average(df)
st.plotly_chart(
    px.line(daily, x="Date", y=["Clicks", "ClicksRolling"]),
    width="stretch",
)

st.subheader("Monthly totals")
st.dataframe(aggregate_monthly(df), width="stretch")