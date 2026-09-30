from base64 import b64encode
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from PIL import Image


st.set_page_config(page_title="Netflix Insights", page_icon="N", layout="wide")

assets_dir = Path(__file__).resolve().parent
background_path = assets_dir / "bg.jpg"
background_css = ""
if background_path.exists():
    background_data = b64encode(background_path.read_bytes()).decode("ascii")
    background_css = f"""
    .stApp {{
        background-image:
            linear-gradient(115deg, rgba(7, 8, 10, 0.80), rgba(7, 8, 10, 0.68) 55%, rgba(7, 8, 10, 0.82)),
            url("data:image/jpeg;base64,{background_data}");
        background-position: center;
        background-size: cover;
        background-attachment: fixed;
        background-color: #090a0c;
    }}
    """

st.markdown(
    """
    <style>
    @keyframes dashboard-enter {
        from { opacity: 0; transform: translateY(12px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stApp { background: #090a0c; color: #f4f1ef; }
    {background_css}
    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stSidebar"] {
        background: rgba(10, 11, 13, 0.94);
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }
    [data-testid="stSidebar"] * { color: #e9e6e4; }
    .block-container { max-width: 1440px; padding-top: 2.25rem; padding-bottom: 3rem; }
    h1, h2, h3 { color: #fffaf8; }
    h1 {
        font-size: 2.4rem;
        font-weight: 750;
        animation: dashboard-enter 650ms cubic-bezier(0.2, 0.7, 0.2, 1) both;
    }
    [data-testid="stCaptionContainer"] { color: #b4b0ae; }
    [data-testid="stMetric"] {
        background: rgba(18, 20, 23, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-top: 2px solid #e50914;
        border-radius: 6px;
        padding: 1rem 1.1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
        animation: dashboard-enter 600ms cubic-bezier(0.2, 0.7, 0.2, 1) both;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] { animation-delay: 80ms; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] { animation-delay: 150ms; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] { animation-delay: 220ms; }
    [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(4) [data-testid="stMetric"] { animation-delay: 290ms; }
    [data-testid="stMetricLabel"] p { color: #aaa6a4; }
    [data-testid="stMetricValue"] { color: #fffaf8; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(17, 19, 22, 0.9);
        border-color: rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }
    [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:has([data-testid="stMarkdownContainer"] strong):has([data-testid="stImage"]) {
        animation: dashboard-enter 700ms cubic-bezier(0.2, 0.7, 0.2, 1) both;
    }
    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:nth-child(1) { animation-delay: 120ms !important; }
    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:nth-child(1) { animation-delay: 200ms !important; }
    [data-testid="stColumn"]:nth-child(1) > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:nth-child(2) { animation-delay: 280ms !important; }
    [data-testid="stColumn"]:nth-child(2) > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:nth-child(2) { animation-delay: 360ms !important; }
    [data-testid="stFileUploader"] {
        background: transparent;
        border: 0;
    }
    [data-testid="stFileUploaderDropzone"] {
        background: rgba(25, 27, 30, 0.92);
        border: 1px dashed rgba(255, 255, 255, 0.24);
        border-radius: 6px;
    }
    [data-testid="stFileUploaderDropzone"] button {
        color: #f4f1ef !important;
        background: #303236 !important;
        border: 1px solid #505258 !important;
    }
    [data-testid="stFileUploaderDropzone"] small { color: #b4b0ae; }
    [data-testid="stMultiSelect"] .react-aria-ComboBox > [role="group"] {
        background: rgba(25, 27, 30, 0.92) !important;
        border: 1px dashed rgba(255, 255, 255, 0.24) !important;
        border-radius: 6px;
    }
    [data-testid="stMultiSelectTagsContainer"] { background: transparent !important; }
    [data-testid="stMultiSelect"] [data-tag] {
        background: #303236 !important;
        border: 1px solid #505258 !important;
        color: #f4f1ef !important;
    }
    [data-testid="stMultiSelect"] input { color: #f4f1ef !important; }
    [data-baseweb="popover"] { background: #191b1e !important; }
    [role="listbox"] { background: #191b1e !important; }
    [role="option"] { color: #e9e6e4 !important; }
    [role="option"]:hover { background: #303236 !important; }
    [data-testid="stDataFrame"] { border: 1px solid rgba(255, 255, 255, 0.12); }
    hr { border-color: rgba(255, 255, 255, 0.12); }
    @media (prefers-reduced-motion: reduce) {
        h1, [data-testid="stMetric"],
        [data-testid="stColumn"] > [data-testid="stVerticalBlock"] > [data-testid="stLayoutWrapper"]:has([data-testid="stMarkdownContainer"] strong):has([data-testid="stImage"]) {
            animation: none !important;
        }
    }
    </style>
    """.replace("{background_css}", background_css),
    unsafe_allow_html=True,
)

header_columns = st.columns([2, 11], vertical_alignment="center")
logo_path = assets_dir / "logo.csv"
if logo_path.exists():
    with header_columns[0]:
        with Image.open(logo_path) as logo_image:
            st.image(logo_image.convert("RGBA"), width=52)
with header_columns[1]:
    st.title("Netflix Insights")
st.caption("Revenue, subscription ratings, and viewing trends")

uploaded_file = st.sidebar.file_uploader("Upload a Netflix CSV", type=["csv"])

if uploaded_file is not None:
    source_name = uploaded_file.name
    source_data = pd.read_csv(uploaded_file)
elif __import__("pathlib").Path("netflix.csv").exists():
    source_name = "netflix.csv"
    source_data = pd.read_csv(source_name)
else:
    st.info("Upload a CSV containing Region, Monthly_Revenue, Subscription_Plan, Rating, Category, and Watch_Date to view the dashboard.")
    st.stop()

required_columns = {
    "Region",
    "Monthly_Revenue",
    "Subscription_Plan",
    "Rating",
    "Category",
    "Watch_Date",
}
missing_columns = sorted(required_columns.difference(source_data.columns))
if missing_columns:
    st.error(f"This CSV is missing required columns: {', '.join(missing_columns)}")
    st.stop()

data = source_data.copy()
data["Monthly_Revenue"] = pd.to_numeric(data["Monthly_Revenue"], errors="coerce")
data["Rating"] = pd.to_numeric(data["Rating"], errors="coerce")
data["Watch_Date"] = pd.to_datetime(data["Watch_Date"], errors="coerce")
for column in ("Region", "Subscription_Plan", "Category"):
    data[column] = data[column].fillna("Unknown").astype(str)
data = data.drop_duplicates()
data["Monthly_Revenue"] = data["Monthly_Revenue"].fillna(data["Monthly_Revenue"].median())
data["Rating"] = data["Rating"].fillna(data["Rating"].median())

st.sidebar.divider()
st.sidebar.caption(f"Data source: {source_name}")
selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(data["Region"].unique()),
    default=sorted(data["Region"].unique()),
)
selected_plans = st.sidebar.multiselect(
    "Subscription plan",
    options=sorted(data["Subscription_Plan"].unique()),
    default=sorted(data["Subscription_Plan"].unique()),
)

filtered = data[
    data["Region"].isin(selected_regions)
    & data["Subscription_Plan"].isin(selected_plans)
]
if filtered.empty:
    st.warning("No rows match the selected filters.")
    st.stop()

metric_columns = st.columns(4)
metric_columns[0].metric("Total revenue", f"${filtered['Monthly_Revenue'].sum():,.2f}")
metric_columns[1].metric("Average rating", f"{filtered['Rating'].mean():.2f} / 5")
metric_columns[2].metric("Records", f"{len(filtered):,}")
metric_columns[3].metric("Regions", f"{filtered['Region'].nunique():,}")

st.subheader("Performance overview")
chart_columns = st.columns(2)
chart_color = "#e50914"
text_color = "#c3bfc0"
plt.rcParams.update(
    {
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "text.color": text_color,
        "axes.labelcolor": text_color,
        "xtick.color": text_color,
        "ytick.color": text_color,
    }
)

with chart_columns[0], st.container(border=True):
    st.markdown("**Revenue by region**")
    revenue_by_region = filtered.groupby("Region")["Monthly_Revenue"].sum().sort_values()
    figure, axis = plt.subplots(figsize=(7, 3.4))
    axis.barh(revenue_by_region.index, revenue_by_region.values, color=chart_color)
    axis.set_xlabel("Revenue", color=text_color)
    axis.grid(axis="x", color="#34373c", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.spines["bottom"].set_color("#45484d")
    axis.tick_params(colors=text_color, length=0)
    figure.tight_layout()
    st.pyplot(figure, width="stretch")
    plt.close(figure)

with chart_columns[1], st.container(border=True):
    st.markdown("**Ratings by subscription plan**")
    ratings_by_plan = filtered.groupby("Subscription_Plan")["Rating"].sum()
    figure, axis = plt.subplots(figsize=(7, 3.4))
    if ratings_by_plan.sum() > 0:
        axis.pie(
            ratings_by_plan,
            labels=ratings_by_plan.index,
            autopct="%1.0f%%",
            startangle=90,
            colors=["#e50914", "#f08a5d", "#4fb3a5", "#7798c4", "#c9b57a"],
            wedgeprops={"linewidth": 2, "edgecolor": "white"},
            textprops={"color": text_color},
        )
        axis.axis("equal")
    else:
        axis.text(0.5, 0.5, "No rating data", ha="center", va="center")
        axis.axis("off")
    figure.tight_layout()
    st.pyplot(figure, width="stretch")
    plt.close(figure)

with chart_columns[0], st.container(border=True):
    st.markdown("**Revenue by category**")
    revenue_by_category = filtered.groupby("Category")["Monthly_Revenue"].sum().sort_values()
    figure, axis = plt.subplots(figsize=(7, 3.4))
    axis.barh(revenue_by_category.index, revenue_by_category.values, color="#4fb3a5")
    axis.set_xlabel("Revenue", color=text_color)
    axis.grid(axis="x", color="#34373c", linewidth=0.8)
    axis.set_axisbelow(True)
    axis.spines[["top", "right", "left"]].set_visible(False)
    axis.spines["bottom"].set_color("#45484d")
    axis.tick_params(colors=text_color, length=0)
    figure.tight_layout()
    st.pyplot(figure, width="stretch")
    plt.close(figure)

with chart_columns[1], st.container(border=True):
    st.markdown("**Monthly revenue trend**")
    dated_rows = filtered.dropna(subset=["Watch_Date"])
    if dated_rows.empty:
        st.info("No valid Watch_Date values are available for the monthly trend.")
    else:
        revenue_by_month = (
            dated_rows.assign(Month=dated_rows["Watch_Date"].dt.to_period("M").dt.to_timestamp())
            .groupby("Month")["Monthly_Revenue"]
            .sum()
            .sort_index()
        )
        figure, axis = plt.subplots(figsize=(7, 3.4))
        axis.plot(
            revenue_by_month.index,
            revenue_by_month.values,
            color=chart_color,
            marker="o",
            linewidth=2.5,
        )
        axis.fill_between(revenue_by_month.index, revenue_by_month.values, color=chart_color, alpha=0.1)
        axis.set_ylabel("Revenue", color=text_color)
        axis.grid(axis="y", color="#34373c", linewidth=0.8)
        axis.set_axisbelow(True)
        axis.spines[["top", "right", "left"]].set_visible(False)
        axis.spines["bottom"].set_color("#45484d")
        axis.tick_params(colors=text_color, length=0)
        figure.autofmt_xdate(rotation=0)
        figure.tight_layout()
        st.pyplot(figure, width="stretch")
        plt.close(figure)

with st.expander("Preview cleaned data"):
    st.dataframe(filtered, width="stretch", hide_index=True)