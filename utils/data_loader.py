import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    """
    Load the startup dataset.
    """
    df = pd.read_csv("data/startup_data.csv")
    return df


@st.cache_data
def load_filtered_data(industry=None, region=None):

    df = load_data()

    if industry:
        df = df[df["Industry"].isin(industry)]

    if region:
        df = df[df["Region"].isin(region)]

    return df


def get_numeric_columns():
    return [
        "Funding Rounds",
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]
