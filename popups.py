import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import math

states = pd.read_csv(
    r"C:\Users\yummy\OneDrive\Documents\h4i\EDGI_Website\us-state-capitals.csv")
counties = pd.read_csv(
    r"C:\Users\yummy\OneDrive\Documents\h4i\EDGI_Website\uscounties.csv")

map = folium.Map()
marker_cluster = MarkerCluster().add_to(map)


def create_markers(df, lat_col, lon_col, info_col, markers):
    for index, row in df.iterrows():
        marker = folium.Marker(
            location=[float(row[lat_col]), float(row[lon_col])],
            popup=row[info_col]
        ).add_to(markers)


create_markers(states, "latitude", "longitude", "name", marker_cluster)
create_markers(counties, "lat", "lng", "county", marker_cluster)

st_data = st_folium(map)
