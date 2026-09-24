import streamlit as st
import pandas as pd
import plotly.express as px
import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY2") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="🛍️",
    layout="wide",
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #07111f 0%, #10243e 55%, #0b132b 100%);
    color: #e5eefb;
}

[data-testid="stSidebar"] {
    background-color: #0b1728;
    border-right: 1px solid #233a59;
}

[data-testid="stMetric"] {
    background: rgba(19, 39, 65, 0.9);
    border: 1px solid #2c527a;
    border-radius: 14px;
    padding: 18px;
}

h1 {
    color: #f8fbff;
    font-weight: 800;
}

h2, h3 {
    color: #67e8f9;
}

div.stButton > button {
    background: #22d3ee;
    color: #062033;
    border: none;
    border-radius: 10px;
    font-weight: 700;
}

div.stButton > button:hover {
    background: #a5f3fc;
    color: #062033;
}

[data-testid="stMetricLabel"] {
    color: #b9d7ef !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

/* Sidebar filter label */
[data-testid="stMultiSelect"] label p {
    color: #b9d7ef !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}



/* Filter box background */
[data-testid="stMultiSelect"] div[data-baseweb="select"] > div {
    background-color: #142b46 !important;
    border-color: #2c527a !important;
}

/* Chatbot question label */
[data-testid="stTextInput"] label p {
    color: #b9d7ef !important;
    font-weight: 600 !important;
    opacity: 1 !important;
}

/* Chatbot typing box */
[data-testid="stTextInput"] input {
    background-color: #142b46 !important;
    color: #ffffff !important;
}

[data-testid="stTextInput"] input::placeholder {
    color: #9ab4cc !important;
    opacity: 1 !important;
}

</style>
""", unsafe_allow_html=True)


st.title("🛍️ E-Commerce Sales Intelligence")
st.caption("Explore sales performance, customer activity, and AI-powered insights.")

df = pd.read_csv("ecommerce_sales_data.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

selected_cities = st.sidebar.multiselect(
    "Filter by city",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique()),
)

df = df[df["City"].isin(selected_cities)]

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
col2.metric("Orders", f"{len(df):,}")
col3.metric("Customers", f"{df['Customer ID'].nunique():,}")

st.subheader("Monthly Sales Trend")

monthly_sales = df.groupby(
    df["Order Date"].dt.to_period("M")
)["Sales"].sum()

monthly_sales.index = monthly_sales.index.astype(str)
st.line_chart(monthly_sales)

category_sales = df.groupby("Category", as_index=False)["Sales"].sum()
fig = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category",
)

fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#e5eefb",
    title_font_color="#67e8f9",
    showlegend=False,
    xaxis={"showgrid": False},
    yaxis={"gridcolor": "#24415f"},
)

st.plotly_chart(fig, use_container_width=True)

st.bar_chart(df.set_index("Product")["Sales"])

st.subheader("Sales Data")

st.dataframe(df)

st.divider()
st.subheader("Ask the Sales Chatbot")

question = st.text_input(
    "Ask a question about sales, products, customers, or cities"
)

if st.button("Ask"):
    if question:
        category_summary = (
            df.groupby("Category")["Sales"].sum().sort_values(ascending=False).to_string()
        )
        city_summary = (
            df.groupby("City")["Sales"].sum().sort_values(ascending=False).to_string()
        )
        product_summary = (
            df.groupby("Product")["Sales"].sum().sort_values(ascending=False).to_string()
        )

        context = f"""
Dataset: {len(df):,} orders from {df["Customer ID"].nunique():,} customers.
Total sales: ₹{df["Sales"].sum():,.2f}

Sales by category:
{category_summary}

Sales by city:
{city_summary}

Sales by product:
{product_summary}
"""

        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an e-commerce sales analyst. Use only the provided dataset summary."
                        "Never invent products, causes, or comparisons."
                        "If the summary does not contain enough evidence for a 'why' question, say that clearly. Be concise.",
                    },
                    {
                        "role": "user",
                        "content": f"Dataset summary:\n{context}\n\nQuestion: {question}",
                    },
                ],
            )

        st.write(response.choices[0].message.content)
    else:
        st.info("Please type a question first.")