import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------
# Page Configuration
# ----------------------------------

st.set_page_config(
    page_title="Regional Analytics",
    page_icon="🌍",
    layout="wide"
)

st.title("🌍 Regional Analytics Dashboard")
st.markdown("Analyze startup ecosystems across different regions.")

# ----------------------------------
# Load Dataset
# ----------------------------------

df = pd.read_csv("data/startup_data.csv")

# ----------------------------------
# Sidebar Filters
# ----------------------------------

st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    df["Region"].isin(selected_regions)
]

# ----------------------------------
# KPI Cards
# ----------------------------------

total_regions = filtered_df["Region"].nunique()
total_startups = len(filtered_df)
total_funding = filtered_df["Funding Amount (M USD)"].sum()
avg_valuation = filtered_df["Valuation (M USD)"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🌍 Regions", total_regions)
c2.metric("🚀 Startups", total_startups)
c3.metric("💰 Total Funding", f"${total_funding:,.2f} M")
c4.metric("📈 Avg Valuation", f"${avg_valuation:,.2f} M")

st.divider()

# ----------------------------------
# Startup Distribution
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    region_count = (
        filtered_df["Region"]
        .value_counts()
        .reset_index()
    )

    region_count.columns = [
        "Region",
        "Count"
    ]

    fig = px.bar(
        region_count,
        x="Region",
        y="Count",
        color="Region",
        title="Number of Startups by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    funding_region = (
        filtered_df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        funding_region,
        names="Region",
        values="Funding Amount (M USD)",
        title="Regional Funding Share"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Valuation Analysis
# ----------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Employees",
        color="Region",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fig = px.box(
        filtered_df,
        x="Region",
        y="Valuation (M USD)",
        color="Region",
        title="Valuation Distribution by Region"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ----------------------------------
# Revenue Analysis
# ----------------------------------

st.subheader("💵 Average Revenue by Region")

revenue_data = (
    filtered_df.groupby("Region")
    ["Revenue (M USD)"]
    .mean()
    .reset_index()
)

fig = px.bar(
    revenue_data,
    x="Region",
    y="Revenue (M USD)",
    color="Region",
    title="Average Revenue"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Top Regional Startups
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
            "Region",
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

st.subheader("📊 Correlation Heatmap")

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
    title="Regional Analytics Correlation Matrix"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------
# Raw Dataset
# ----------------------------------

with st.expander("📋 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
