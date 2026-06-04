import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Startup Segmentation",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 Startup Segmentation")
st.markdown("Group startups based on industry, funding, valuation, and profitability.")

# -----------------------------------
# Load Dataset
# -----------------------------------

df = pd.read_csv("data/startup_data.csv")

# -----------------------------------
# Sidebar Filters
# -----------------------------------

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

# -----------------------------------
# KPI Cards
# -----------------------------------

total = len(filtered_df)
industries = filtered_df["Industry"].nunique()
regions = filtered_df["Region"].nunique()
avg_val = filtered_df["Valuation (M USD)"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("🚀 Startups", total)
c2.metric("🏭 Industries", industries)
c3.metric("🌍 Regions", regions)
c4.metric("📈 Avg Valuation", f"${avg_val:,.2f} M")

st.divider()

# -----------------------------------
# Industry Segmentation
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    industry_count = (
        filtered_df["Industry"]
        .value_counts()
        .reset_index()
    )

    industry_count.columns = ["Industry", "Count"]

    fig = px.bar(
        industry_count,
        x="Industry",
        y="Count",
        color="Industry",
        title="Startup Distribution by Industry"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered_df,
        names="Industry",
        title="Industry Share"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------
# Funding vs Valuation Segmentation
# -----------------------------------

st.subheader("💰 Funding vs Valuation")

fig = px.scatter(
    filtered_df,
    x="Funding Amount (M USD)",
    y="Valuation (M USD)",
    color="Industry",
    size="Employees",
    hover_name="Startup Name",
    title="Startup Segments"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Regional Segmentation
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    region_data = (
        filtered_df["Region"]
        .value_counts()
        .reset_index()
    )

    region_data.columns = ["Region", "Count"]

    fig = px.bar(
        region_data,
        x="Region",
        y="Count",
        color="Region",
        title="Regional Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

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

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------------
# Profitability Segmentation
# -----------------------------------

st.subheader("💹 Profitability Segments")

profit_data = (
    filtered_df["Profitable"]
    .value_counts()
    .reset_index()
)

profit_data.columns = ["Status", "Count"]
profit_data["Status"] = profit_data["Status"].map(
    {
        True: "Profitable",
        False: "Non-Profitable"
    }
)

fig = px.pie(
    profit_data,
    names="Status",
    values="Count",
    title="Profitability Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Top Segments Table
# -----------------------------------

st.subheader("🏆 Top 10 High-Valuation Startups")

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
            "Funding Amount (M USD)",
            "Valuation (M USD)",
            "Revenue (M USD)",
            "Profitable"
        ]
    ],
    use_container_width=True
)

# -----------------------------------
# Correlation Heatmap
# -----------------------------------

st.subheader("📊 Correlation Matrix")

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
    title="Startup Feature Correlation"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Dataset Viewer
# -----------------------------------

with st.expander("📋 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
