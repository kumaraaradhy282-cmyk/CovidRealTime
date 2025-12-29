import streamlit as st
import requests

st.set_page_config(page_title="COVID MVP", page_icon="🦠")

st.title("🦠 COVID-19 Live MVP")

@st.cache_data(ttl=1800)
def load_data():
    url = "https://disease.sh/v3/covid-19/all"
    return requests.get(url).json()

data = load_data()

st.write("### Global Numbers (Live)")
st.write(f"**Total Cases:** {data['cases']:,}")
st.write(f"**Total Deaths:** {data['deaths']:,}")
st.write(f"**Recovered:** {data['recovered']:,}")

st.caption("Data source: disease.sh | Streamlit Free Safe")
