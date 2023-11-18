import json
import git
import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


try:
    repo_link = "https://github.com/edgi-govdata-archiving/EEW_County_ReportCards"
    repo = git.Repo.clone_from(repo_link, "EEW_County_ReportCards")
except git.GitCommandError:
    g = git.cmd.Git("EEW_County_ReportCards")
    g.pull()

try:
    repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
    repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
except git.GitCommandError:
    g = git.cmd.Git("ECHO_Modules.ECHO_modules")
    g.pull()

from ECHO_Modules.ECHO_modules.utilities import (
    show_region_type_widget,
    show_state_widget,
    show_pick_region_widget,
)
from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_Modules.ECHO_modules.geographies import states

programs = ["CAA", "CWA", "RCRA"]

st.title("Region Data")
st.write(
    """
This application uses the region.db SQLite database to look up data on regions.
You can select states or counties and get violations per 1000 facilities for each.
"""
)


# Select Region Type
region_type = st.selectbox("Region of interest", ["State", "County"])
selected_state = st.selectbox("States", states)

if region_type == "County":
    url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
    url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
    df = pd.read_csv( url )
    counties = df[df['FAC_STATE'] == selected_state]['County']
    counties = counties.unique()

    selected_counties = st.selectbox(
        "County", counties
    )


program = st.selectbox("Select program", ["CAA", "CWA", "RCRA"])
year = st.selectbox("Select year: ", [2020, 2021, 2022])



# given code 
def create_df( data_type, y_field ):
    usa_region = Region( type='Nation' )
    usa_num_facs = usa_region.get_active_facilities( program )
    usa_events = usa_region.get_events( data_type, program, 2021 )
    usa_events['USA'] = usa_events[y_field]/usa_num_facs

    state_events_dict = {}
    for state in states:
        state_region = Region( type='State', state=state,
                    programs=[program,] )
        state_num_facs = state_region.get_active_facilities( program )
        state_events = state_region.get_events( data_type, program, 2021 )
        state_events[ state ] = state_events[y_field]/state_num_facs
        state_events_dict[ state ] = state_events

    if ( region_type != 'State' ):
        local_region = Region( type=region_type, state=states[0], value=region_selected,
                             programs=[program,])
        local_num_facs = local_region.get_active_facilities( program )
        local_events = local_region.get_events( data_type, program, 2021 )
        local_events[ region_selected ] = local_events[y_field]/local_num_facs

    df_events = usa_events.drop( columns=y_field, axis=1 )
    for state_name,state_events in state_events_dict.items():
        df_events = df_events.merge( state_events[['Year',state_name]] )
    if ( region_type != 'State' ):
        df_events = df_events.merge( local_events[['Year',region_selected]])
    
    st.line_chart(df_events)
    return df_events








def run_data_analysis(selected_state, selected_counties):
    st.write(selected_state)
    st.write(selected_counties)
    st.write(program)
    if region_type == "State":
        region = Region(type=region_type, state=selected_state,
                        programs=program)
        # st.write(region)
    elif region_type == "County":
        region = Region(type=region_type, state=selected_state,
                        value=selected_counties, programs=program)
        # st.write(region)

    else:
        st.error("Please select a region type and corresponding area.")
        return

    df = region.get_per_1000('violations', 'USA', 2020)
    st.write(df)

    events = region.get_events('violations', program, year)
    st.line_chart(events)

    active_facilities = region.get_active_facilities(program)
    st.write("Active facilities: ", active_facilities)



if st.button("Run Analysis"):
    if region_type == "County":
        run_data_analysis(selected_state, selected_counties)
    else:
        run_data_analysis(selected_state, selected_counties=[])