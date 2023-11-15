import streamlit as st
import pandas as pd
from ECHO_modules.geographies import states as state_abbreviations # Import US state abbreviations for help
from searchbox_funcs import bivariate_map, format_county, get_facilities, get_county_boundaries, get_justice_data
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create some session state variables to track user interaction
if "first_time" not in st.session_state: # If this is the first time loading the script, track that
	  st.session_state["first_time"] = True 
if "county_list" not in st.session_state: # If we haven't loaded county names before, get ready to
	  st.session_state["county_list"] = None

# Initial data load
@st.cache_data
def load_county_list():
    '''
    Load data from state_counties_csv on first time running the app
    '''
    # Get list of counties in the format COUNTY, STATE
    url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
    url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
    all_counties = pd.read_csv( url )
    # Data pre-processing - make sure the only states in the list are real states, but comparing with the fips data
    all_counties = all_counties.loc[all_counties["FAC_STATE"].isin(state_abbreviations)]

    column_1 = 'County'
    column_2 = 'FAC_STATE'
    # combine county and state columns
    all_counties['County_Pairs'] = all_counties[column_1] + ', ' + all_counties[column_2]
    county_list = all_counties['County_Pairs']
    # filter duplicates
    county_list = county_list.unique()

    return county_list

## Only load counties if this is the first run through of the script
if st.session_state["first_time"]:
    st.session_state["county_list"] = load_county_list()
    st.session_state["first_time"] = False

# Let user select county
user_selection = st.selectbox(
    'Search for a county',
    st.session_state["county_list"]
)

comma_pos = user_selection.find(',')
# Extract state and county from user's selection
selected_state = user_selection[comma_pos + 2:]
selected_county = user_selection[:comma_pos]
county_name = format_county(selected_county)

# handle errors with empty columns
try:
    st.markdown('### Get Facilities in Selected County')
    fac = get_facilities(selected_county, selected_state)
    # Display facilities
    fac

    st.markdown('### Get County Boundaries')
    county, state = get_county_boundaries(county_name, selected_state)
    # Display county boundaries
    county

    st.markdown('### Map Boundaries and Facilities')
    # Display map of facilities in the county
    bivariate_map(county, fac)
except:
    st.warning("### No columns to parse from file")

try:
    st.markdown("### Get Environmental Justice Data")
    justice_data = get_justice_data(county)
    # Display environmental justice data
    justice_data

except:
    st.warning("### No columns to parse from file")
