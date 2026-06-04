import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error

# -----------------------------
# Features and Target
# -----------------------------

FEATURES = [
    "Funding Rounds",
    "Funding Amount (M USD)",
    "Revenue (M USD)",
    "Employees",
    "Market Share (%)"
]

TARGET = "Valuation (M USD)"

# -----------------------------
# Data Preparation
# -----------------------------

def prepare_data(df):

    data = df[FEATURES + [TARGET]].dropna()

    X = data[FEATURES]
    y = data[TARGET]

    return X, y

# -----------------------------
# Train ML Model
# -----------------------------

def train_valuation_model(df):

    X, y = prepare_data(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    model = LinearRegression()

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    return model, r2, mae

# -----------------------------
# Single Prediction
# -----------------------------

def predict_valuation(
    model,
    funding_rounds,
    funding_amount,
    revenue,
    employees,
    market_share
):

    input_df = pd.DataFrame({
        "Funding Rounds": [funding_rounds],
        "Funding Amount (M USD)": [funding_amount],
        "Revenue (M USD)": [revenue],
        "Employees": [employees],
        "Market Share (%)": [market_share]
    })

    prediction = model.predict(input_df)

    return prediction[0]

# -----------------------------
# Batch Prediction
# -----------------------------

def batch_prediction(model, df):

    temp = df.copy()

    temp["Predicted Valuation (M USD)"] = model.predict(
        temp[FEATURES]
    )

    return temp

# -----------------------------
# Feature Importance
# -----------------------------

def feature_importance(model):

    importance = pd.DataFrame({
        "Feature": FEATURES,
        "Coefficient": model.coef_
    })

    importance = importance.sort_values(
        by="Coefficient",
        ascending=False
    )

    return importance

# -----------------------------
# Business Insights Generator
# -----------------------------

def generate_ai_insights(df):

    insights = []

    top_industry = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .idxmax()
    )

    insights.append(
        f"🏭 Highest funded industry: {top_industry}"
    )

    top_region = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .mean()
        .idxmax()
    )

    insights.append(
        f"🌍 Region with highest average valuation: {top_region}"
    )

    profitable = (
        df["Profitable"].sum() /
        len(df)
    ) * 100

    insights.append(
        f"💹 {profitable:.1f}% startups are profitable."
    )

    highest = df.loc[
        df["Valuation (M USD)"].idxmax(),
        "Startup Name"
    ]

    insights.append(
        f"🏆 Highest valued startup: {highest}"
    )

    return insights
