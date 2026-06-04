import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Profitability Analytics",
    page_icon="💹",
    layout="wide"
)

st.title("💹 Profitability Analytics Dashboard")
st.markdown("Analyze startup profitability and financial performance.")

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv("data/startup_data.csv")

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filters")

industry = st.sidebar.multiselect(
    "Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

# ----------------------------------
# KPI Cards
# ----------------------------------

total_startups = len(filtered_df)
profitable = filtered_df["Profitable"].sum()
non_profitable = total_startups - profitable
profit_rate = (profitable / total_startups) * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric("🚀 Total Startups", total_startups)
c2.metric("✅ Profitable", profitable)
c3.metric("❌ Non-Profitable", non_profitable)
c4.metric("📊 Profit Rate", f"{profit_rate:.1f}%")

st.divider()

# ----------------------------------
# Profitability Distribution
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    profit_data = (
        filtered_df["Profitable"]
        .value_counts()
        .reset_index()
    )

    profit_data.columns = ["Status", "Count"]
    profit_data["Status"] = profit_data["Status"].map({
        True: "Profitable",
        False: "Non-Profitable"
    })

    fig = px.pie(
        profit_data,
        names="Status",
        values="Count",
        title="Profitability Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    industry_profit = (
        filtered_df.groupby("Industry")["Profitable"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        industry_profit,
        x="Industry",
        y="Profitable",
        color="Industry",
        title="Profitable Startups by Industry"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------------
# Revenue vs Valuation
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        color="Profitable",
        size="Employees",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.box(
        filtered_df,
        x="Profitable",
        y="Revenue (M USD)",
        color="Profitable",
        title="Revenue Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ----------------------------------
# Regional Profitability
# ----------------------------------

st.subheader("🌍 Profitable Startups by Region")

region_profit = (
    filtered_df.groupby("Region")["Profitable"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_profit,
    x="Region",
    y="Profitable",
    color="Region",
    title="Regional Profitability"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Top Profitable Startups
# ----------------------------------

st.subheader("🏆 Top 10 Highest Revenue Startups")

top10 = (
    filtered_df
    .sort_values(
        by="Revenue (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[
        [
            "Startup Name",
            "Industry",
            "Region",
            "Revenue (M USD)",
            "Valuation (M USD)",
            "Profitable"
        ]
    ],
    use_container_width=True
)

# ----------------------------------
# Correlation Heatmap
# ----------------------------------

st.subheader("📈 Financial Correlation Matrix")

corr = filtered_df[
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

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------
# Dataset Viewer
# ----------------------------------

with st.expander("📋 View Complete Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
