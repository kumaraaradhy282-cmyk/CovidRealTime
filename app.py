import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="COVID Live", page_icon="🦠")

st.title("🦠 COVID-19 Live Data (MVP)")

@st.cache_data(ttl=1800)
def load_data():
    url = "https://disease.sh/v3/covid-19/all"
    return requests.get(url).json()

data = load_data()

st.metric("Total Cases", f"{data['cases']:,}")
st.metric("Total Deaths", f"{data['deaths']:,}")
st.metric("Recovered", f"{data['recovered']:,}")

st.subheader("Cases Over Time (Last 30 Days)")

@st.cache_data(ttl=1800)
def history():
    url = "https://disease.sh/v3/covid-19/historical/all?lastdays=30"
    h = requests.get(url).json()
    df = pd.DataFrame({
        "date": h["cases"].keys(),
        "cases": h["cases"].values()
    })
    df["date"] = pd.to_datetime(df["date"])
    return df

df = history()

# Streamlit native chart (NO extra libs)
st.line_chart(df.set_index("date"))

st.caption("Data source: disease.sh | Streamlit Free Compatible")
