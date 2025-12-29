import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="Real-Time COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide"
)

st.title("🦠 Real-Time COVID-19 Dashboard")
st.caption("Live real-world COVID-19 data (MVP)")

# -------------------------------
# Data Functions
# -------------------------------
@st.cache_data(ttl=3600)
def get_countries():
    url = "https://disease.sh/v3/covid-19/countries"
    data = requests.get(url).json()
    return sorted([c["country"] for c in data])

@st.cache_data(ttl=3600)
def get_country_data(country):
    url = f"https://disease.sh/v3/covid-19/historical/{country}?lastdays=365"
    data = requests.get(url).json()["timeline"]

    df = pd.DataFrame({
        "date": data["cases"].keys(),
        "cases": data["cases"].values(),
        "deaths": data["deaths"].values(),
        "recovered": data["recovered"].values(),
    })

    df["date"] = pd.to_datetime(df["date"])
    return df

@st.cache_data(ttl=600)
def get_current_stats(country):
    url = f"https://disease.sh/v3/covid-19/countries/{country}"
    return requests.get(url).json()

# -------------------------------
# Sidebar
# -------------------------------
st.sidebar.header("🌍 Select Country")

countries = get_countries()
country = st.sidebar.selectbox(
    "Country",
    countries,
    index=countries.index("USA") if "USA" in countries else 0
)

# -------------------------------
# Load Data
# -------------------------------
df = get_country_data(country)
stats = get_current_stats(country)

# -------------------------------
# Metrics
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Cases", f"{stats['cases']:,}")
c2.metric("Total Deaths", f"{stats['deaths']:,}")
c3.metric("Recovered", f"{stats['recovered']:,}")
c4.metric("Active", f"{stats['active']:,}")

st.divider()

# -------------------------------
# Beautiful Graph (Matplotlib)
# -------------------------------
fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(df["date"], df["cases"], label="Cases", linewidth=2)
ax.plot(df["date"], df["deaths"], label="Deaths", linewidth=2)
ax.plot(df["date"], df["recovered"], label="Recovered", linewidth=2)

ax.set_title(f"COVID-19 Trends in {country}", fontsize=16)
ax.set_xlabel("Date")
ax.set_ylabel("People")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

# -------------------------------
# Raw Data
# -------------------------------
with st.expander("📄 Show Raw Data"):
    st.dataframe(df)

# -------------------------------
# Footer
# -------------------------------
st.caption(
    f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | "
    "Source: disease.sh (WHO / Johns Hopkins)"
)
