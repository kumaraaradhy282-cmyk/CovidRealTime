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

st.divider()
st.subheader("🌍 Country-wise Live COVID Cases")

@st.cache_data(ttl=1800)
def load_country_data():
    url = "https://disease.sh/v3/covid-19/countries"
    return requests.get(url).json()

countries = load_country_data()

# Show top 10 countries by cases (simple & fast)
for c in sorted(countries, key=lambda x: x["cases"], reverse=True)[:10]:
    st.write(
        f"**{c['country']}** → "
        f"Cases: {c['cases']:,}, "
        f"Deaths: {c['deaths']:,}, "
        f"Active: {c['active']:,}"
    )

st.caption("Country data is live and auto-updated")


st.divider()
st.subheader("🌍 World COVID-19 Heat Map (Live)")

import pandas as pd
import pydeck as pdk

@st.cache_data(ttl=1800)
def load_world_map_data():
    url = "https://disease.sh/v3/covid-19/countries"
    data = requests.get(url).json()

    rows = []
    for c in data:
        if c.get("countryInfo") and c["countryInfo"].get("lat"):
            rows.append({
                "country": c["country"],
                "lat": c["countryInfo"]["lat"],
                "lon": c["countryInfo"]["long"],
                "cases": c["cases"]
            })

    return pd.DataFrame(rows)

df_map = load_world_map_data()

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_map,
    get_position="[lon, lat]",
    get_radius="cases / 500",
    get_fill_color="[255, 0, 0, 140]",
    pickable=True,
)

view_state = pdk.ViewState(
    latitude=20,
    longitude=0,
    zoom=1,
)

deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>{country}</b><br/>Cases: {cases}",
        "style": {"color": "white"}
    },
)

st.pydeck_chart(deck)

