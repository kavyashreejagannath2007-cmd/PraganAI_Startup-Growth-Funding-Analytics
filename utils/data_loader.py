from pathlib import Path
import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    base_dir = Path(__file__).resolve().parent.parent
    csv_path = base_dir / "data" / "startup_data.csv"

    return pd.read_csv(csv_path)
