import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------
# Page Configuration
# ---------------------------------

st.set_page_config(
    page_title="Valuation Insights",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Startup Valuation Insights")
st.markdown("Analyze startup valuations across industries and regions.")

# ---------------------------------
# Load Dataset
# ---------------------------------

df = pd.read_csv("data/startup_data.csv")

# ---------------------------------
# Sidebar Filters
# ---------------------------------

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

# ---------------------------------
# KPI Cards
# ---------------------------------

total_value = filtered_df["Valuation (M USD)"].sum()
avg_value = filtered_df["Valuation (M USD)"].mean()
max_value = filtered_df["Valuation (M USD)"].max()
median_value = filtered_df["Valuation (M USD)"].median()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "💰 Total Valuation",
    f"${total_value:,.0f} M"
)

c2.metric(
    "📊 Average Valuation",
    f"${avg_value:,.2f} M"
)

c3.metric(
    "🚀 Highest Valuation",
    f"${max_value:,.2f} M"
)

c4.metric(
    "📌 Median Valuation",
    f"${median_value:,.2f} M"
)

st.divider()

# ---------------------------------
# Row 1
# ---------------------------------

col1, col2 = st.columns(2)

with col1:

    valuation_industry = (
        filtered_df
        .groupby("Industry")["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        valuation_industry,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry",
        title="Industry-wise Valuation"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    valuation_region = (
        filtered_df
        .groupby("Region")["Valuation (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        valuation_region,
        names="Region",
        values="Valuation (M USD)",
        title="Regional Valuation Share"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Row 2
# ---------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Revenue (M USD)",
        color="Industry",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.box(
        filtered_df,
        x="Industry",
        y="Valuation (M USD)",
        color="Industry",
        title="Valuation Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# ---------------------------------
# Top 10 Valuable Startups
# ---------------------------------

st.subheader("🏆 Top 10 Most Valuable Startups")

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
            "Region",
            "Valuation (M USD)",
            "Funding Amount (M USD)",
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# ---------------------------------
# Revenue vs Valuation
# ---------------------------------

st.subheader("📊 Revenue vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Revenue (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Revenue and Valuation Relationship"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Correlation Heatmap
# ---------------------------------

st.subheader("📈 Correlation Matrix")

corr = filtered_df[
    [
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)",
        "Funding Rounds"
    ]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Heatmap"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# Raw Dataset
# ---------------------------------

with st.expander("📋 View Data"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
