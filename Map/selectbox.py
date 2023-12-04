import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import geopandas
import json

# Style constants
UNSELECTED_FILL = "#00000000"
UNSELECTED_OUTLINE = "black"
HIGHLIGHT_FILL = "#FF0000"
HIGHLIGHT_OUTLINE = "#9A0000"

with open("../css/style.css") as f:
        st.markdown(
            f"""<style>{f.read()}</style>""",
            unsafe_allow_html=True,
        )

def convert_state_fp(code):
    '''
    Returns the state name represented by the two-digit American National Standards Institute (ANSI) Code
    '''
    states = {"01" : "Alabama", "02" : "Alaska", "04" : "Arizona", "05" : "Arkansas", "06": "California", "08": "Colorado", "09" : "Connecticut", "10" : "Delaware", "11" : "District of Columbia", "12": "Florida", "13": "Georgia", "15": "Hawaii", "16" : "Idaho", "17" : "Illinois", "18" : "Indiana", "19" : "Iowa", "20" : "Kansas", "21" : "Kentucky", "22" : "Louisiana", "23" : "Maine", "24" : "Maryland", "25" : "Massachusetts", "26" : "Michigan", "27": "Minnesota", "28": "Mississippi", "29" : "Missouri", "30" : "Montana", "31" : "Nebraska", "32" : "Nevada", "33" : "New Hampshire", "34" : "New Jersey", "35" : "New Mexico", "36" : "New York", "37" : "North Carolina", "38" : "North Dakota", "39": "Ohio", "40": "Oklahoma", "41" : "Oregon", "42": "Pennsylvania", "44": "Rhode Island", "45" : "South Carolina", "46": "South Dakota", "47": "Tennessee", "48": "Texas", "49" : "Utah", "50": "Vermont", "51": "Virginia", "53": "Washington", "54": "West Virginia", "55": "Wisconsin", "56":"Wyoming", "72":"Puerto Rico"}

    return states[code]

# Create some session state variables to track user interaction
if "first_time" not in st.session_state: # If this is the first time loading the script, track that
    st.session_state["first_time"] = True
if "state_data" not in st.session_state: # If we haven't loaded state data before, get ready to
	  st.session_state["state_data"] = None
if "county_data" not in st.session_state: # If we haven't loaded state data before, get ready to
	  st.session_state["county_data"] = None
        

@st.cache_data
def load_states_gdf():
    '''
    Reads the GeoJSON containing state data and returns a GeoDataFrame with that data
    '''
    # Create GeoDataFrame for states
    states_gdf = geopandas.read_file(
        "https://raw.githubusercontent.com/python-visualization/folium-example-data/main/us_states.json",
        driver="GeoJSON",
    )
    return states_gdf

@st.cache_data
def load_counties_gdf():
    '''
    Reads the GeoJSON containing county data and returns a GeoDataFrame with that data
    '''
    # Read counties GeoJSON
    f = open("../data/counties.geojson",)
    data = json.load(f)

    # Add state names to each county name in counties.geojson
    for feature in data["features"]:
        feature['properties']['NAME'] = feature['properties']['NAME'] + ", " + \
            convert_state_fp(feature['properties']['STATEFP'])

    f.close()

    # Create GeoDataFrame for counties
    counties_gdf = geopandas.GeoDataFrame.from_features(data["features"])
    counties_gdf = counties_gdf.set_crs("EPSG:4326")
    
    return counties_gdf

if st.session_state["first_time"]:
    st.session_state["state_data"] = load_states_gdf()
    st.session_state["county_data"] = load_counties_gdf()
    st.session_state["first_time"] = False

# Create map
m = folium.Map(location=[38, -97], zoom_start=4)

# Add counties to map
county_geo = folium.GeoJson(
    st.session_state["county_data"],
    zoom_on_click=True,
    name="US Counties",
    style_function=lambda feature: {
        "fillColor": UNSELECTED_FILL,
        "color": UNSELECTED_OUTLINE,
        "weight": 1,
        "fillOpacity": 0,
    },
    highlight_function=lambda feature: {
        "fillColor": HIGHLIGHT_FILL,
        "color": HIGHLIGHT_OUTLINE,
        "weight": 2,
        "fillOpacity": 0.2,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["NAME"], aliases=[""], localize=True
    ),
).add_to(m)

# Add states to map
state_geo = folium.GeoJson(
    st.session_state["state_data"],
    zoom_on_click=True,
    name="US States",
    style_function=lambda feature: {
        "fillColor": UNSELECTED_FILL,
        "color": UNSELECTED_OUTLINE,
        "weight": 2,
        "fillOpacity": 0,
    },
    highlight_function=lambda feature: {
        "fillColor": HIGHLIGHT_FILL,
        "color": HIGHLIGHT_OUTLINE,
        "weight": 2,
        "fillOpacity": 0.2,
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["name"], aliases=[""], localize=True
    ),
).add_to(m)

# Get list of counties in the format COUNTY, STATE
url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
all_counties = pd.read_csv( url )
column_1 = 'County'
column_2 = 'FAC_STATE'
all_counties['County_Pairs'] = all_counties[column_1] + ', ' + all_counties[column_2]
county_list = all_counties['County_Pairs']
county_list = set(county_list)
user_selection = st.selectbox("", county_list, index= None, placeholder="Search for a state or county")
user_selection = str(user_selection)
comma_pos = user_selection.find(',')
selected_state = user_selection[comma_pos + 2:]
selected_county = user_selection[:comma_pos].split(" ")
for countyName in range(len(selected_county)):
      selected_county[countyName] = selected_county[countyName][0] + (selected_county[countyName][1:]).lower() + " "
selected_county = "".join(str(l) for l in selected_county)[:-1]

if len(user_selection) > 0:
    f = open("../data/uscounties.csv")
    df = pd.read_csv(f)
    lat = df[(df["county_ascii"] == selected_county) & (df["state_id"] == selected_state)]["lat"]
    st.write((df["county_ascii"] == selected_county) & (df["state_id"] == selected_state))
    st.write(df["state_id"] == selected_state)
    st.write(lat)
    lng = df[(df["county"] == "".join(selected_county)) & df["state_id"] == selected_state]["lng"]
    st.write(lng)


# folium.Marker([float(lat), float(lng)]).add_to(m)


# Display the map
folium.LayerControl().add_to(m)

st_data = st_folium(m, width=725, returned_objects=[])