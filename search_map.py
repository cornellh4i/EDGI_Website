import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, Search
import math
import geopandas
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import geojson
import json

# # these are the CSV files of the capitals and countries, both located in data
# states = pd.read_csv(
#     r"data/us-state-capitals.csv")
# counties = pd.read_csv(
#     r"data/uscounties.csv")

# # creates the Streamlit map and the add to the clusters map
# map = folium.Map()
# marker_cluster = MarkerCluster().add_to(map)

# # helper to create the markers
# def create_markers(df, lat_col, lon_col, info_col, markers):
#     '''
#     Creates markers based on information in df specified by the lat_col and 
#     lon_col to reference in the df. The marker will also have a popup that 
#     displays the information that corresponds to it in the df. 

#     REQUIRES
#     - df that is a dataframe that has colums with lon_col, lat_col, and info_col
#     - lat_col is a string that represents the lat_col in the df, which contains 
#     the latitude coordinate
#     - lon_col is a string that represents the lon_col in the df, which contains 
#     the longitude coordinate
#     - info_col is a string that represents the info_col in the df, which contains
#     the information (such as the name)
#     '''
#     for index, row in df.iterrows():
#         marker = folium.Marker(
#             location=[float(row[lat_col]), float(row[lon_col])],
#             popup=row[info_col]
#         ).add_to(markers)

# # seperate markers for state and counties
# create_markers(states, "latitude", "longitude", "name", marker_cluster)
# create_markers(counties, "lat", "lng", "county", marker_cluster)

# st_data = st_folium(map)

# ========================================================================================================

states = geopandas.read_file(
    "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json",
    driver="GeoJSON",
)

counties = geopandas.read_file(
    "https://gist.githubusercontent.com/sdwfrost/d1c73f91dd9d175998ed166eb216994a/raw/e89c35f308cee7e2e5a784e1d3afc5d449e9e4bb/counties.geojson",
    driver="GeoJSON",
)

# st.write(type(counties['feature']))

def convert_state_fp(code):
    '''
    Returns the state name represented by the two-digit American National Standards Institute (ANSI) Code
    '''
    states = {"01" : "Alabama", "02" : "Alaska", "04" : "Arizona", "05" : "Arkansas", "06": "California", "08": "Colorado", "09" : "Connecticut", "10" : "Delaware", "11" : "District of Columbia", "12": "Florida", "13": "Georgia", "15": "Hawaii", "16" : "Idaho", "17" : "Illinois", "18" : "Indiana", "19" : "Iowa", "20" : "Kansas", "21" : "Kentucky", "22" : "Louisiana", "23" : "Maine", "24" : "Maryland", "25" : "Massachusetts", "26" : "Michigan", "27": "Minnesota", "28": "Mississippi", "29" : "Missouri", "30" : "Montana", "31" : "Nebraska", "32" : "Nevada", "33" : "New Hampshire", "34" : "New Jersey", "35" : "New Mexico", "36" : "New York", "37" : "North Carolina", "38" : "North Dakota", "39": "Ohio", "40": "Oklahoma", "41" : "Oregon", "42": "Pennsylvania", "44": "Rhode Island", "45" : "South Carolina", "46": "South Dakota", "47": "Tennessee", "48": "Texas", "49" : "Utah", "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia", "55": "Wisconsin", "56":"Wyoming", "72":"Puerto Rico"}

    return states[code]

f = open("data\counties.geojson",)
data = json.load(f)

# Add state names to each county name in counties.geojson
for feature in data["features"]:
    feature['properties']['NAME'] = feature['properties']['NAME'] + convert_state_fp(feature['properties']['STATEFP'])

f.close()

m = folium.Map(location=[38, -97], zoom_start=4)


def style_function(x):
    return {
        "fillColor": "white",
        "color": "black",
        "weight": 2,
        "fillOpacity": 0.5,
    }


stategeo = folium.GeoJson(
    states,
    name="US States",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["name"], aliases=["State: "], localize=True
    ),
).add_to(m)


countygeo = folium.GeoJson(
    counties,
    name="US Counties",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(
        fields=["NAME"], aliases=["County: "], localize=True
    ),
).add_to(m)


statesearch = Search(
    layer=stategeo,
    geom_type="Polygon",
    placeholder="Search for a US State",
    collapsed=False,
    search_label="name",
    weight=3,
).add_to(m)


countysearch = Search(
    layer=countygeo,
    geom_type="Polygon",
    placeholder="Search for a US County",
    collapsed=False,
    search_label="NAME",
    weight=3,
).add_to(m)


folium.LayerControl().add_to(m)
#colormap.add_to(m)

st_data = st_folium(m, width=725)