import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import math

# these are the CSV files of the capitals and countries, both located in data
states = pd.read_csv(
    r"data/us-state-capitals.csv")
counties = pd.read_csv(
    r"data/uscounties.csv")

# creates the Streamlit map and the add to the clusters map
map = folium.Map()
marker_cluster = MarkerCluster().add_to(map)

# helper to create the markers
def create_markers(df, lat_col, lon_col, info_col, markers):
    '''
    Creates markers based on information in df specified by the lat_col and 
    lon_col to reference in the df. The marker will also have a popup that 
    displays the information that corresponds to it in the df. 

    REQUIRES
    - df that is a dataframe that has colums with lon_col, lat_col, and info_col
    - lat_col is a string that represents the lat_col in the df, which contains 
    the latitude coordinate
    - lon_col is a string that represents the lon_col in the df, which contains 
    the longitude coordinate
    - info_col is a string that represents the info_col in the df, which contains
    the information (such as the name)
    '''
    for index, row in df.iterrows():
        marker = folium.Marker(
            location=[float(row[lat_col]), float(row[lon_col])],
            popup=row[info_col]
        ).add_to(markers)

# seperate markers for state and counties
create_markers(states, "latitude", "longitude", "name", marker_cluster)
create_markers(counties, "lat", "lng", "county", marker_cluster)

st_data = st_folium(map)
