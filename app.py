import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="Real-Time COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 Real-Time COVID-19 Dashboard")
st.caption("Live data from real-world sources • MVP built with Streamlit")

# -------------------------------
# Helper Functions
# -------------------------------
@st.cache_data(ttl=3600)
def get_countries():
    url = "https://disease.sh/v3/covid-19/countries"
    response = requests.get(url)
    data = response.json()
    return sorted([c["country"] for c in data])

@st.cache_data(ttl=3600)
def get_country_data(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=365"
    response = requests.get(url)
    data = response.json()
    timeline = data["timeline"]

    df = pd.DataFrame({
        "date": timeline["cases"].keys(),
        "cases": timeline["cases"].values(),
        "deaths": timeline["deaths"].values(),
        "recovered": timeline["recovered"].values(),
    })

    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=600)
def get_current_stats(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    response = requests.get(url)
    return response.json()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🌍 Settings")

countries = get_countries()
selected_country = st.sidebar.selectbox(
    "Select Country",
    countries,
    index=countries.index("USA") if "USA" in countries else 0
)

# -------------------------------
# Load Data
# -------------------------------
df = get_country_data(selected_country)
stats = get_current_stats(selected_country)

# -------------------------------
# Metrics
# -------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cases", f"{stats['cases']:,}")
col2.metric("Total Deaths", f"{stats['deaths']:,}")
col3.metric("Recovered", f"{stats['recovered']:,}")
col4.metric("Active Cases", f"{stats['active']:,}")

st.markdown("---")

# -------------------------------
# Interactive Graph
# -------------------------------
fig = px.line(
    df,
    x="date",
    y=["cases", "deaths", "recovered"],
    title=f"COVID-19 Trend in {selected_country}",
    labels={
        "value": "Number of People",
        "date": "Date",
        "variable": "Metric"
    },
    template="plotly_dark"
)

fig.update_layout(
    hovermode="x unified",
    legend_title_text="",
    title_x=0.5
)

st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Raw Data (Optional MVP Feature)
# -------------------------------
with st.expander("📄 View Raw Data"):
    st.dataframe(df)

# -------------------------------
# Footer
# -------------------------------
st.caption(
    f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | "
    "Data source: disease.sh (Johns Hopkins / WHO)"
)
