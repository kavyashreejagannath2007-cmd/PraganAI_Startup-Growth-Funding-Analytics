import streamlit as st

from utils.data_loader import load_data
from utils.ml_modules import train_valuation_model

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

# Load dataset FIRST
df = load_data()

# Train model AFTER loading data
model, r2, mae = train_valuation_model(df)

st.title("🚀 Startup Growth & Funding Analytics")

st.success(f"Dataset Loaded: {len(df)} records")
st.info(f"Model Accuracy (R²): {r2:.2f}")
st.info(f"Mean Absolute Error: {mae:.2f}")

st.dataframe(df.head())
