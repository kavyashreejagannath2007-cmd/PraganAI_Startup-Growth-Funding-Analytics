import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Insights",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 AI Business Insights")
st.markdown(
    "Automatically generated insights from startup funding, valuation, and profitability data."
)

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("data/startup_data.csv")

# -----------------------------------
# KPI Cards
# -----------------------------------

total_startups = len(df)
total_funding = df["Funding Amount (M USD)"].sum()
avg_valuation = df["Valuation (M USD)"].mean()
profit_rate = (df["Profitable"].sum() / total_startups) * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric("🚀 Startups", total_startups)
c2.metric("💰 Total Funding", f"${total_funding:,.0f} M")
c3.metric("📈 Avg Valuation", f"${avg_valuation:,.2f} M")
c4.metric("💹 Profit Rate", f"{profit_rate:.1f}%")

st.divider()

# -----------------------------------
# AI Generated Insights
# -----------------------------------

st.subheader("🤖 Automated Insights")

top_industry = (
    df.groupby("Industry")["Funding Amount (M USD)"]
    .sum()
    .idxmax()
)

top_region = (
    df.groupby("Region")["Valuation (M USD)"]
    .mean()
    .idxmax()
)

highest_company = (
    df.loc[
        df["Valuation (M USD)"].idxmax(),
        "Startup Name"
    ]
)

avg_revenue = df["Revenue (M USD)"].mean()

profitable_percent = (
    df["Profitable"].sum() /
    len(df)
) * 100

st.success(
    f"""
### 📌 Key Findings

- 🏭 **{top_industry}** receives the highest overall funding.

- 🌍 **{top_region}** has the highest average startup valuation.

- 🏆 **{highest_company}** is the highest-valued startup.

- 💰 Average startup revenue is **${avg_revenue:,.2f} Million**.

- 💹 Approximately **{profitable_percent:.1f}%** of startups are profitable.

- 📈 Higher funding generally leads to higher valuation.
"""
)

st.divider()

# -----------------------------------
# Industry Funding
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    funding = (
        df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        funding,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="AI Insight: Industry Funding"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    valuation = (
        df.groupby("Region")
        ["Valuation (M USD)"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        valuation,
        x="Region",
        y="Valuation (M USD)",
        color="Region",
        title="AI Insight: Average Regional Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# -----------------------------------
# Funding vs Valuation
# -----------------------------------

st.subheader("📊 AI Pattern Detection")

fig = px.scatter(
    df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Profitable",
    size="Employees",
    hover_name="Startup Name",
    title="Funding vs Valuation Pattern"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.info(
    "💡 AI Observation: Startups with larger funding amounts generally show higher valuations, although some highly efficient startups achieve strong valuations with relatively lower funding."
)

st.divider()

# -----------------------------------
# Profitability Analysis
# -----------------------------------

profit = (
    df["Profitable"]
    .value_counts()
    .reset_index()
)

profit.columns = ["Status", "Count"]

profit["Status"] = profit["Status"].map(
    {
        True: "Profitable",
        False: "Non-Profitable"
    }
)

fig = px.pie(
    profit,
    names="Status",
    values="Count",
    title="AI Insight: Profitability Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# -----------------------------------
# Top 10 AI Recommended Startups
# -----------------------------------

st.subheader("🏆 AI Recommended High-Potential Startups")

recommend = (
    df.sort_values(
        by=[
            "Valuation (M USD)",
            "Revenue (M USD)"
        ],
        ascending=False
    )
    .head(10)
)

st.dataframe(
    recommend[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Funding Amount (M USD)",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Profitable"
        ]
    ],
    use_container_width=True
)

st.divider()

# -----------------------------------
# Correlation Heatmap
# -----------------------------------

st.subheader("🔥 AI Correlation Matrix")

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
    title="Business Metric Correlation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Raw Dataset
# -----------------------------------

with st.expander("📋 View Dataset"):
    st.dataframe(
        df,
        use_container_width=True
    )
