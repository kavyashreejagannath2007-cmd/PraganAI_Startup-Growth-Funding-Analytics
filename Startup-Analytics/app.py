import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Startup Analytics Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Startup Analytics Dashboard")
st.markdown("---")

df = pd.read_csv("startup_data.csv")

# Sidebar

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

exit_status = st.sidebar.multiselect(
    "Exit Status",
    options=df["Exit Status"].unique(),
    default=df["Exit Status"].unique()
)

filtered_df = df[
    (df["Industry"].isin(industry)) &
    (df["Region"].isin(region)) &
    (df["Exit Status"].isin(exit_status))
]

# KPIs

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric(
    "Total Startups",
    len(filtered_df)
)

col2.metric(
    "Total Funding",
    f"${filtered_df['Funding Amount (M USD)'].sum():,.0f} M"
)

col3.metric(
    "Avg Valuation",
    f"${filtered_df['Valuation (M USD)'].mean():,.0f} M"
)

col4.metric(
    "Total Revenue",
    f"${filtered_df['Revenue (M USD)'].sum():,.0f} M"
)

col5.metric(
    "Profitable",
    filtered_df["Profitable"].sum()
)

st.markdown("---")

# Row 1

col1,col2 = st.columns(2)

with col1:
    fig = px.bar(
        filtered_df.groupby("Industry")["Funding Amount (M USD)"].sum().reset_index(),
        x="Industry",
        y="Funding Amount (M USD)",
        color="Industry",
        title="Industry-wise Funding"
    )
    st.plotly_chart(fig,use_container_width=True)

with col2:
    fig = px.pie(
        filtered_df,
        names="Region",
        title="Region Distribution"
    )
    st.plotly_chart(fig,use_container_width=True)

# Row 2

col1,col2 = st.columns(2)

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
    st.plotly_chart(fig,use_container_width=True)

with col2:
    fig = px.histogram(
        filtered_df,
        x="Funding Rounds",
        color="Industry",
        title="Funding Rounds Distribution"
    )
    st.plotly_chart(fig,use_container_width=True)

# Row 3

col1,col2 = st.columns(2)

with col1:
    fig = px.box(
        filtered_df,
        x="Industry",
        y="Market Share (%)",
        color="Industry",
        title="Market Share Analysis"
    )
    st.plotly_chart(fig,use_container_width=True)

with col2:
    exit_data = filtered_df["Exit Status"].value_counts().reset_index()
    exit_data.columns = ["Exit Status","Count"]

    fig = px.bar(
        exit_data,
        x="Exit Status",
        y="Count",
        color="Exit Status",
        title="Exit Status"
    )
    st.plotly_chart(fig,use_container_width=True)

# Correlation Heatmap

st.subheader("Correlation Matrix")

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
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig,use_container_width=True)

# Top Startups

st.subheader("Top 10 Valuable Startups")

top = filtered_df.sort_values(
    by="Valuation (M USD)",
    ascending=False
).head(10)

st.dataframe(top)
