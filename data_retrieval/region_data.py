from ECHO_modules.ECHO_modules.geographies import states
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from EEW_County_ReportCards.Region import Region
from ECHO_modules.ECHO_modules.utilities import (
    show_region_type_widget,
    show_state_widget,
    show_pick_region_widget,
)
import json
import git
import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# If you are running this script for the first time, you should expect the following after you the following block of code runs:
#  1. You should see the two new folders downloaded in the data_retrieval folder: ECHO_Modules and EEW_County_ReportCards.
#  2. There will probably be an error saying that "AllProgram_utils" doesn't exist. This is expected. Go to Region.py and replace "from AllPrograms_util import get_region_rowid" with "from .AllPrograms_util import get_region_rowid"
#  Everything should run now :)

try:
    repo_link = "https://github.com/edgi-govdata-archiving/EEW_County_ReportCards"
    st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "EEW_County_ReportCards")
except git.GitCommandError:
    g = git.cmd.Git("EEW_County_ReportCards")
    g.pull()

try:
    repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
    st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
except git.GitCommandError:
    g = git.cmd.Git("ECHO_Modules")
    g.pull()


# Defining a new variable that stores the list of programs
programs = ["CAA", "CWA", "RCRA"]

# Display the title of the page (Can be deleted in future use)
st.title("Region Data")
st.write(
    """
This application uses the region.db SQLite database to look up data on regions.
You can select states or counties and get violations per 1000 facilities for each.
"""
)


# Select Region Type:
region_type = st.selectbox("Region of interest", ["State", "County"])

# Regardless of region_type, a state must be selected. This stores the state selected by the user.
selected_state = st.selectbox("States", states)

# If region_type is County, we will display another selector containing options for the County
if region_type == "County":
    # url stores the link in which we are getting county names from
    url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
    url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
    # reading the csv
    df = pd.read_csv(url)
    # counties of the selected state
    counties = df[df['FAC_STATE'] == selected_state]['County']
    # remove redundant counties
    counties = counties.unique()
    # display the select box with the counties option
    selected_county = st.selectbox(
        "County", counties
    )
# If region_type is State, we will set selected_county to empty list to avoid later issues with data retrieval
else:
    selected_county = []

# displaying the selectbox for pragrams
program = st.selectbox("Select program", ["CAA", "CWA", "RCRA"])
# displaying the selectbox for years
year = st.selectbox("Select year: ", [2020, 2021, 2022])


# this is the function that creates the dataframe for States and County; data_type are types like "inspection", "vioaltions", etc. y_field is the column that we hope to DROP(y_field must be a valid column name)
def create_df(data_type, y_field):
    # This block of code retrieves nationwide data
    st.write("Nation Data")
    usa_region = Region(type='Nation')
    # nationwide active facilities
    usa_num_facs = usa_region.get_active_facilities(program)
    st.write("Nationwide active facilities: ", usa_num_facs)
    # nationwide data for the specified data_type
    usa_events = usa_region.get_events(data_type, program, year)
    usa_events['USA'] = usa_events[y_field]/usa_num_facs
    st.write("Nationwide ", data_type)
    st.bar_chart(usa_events, x="Year")

    # This block of code retrieves State or State & County data depending on the region_type

    # this variable is used to compose the final dataframe
    state_events_dict = {}

    # If the user chose to view State related data
    if (region_type == 'State'):

        # let state be the selected_state
        state = selected_state
        # display on the web
        st.write("state:", state)
        # create a Region object for the state
        state_region = Region(type='State', state=state,
                              programs=program)
        # calling the corresponding function to get the active facilities for the specified program in this Region object
        state_num_facs = state_region.get_active_facilities(program)
        # display the data on the web
        st.write("get_active_facilities: ", state_num_facs)
        # retrieve the events for the specified data_type, program and year
        state_events = state_region.get_events(data_type, program, year)
        # display the name of the data_type on web
        st.write(data_type)
        # creating the dataframe for this particular state
        state_events[state] = state_events[y_field]/state_num_facs
        # and populate the outputed dictionary
        state_events_dict[state] = state_events

    # if user is interested in Counties
    if (region_type != 'State'):
        # create a local region object
        local_region = Region(
            type=region_type, state=selected_state, value=selected_county, programs=program)
        # display the selected county
        st.write(selected_county)
        # retrieve the active facility number
        local_num_facs = local_region.get_active_facilities(program)
        # display on web
        st.write("local_num_facs: ", local_num_facs)
        # display the data_type
        st.write(data_type)
        # create datagframe for the county, of the specified program and year
        local_events = local_region.get_events(data_type, program, year)
        local_events[selected_county] = local_events[y_field]/local_num_facs

    # drop the y_field column
    df_events = usa_events.drop(columns=y_field, axis=1)
    # merging the dataframe using the data we retrieved from before
    for state_name, state_events in state_events_dict.items():
        df_events = df_events.merge(state_events[['Year', state_name]])
    if (region_type != 'State'):
        df_events = df_events.merge(local_events[['Year', selected_county]])
    return df_events


# retrieve and graph inspection amount
df_events_inspections = create_df('inspections', 'Count')
st.line_chart(df_events_inspections.set_index('Year'))

# retrieve and graph violation amount
df_events_violations = create_df('violations', 'Count')
st.line_chart(df_events_violations.set_index('Year'))

# retrieve and graph enforcements amount
df_events_enforcement = create_df('enforcements', 'Count')
df_events = df_events_enforcement.drop(columns='Amount', axis=1)
st.line_chart(df_events_enforcement, x='Year', y='Amount')

# retrieve and graph enforcements count
df_events_fines = create_df('enforcements', 'Amount')
df_events = df_events_fines.drop(columns='Count', axis=1)
st.line_chart(df_events_fines, x='Year', y='Count')


# this retrieves and displays the get_per_1000 data from violates
local_region = Region(type='County', state=selected_state, value=selected_county,
                      programs=programs)
st.write("get_per_1000")
df = local_region.get_per_1000('violations', 'State', year)
st.write(df)
st.bar_chart(df, x="Program")
