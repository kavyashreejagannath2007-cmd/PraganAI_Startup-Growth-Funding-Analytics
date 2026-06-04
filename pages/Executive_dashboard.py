import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# Page Configuration
# ---------------------------

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Executive Dashboard")
st.markdown("### Startup Ecosystem Overview")

# ---------------------------
# Load Data
# ---------------------------

df = pd.read_csv("data/startup_data.csv")

# ---------------------------
# Sidebar Filters
# ---------------------------

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

# ---------------------------
# KPI Section
# ---------------------------

total_startups = len(filtered_df)
total_funding = filtered_df["Funding Amount (M USD)"].sum()
avg_valuation = filtered_df["Valuation (M USD)"].mean()
total_revenue = filtered_df["Revenue (M USD)"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🚀 Total Startups",
    total_startups
)

col2.metric(
    "💰 Total Funding",
    f"${total_funding:,.0f} M"
)

col3.metric(
    "📈 Avg Valuation",
    f"${avg_valuation:,.0f} M"
)

col4.metric(
    "💵 Total Revenue",
    f"${total_revenue:,.0f} M"
)

st.markdown("---")

# ---------------------------
# Charts Row 1
# ---------------------------

col1, col2 = st.columns(2)

with col1:

    industry_funding = (
        filtered_df
        .groupby("Industry")["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        industry_funding,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Industry-wise Funding"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered_df,
        names="Region",
        title="Regional Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Charts Row 2
# ---------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Revenue (M USD)",
        y="Valuation (M USD)",
        size="Employees",
        color="Industry",
        hover_name="Startup Name",
        title="Revenue vs Valuation"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.histogram(
        filtered_df,
        x="Funding Rounds",
        color="Industry",
        title="Funding Rounds Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------
# Top 10 Startups
# ---------------------------

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
            "Revenue (M USD)"
        ]
    ],
    use_container_width=True
)

# ---------------------------
# Correlation Heatmap
# ---------------------------

st.subheader("📊 Correlation Analysis")

corr = filtered_df[
    [
        "Funding Rounds",
        "Funding Amount (M USD)",
        "Valuation (M USD)",
        "Revenue (M USD)",
        "Employees",
        "Market Share (%)"
    ]
].corr()

fig = px.imshow(
    corr,
    text_auto=True,
    aspect="auto",
    title="Feature Correlation Heatmap"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------
# Raw Data
# ---------------------------

with st.expander("📋 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
