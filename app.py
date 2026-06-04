from utils.ml_modules import train_valuation_model, predict_valuation

model, accuracy = train_valuation_model(df)

st.sidebar.subheader("🤖 ML Valuation Predictor")

fr = st.sidebar.number_input("Funding Rounds", 1, 20, 5)
fa = st.sidebar.number_input("Funding Amount (M USD)", 1.0, 5000.0, 100.0)
rev = st.sidebar.number_input("Revenue (M USD)", 1.0, 5000.0, 50.0)
emp = st.sidebar.number_input("Employees", 1, 100000, 500)
ms = st.sidebar.slider("Market Share (%)", 0.0, 100.0, 5.0)

if st.sidebar.button("Predict Valuation"):
    pred = predict_valuation(
        model,
        fr,
        fa,
        rev,
        emp,
        ms
    )

    st.sidebar.success(
        f"Estimated Valuation: ${pred:,.2f} Million"
    )

st.sidebar.info(f"Model Accuracy (R² Score): {accuracy:.2f}")
