import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Industrial Analytics",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Industrial Analytics Dashboard")
st.markdown("Analyze startup performance across different industries.")

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv("data/startup_data.csv")

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filters")

selected_industries = st.sidebar.multiselect(
    "Select Industry",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

filtered_df = df[
    df["Industry"].isin(selected_industries)
]

# ----------------------------------
# KPI Section
# ----------------------------------

total_industries = filtered_df["Industry"].nunique()
total_startups = len(filtered_df)
avg_valuation = filtered_df["Valuation (M USD)"].mean()
total_funding = filtered_df["Funding Amount (M USD)"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏭 Industries",
    total_industries
)

col2.metric(
    "🚀 Startups",
    total_startups
)

col3.metric(
    "📈 Avg Valuation",
    f"${avg_valuation:,.2f} M"
)

col4.metric(
    "💰 Total Funding",
    f"${total_funding:,.2f} M"
)

st.divider()

# ----------------------------------
# Industry Distribution
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_count = (
        filtered_df["Industry"]
        .value_counts()
        .reset_index()
    )

    industry_count.columns = [
        "Industry",
        "Count"
    ]

    fig = px.bar(
        industry_count,
        x="Industry",
        y="Count",
        color="Industry",
        title="Number of Startups by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    funding_data = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        funding_data,
        names="Industry",
        values="Funding Amount (M USD)",
        title="Industry Funding Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Revenue and Valuation Analysis
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        color="Industry",
        size="Employees",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Revenue (M USD)",
        color="Industry",
        title="Revenue Distribution by Industry"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Market Share Analysis
# ----------------------------------

st.subheader("📊 Industry Market Share")

market_share = (
    filtered_df.groupby("Industry")
    ["Market Share (%)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    market_share,
    x="Industry",
    y="Market Share (%)",
    color="Industry",
    title="Average Market Share"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Top Startups
# ----------------------------------

st.subheader("🏆 Top 10 Valuable Startups")

top10 = (
    filtered_df
    .sort_values(
        by="Valuation (M USD)",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top10[
        [
            "Startup Name",
            "Industry",
            "Funding Amount (M USD)",
            "Valuation (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# ----------------------------------
# Correlation Heatmap
# ----------------------------------

st.subheader("📈 Correlation Heatmap")

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
    title="Industry Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Dataset Viewer
# ----------------------------------

with st.expander("📋 View Complete Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
