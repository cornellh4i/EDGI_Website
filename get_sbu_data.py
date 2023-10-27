import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import FastMarkerCluster
from streamlit_folium import st_folium
from ECHO_modules.get_data import get_echo_data # Import the get_echo_data function, which is the function that does the work of retrieving data from the SBU database
from ECHO_modules.get_data import get_spatial_data # Import this function, which will help us get county boundaries
from ECHO_modules.geographies import spatial_tables, fips, region_field, states # Import for mapping purposes

# Styles for States ("other") and selected regions (e.g. Zip Codes) - "this"
map_style = {'this': {'fillColor': '#0099ff', 'color': '#182799', "weight": 1},
'other': {'fillColor': '#FFA500', 'color': '#182799', "weight": 1}}

selected_state = st.selectbox(
    'Select a state',
    states)

# Get list of counties for selected state
url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
df = pd.read_csv( url )
counties = df[df['FAC_STATE'] == selected_state]['County']
counties = counties.unique()

selected_county = st.selectbox(
    'Select a county',
    counties)

st.write('You selected:', selected_county, ", ", selected_state)

def format_county(selected_county):
    '''
    Returns the formatted county string from uppercase to lowercase and capitalized
    Example: format_county('SAN FRANCISCO') returns 'San Francisco'
    '''
    format_county = ''
    county_words = selected_county.split(' ')
    for word in county_words:
        format_county += word.lower().capitalize() + ' '
    format_county = format_county[:-1]
    return format_county

format_county = format_county(selected_county)


st.header('Get Facilities in Selected County')
#sql = 'select * from "ECHO_EXPORTER" where "FAC_COUNTY" = \'TOMPKINS\' and "FAC_STATE" = \'NY\'' # "ECHO_EXPORTER" contains basic info about all regulated industrial facilities, including location
#fac = get_echo_data(sql)
"""Note: because of errors in the EPA's own data, the above query may not always return accurate results.
For instance, sometimes county names are listed as just "Tompkins"; sometimes they are listed as "Tompkins County".
A more robust version utilizes another approach. See below:
"""
# Get county names based on Steve's work. If we know our county of interest is Tompkins, NY, we can search for other names it may be listed under
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
print(sql)
fac = get_echo_data(sql)
fac


st.header('Get County Boundaries')
# This one gets a little complicated because of how the data are structured and the fact that a county name may not be unique (e.g. there are multiple Cedar Counties in the US
statefp = fips[selected_state] # Get state's code
sql = 'select * from "tl_2020_us_county" where "name" = \''+format_county +'\' and "statefp" = \''+str(statefp)+'\'' # Select specific county depending on state code
county, state = get_spatial_data("County", [selected_state], spatial_tables, fips, format_county)
county


def marker_text( row, no_text ):
    '''
    Create a string with information about the facility or program instance.

    Parameters
    ----------
    row : Series
        Expected to contain FAC_NAME and DFR_URL fields from ECHO_EXPORTER
    no_text : Boolean
        If True, don't put any text with the markers, which reduces chance of errors 

    Returns
    -------
    str
        The text to attach to the marker
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
    show the map of region(s) (e.g. zip codes) and points (e.g. facilities within the regions)
    create the map using a library called Folium (https://github.com/python-visualization/folium)
    bounds can be preset if necessary
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
    #kwargs={"disableClusteringAtZoom": 10, "showCoverageOnHover": False}
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
data = get_echo_data(sql)
data
