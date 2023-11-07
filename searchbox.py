import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from ECHO_modules.get_data import get_echo_data # This function does the work of retrieving data from the SBU database
from ECHO_modules.get_data import get_spatial_data # This function will help us get county boundaries
from ECHO_modules.geographies import spatial_tables, fips, region_field, states # Import for mapping purposes
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Styles for States ("other") and selected regions (e.g. Zip Codes) - "this"
map_style = {'this': {'fillColor': '#0099ff', 'color': '#182799', "weight": 1},
'other': {'fillColor': '#FFA500', 'color': '#182799', "weight": 1}}

# Get list of counties in the format COUNTY, STATE
url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
all_counties = pd.read_csv( url )
column_1 = 'County'
column_2 = 'FAC_STATE'
all_counties['County_Pairs'] = all_counties[column_1] + ', ' + all_counties[column_2]
county_list = all_counties['County_Pairs']
county_list = county_list.unique()

user_selection = st.selectbox(
    'Search for a county',
    county_list)
comma_pos = user_selection.find(',')
selected_state = user_selection[comma_pos + 2:]
selected_county = user_selection[:comma_pos]


def format_county(selected_county):
    '''
    Returns the county with the first letter of each word capitalized.

    Example: format_county('SAN FRANCISCO') returns 'San Francisco'
    '''
    res = ''
    county_words = selected_county.split(' ')
    for word in county_words:
        res += word.lower().capitalize() + ' '
    return res[:-1]

county_name = format_county(selected_county)


st.header('Get Facilities in Selected County')
# Get county names based on Steve's work.
counties = pd.read_csv("https://raw.githubusercontent.com/edgi-govdata-archiving/ECHO_modules/main/data/state_counties_corrected.csv") # Get a county name lookup
counties = counties.groupby(by=["FAC_STATE", "County", "FAC_COUNTY"]).count() # Restructure the data
counties = counties.iloc[(counties.index.get_level_values('County') == selected_county) & (counties.index.get_level_values('FAC_STATE') == selected_state)].reset_index() # Search for COUNTY, STATE
counties = list(counties["FAC_COUNTY"].unique()) # List FAC_COUNTY names in ECHO associated with COUNTY
# Format a sql query
c = "("
for county in counties:
  c += "\'"+county+"\',"
c = c[:-1] + ")"
sql = 'select * from "ECHO_EXPORTER" where "FAC_COUNTY" in ' + c + ' and "FAC_STATE" = \'' + selected_state + '\'' # "ECHO_EXPORTER" contains basic info about all regulated industrial facilities, including location
fac = get_echo_data(sql)
# display facilities in county
fac


st.header('Get County Boundaries')
# This one gets a little complicated because of how the data are structured and the fact that a county name may not be unique (e.g. there are multiple Cedar Counties in the US
statefp = fips[selected_state] # Get state's code
sql = 'select * from "tl_2020_us_county" where "name" = \''+county_name +'\' and "statefp" = \''+str(statefp)+'\'' # Select specific county depending on state code
county, state = get_spatial_data("County", [selected_state], spatial_tables, fips, county_name)
# display county boundaries
county


def marker_text( row, no_text ):
    '''
    Create a string with information about the facility or program instance.
    
    Returns the text (a str) to attach to the marker

    Parameters
    ----------
    row : Series
        Expected to contain FAC_NAME and DFR_URL fields from ECHO_EXPORTER
    no_text : Boolean
        If True, don't put any text with the markers, which reduces chance of errors 
    '''

    text = ""
    if ( no_text ):
        return text
    if ( type( row['FAC_NAME'] == str )) :
        try:
            text = row["FAC_NAME"] + ' - '
        except TypeError:
            print( "A facility was found without a name. ")
        if 'DFR_URL' in row:
            text += " - <p><a href='"+row["DFR_URL"]
            text += "' target='_blank'>Link to ECHO detailed report</a></p>" 
    return text


def bivariate_map(regions, points, bounds=None, no_text=False):
    '''
    Show the map of region(s) (e.g. zip codes) and points (e.g. facilities within the regions)

    Create the map using a library called Folium (https://github.com/python-visualization/folium)

    Bounds can be preset if necessary

    no_text errors can be managed
    '''
    m = folium.Map()  

    # Show the region(s
    s = folium.GeoJson(
      regions,
      style_function = lambda x: map_style['other']
    ).add_to(m)

    # Show the points
    ## Create the Marker Cluster array
    mc = FastMarkerCluster("")
 
    # Add a clickable marker for each facility
    for index, row in points.iterrows():
      if ( bounds is not None ):
        if ( not check_bounds( row, bounds )):
          continue
      mc.add_child(folium.CircleMarker(
        location = [row["FAC_LAT"], row["FAC_LONG"]],
        popup = marker_text( row, no_text ),
        radius = 8,
        color = "black",
        weight = 1,
        fill_color = "orange",
        fill_opacity= .4
      ))
    
    m.add_child(mc)

    # compute boundaries so that the map automatically zooms in
    bounds = m.get_bounds()
    m.fit_bounds(bounds, padding=0)

    # display the map!
    st_data = st_folium(m, width=725)

st.header('Map Boundaries and Facilities')
bivariate_map(county, fac)


st.header('Get Environmental Justice Data')
# Based on this https://www.census.gov/programs-surveys/geography/guidance/geo-identifiers.html
baseline = int(str(county["geoid"][0]) + "0000000") # Find the county's geoid and turn it into a 12 digit block group code
next = baseline + 10000000 # Find the next county's geoid - we don't want any of this so it's the limit of our query
sql = 'SELECT * from "EJSCREEN_2021_USPR" where "ID" between '+str(baseline)+' and '+str(next)+''
# The above query should give us all the block groups in the county, nothing more nothing less
justice_data = get_echo_data(sql)
# display environmental justice data
justice_data
