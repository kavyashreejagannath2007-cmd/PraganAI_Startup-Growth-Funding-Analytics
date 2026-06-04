from utils.ml_modules import (
    train_valuation_model,
    predict_valuation,
    feature_importance
)

model, r2, mae = train_valuation_model(df)

st.sidebar.header("🤖 ML Predictor")

fr = st.sidebar.number_input(
    "Funding Rounds",
    min_value=1,
    max_value=20,
    value=5
)

fa = st.sidebar.number_input(
    "Funding Amount (M USD)",
    min_value=1.0,
    value=100.0
)

rev = st.sidebar.number_input(
    "Revenue (M USD)",
    min_value=1.0,
    value=50.0
)

emp = st.sidebar.number_input(
    "Employees",
    min_value=1,
    value=500
)

ms = st.sidebar.slider(
    "Market Share (%)",
    0.0,
    100.0,
    10.0
)

if st.sidebar.button("Predict Startup Valuation"):
    result = predict_valuation(
        model,
        fr,
        fa,
        rev,
        emp,
        ms
    )

    st.sidebar.success(
        f"Predicted Valuation: ${result:,.2f} Million"
    )

st.sidebar.info(f"Model R² Score : {r2:.2f}")
st.sidebar.info(f"Mean Absolute Error : {mae:.2f}")

st.subheader("📊 Feature Importance")

importance = feature_importance(model)

st.dataframe(importance)
