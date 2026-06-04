import streamlit as st
import pandas as pd
import plotly.express as px

from utils.ml_modules import (
    train_valuation_model,
    predict_valuation,
    feature_importance
)

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Predictive Analytics",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Predictive Analytics")
st.markdown("Machine Learning based Startup Valuation Prediction")

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv("data/startup_data.csv")

# ----------------------------------
# Train Model
# ----------------------------------

model, r2_score, mae = train_valuation_model(df)

# ----------------------------------
# KPI Cards
# ----------------------------------

col1, col2, col3 = st.columns(3)

col1.metric(
    "📊 Dataset Size",
    len(df)
)

col2.metric(
    "🎯 Model Accuracy (R²)",
    f"{r2_score:.2f}"
)

col3.metric(
    "📉 Mean Absolute Error",
    f"{mae:.2f}"
)

st.divider()

# ----------------------------------
# Prediction Form
# ----------------------------------

st.subheader("🚀 Startup Valuation Predictor")

c1, c2 = st.columns(2)

with c1:

    funding_rounds = st.number_input(
        "Funding Rounds",
        min_value=1,
        max_value=20,
        value=5
    )

    funding_amount = st.number_input(
        "Funding Amount (M USD)",
        min_value=0.0,
        value=100.0
    )

    revenue = st.number_input(
        "Revenue (M USD)",
        min_value=0.0,
        value=50.0
    )

with c2:

    employees = st.number_input(
        "Employees",
        min_value=1,
        value=500
    )

    market_share = st.slider(
        "Market Share (%)",
        0.0,
        100.0,
        10.0
    )

st.divider()

# ----------------------------------
# Prediction Button
# ----------------------------------

if st.button("🔮 Predict Startup Valuation"):

    predicted_value = predict_valuation(
        model,
        funding_rounds,
        funding_amount,
        revenue,
        employees,
        market_share
    )

    st.success(
        f"Estimated Startup Valuation : ${predicted_value:,.2f} Million"
    )

# ----------------------------------
# Feature Importance
# ----------------------------------

st.subheader("📈 Feature Importance")

importance = feature_importance(model)

fig = px.bar(
    importance,
    x="Coefficient",
    y="Feature",
    orientation="h",
    title="ML Feature Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Actual vs Predicted Visualization
# ----------------------------------

st.subheader("📊 Startup Valuation Distribution")

fig = px.scatter(
    df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Funding vs Actual Valuation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Correlation Matrix
# ----------------------------------

st.subheader("🔥 Feature Correlation")

corr = df[
    [
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Funding Rounds",
        "Market Share (%)"
    ]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Sample Prediction Dataset
# ----------------------------------

st.subheader("📋 Sample Data")

st.dataframe(
    df.head(15),
    use_container_width=True
)

# ----------------------------------
# Footer
# ----------------------------------

st.info(
    "This prediction model uses Linear Regression based on Funding, Revenue, Employees, Market Share, and Funding Rounds."
)
