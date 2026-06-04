import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="Funding Analytics",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Funding Analytics Dashboard")
st.markdown("Analyze startup funding patterns and investment trends.")

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("data/startup_data.csv")

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filter Data")

industry = st.sidebar.multiselect(
    "Industry",
    df["Industry"].unique(),
    default=df["Industry"].unique()
)

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region))
]

# -----------------------------
# KPI Cards
# -----------------------------

total_funding = filtered_df["Funding Amount (M USD)"].sum()
avg_funding = filtered_df["Funding Amount (M USD)"].mean()
max_funding = filtered_df["Funding Amount (M USD)"].max()
avg_rounds = filtered_df["Funding Rounds"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💵 Total Funding", f"${total_funding:,.0f} M")
c2.metric("📊 Average Funding", f"${avg_funding:,.2f} M")
c3.metric("🚀 Highest Funding", f"${max_funding:,.2f} M")
c4.metric("🔄 Avg Funding Rounds", f"{avg_rounds:.1f}")

st.divider()

# -----------------------------
# Funding by Industry
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    industry_data = (
        filtered_df.groupby("Industry")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        industry_data,
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Funding by Industry"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    region_data = (
        filtered_df.groupby("Region")
        ["Funding Amount (M USD)"]
        .sum()
        .reset_index()
    )

    fig = px.pie(
        region_data,
        names="Region",
        values="Funding Amount (M USD)",
        title="Regional Funding Share"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Funding vs Valuation
# -----------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Funding Amount (M USD)",
        y="Valuation (M USD)",
        size="Employees",
        color="Industry",
        hover_name="Startup Name",
        title="Funding vs Valuation"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.histogram(
        filtered_df,
        x="Funding Rounds",
        nbins=15,
        color="Industry",
        title="Funding Rounds Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------------
# Top Funded Companies
# -----------------------------

st.subheader("🏆 Top 10 Funded Startups")

top10 = (
    filtered_df.sort_values(
        by="Funding Amount (M USD)",
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
            "Valuation (M USD)"
        ]
    ],
    use_container_width=True
)

# -----------------------------
# Funding Trend by Year
# -----------------------------

if "Founded Year" in filtered_df.columns:

    st.subheader("📈 Startup Founded Year Trend")

    year_data = (
        filtered_df.groupby("Founded Year")
        .size()
        .reset_index(name="Count")
    )

    fig = px.line(
        year_data,
        x="Founded Year",
        y="Count",
        markers=True,
        title="Startups Founded Per Year"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Raw Data
# -----------------------------

with st.expander("📋 View Dataset"):
    st.dataframe(
        filtered_df,
        use_container_width=True
    )
