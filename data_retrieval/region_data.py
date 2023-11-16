import json
import git
import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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
region_type_widget = show_region_type_widget(
    region_types=["County", "State"], default_value="County"
)
state_widget = None
# Select Region Type
region_type = st.selectbox("Region of interest", ["State", "County"])
selected_state = st.selectbox("States", states)

if region_type == "County":
    st.selectbox(
        "County",
    )


program = st.selectbox("Select program", ["CAA", "CWA", "RCRA"])
year = st.selectbox("Select year: ", [2020, 2021, 2022])
selected_counties = "Tompskins"

# region = Region(type="County", state="NY", value="Tompkins", programs=program)
# df = region.get_per_1000("violations", "USA", 2020)
# st.write(df)


def plot_data(title, data_frame):
    st.line_chart(data_frame)


def run_data_analysis(selected_state, selected_counties):
    st.write(selected_state)
    # st.write(selected_counties)
    st.write(program)
    if region_type == "State":
        region = Region(type="State", state="NY", programs=program)
        st.write(region)
    elif region_type == "County":
        region = Region(
            type="County",
            state=selected_state,
            value=selected_counties,
            programs=program,
        )
        st.write(region)

    else:
        st.error("Please select a region type and corresponding area.")
        return

    # this_state = 'NY'
    # this_county = 'Tompkins'
    # gitregion = Region(type='County', state=this_state, value=this_county,
    #                 programs=program)
    df = region.get_per_1000("violations", "USA", 2020)
    st.dataframe(df)
    # violations_per_1000 = region.get_per_1000('violations', region_type, 2020)
    # st.write("Violations per 1000 facilities", violations_per_1000)

    # recurring_violations = get_recurring_violations(program)
    # st.write("Recurring violations: ", recurring_violations)

    # inflation = get_inflation(2000)
    # plot_data("Inflation since 2000: ", inflation)

    events = region.get_events("violations", program, year)
    plot_data("Events: ", events)

    # non_compliants = get_non_compliants(program)
    # plot_data("Non-compliants: ", non_compliants)

    active_facilities = region.get_active_facilities(program)
    st.write("Active facilities: ", active_facilities)


if st.button("Run Analysis"):
    if region_type == "County":
        run_data_analysis(selected_state, selected_counties)
    else:
        run_data_analysis(selected_state, selected_counties=[])
