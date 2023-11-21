import json
import git
import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


# try:
#     repo_link = "https://github.com/edgi-govdata-archiving/EEW_County_ReportCards"
#     repo = git.Repo.clone_from(repo_link, "EEW_County_ReportCards")
# except git.GitCommandError:
#     g = git.cmd.Git("EEW_County_ReportCards")
#     g.pull()

# try:
#     repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
#     repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
# except git.GitCommandError:
#     g = git.cmd.Git("ECHO_Modules.ECHO_modules")
#     g.pull()

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

    selected_county = st.selectbox(
        "County", counties
    )
else:
    selected_county = []

program = st.selectbox("Select program", ["CAA", "CWA", "RCRA"])
year = st.selectbox("Select year: ", [2020, 2021, 2022])



# given code 
def create_df( data_type, y_field):
    usa_region = Region( type='Nation' )
    usa_num_facs = usa_region.get_active_facilities( program )
    usa_events = usa_region.get_events( data_type, program, 2021 )
    usa_events['USA'] = usa_events[y_field]/usa_num_facs

    state_events_dict = {}
    if (region_type == 'State'):
        # for state in states:
        state = selected_state
        st.write("state:", state)

        state_region = Region( type='State', state=state,
                    programs=program)
        state_num_facs = state_region.get_active_facilities( program )

        st.write("get_active_facilities: ", state_num_facs)

        state_events = state_region.get_events( data_type, program, 2021 )

        st.write(data_type)
        state_events[ state ] = state_events[y_field]/state_num_facs
        state_events_dict[ state ] = state_events


    if ( region_type != 'State' ):
        local_region = Region( type=region_type, state=selected_state, value=selected_county,programs=program)

        st.write(selected_county)

        local_num_facs = local_region.get_active_facilities( program )
        
        st.write("local_num_facs: ", local_num_facs)
        st.write(data_type)
        local_events = local_region.get_events( data_type, program, 2021 )
        local_events[ selected_county ] = local_events[y_field]/local_num_facs

    df_events = usa_events.drop( columns=y_field, axis=1 )
    for state_name,state_events in state_events_dict.items():
        df_events = df_events.merge( state_events[['Year',state_name]] )
    if ( region_type != 'State' ):
        df_events = df_events.merge( local_events[['Year',selected_county]])
    return df_events



df_events_inspections = create_df('inspections', 'Count')
st.line_chart(df_events_inspections.set_index('Year'))

df_events_violations = create_df( 'violations', 'Count')
st.line_chart(df_events_violations.set_index('Year')) 


df_events_enforcement = create_df( 'enforcements', 'Count' )
df_events = df_events_enforcement.drop( columns='Amount', axis=1)
st.line_chart(df_events_enforcement, x='Year', y='Amount' )

df_events_fines = create_df( 'enforcements', 'Amount' )
df_events = df_events_fines.drop( columns='Count', axis=1)
st.line_chart( df_events_fines, x='Year', y= 'Count')


local_region = Region(type='County', state=selected_state, value=selected_county,
            programs=programs )
st.write("get_per_1000")
df = local_region.get_per_1000('violations', 'State', 2022)
st.write(df)
st.bar_chart(df, x = "Program")