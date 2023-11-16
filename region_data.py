
import json
import git
import os
import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from ECHO_Modules.ECHO_modules.utilities import show_region_type_widget, show_state_widget, show_pick_region_widget
from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_Modules.ECHO_modules.geographies import states

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

# data = pd.read_csv('ECHO_Modules/data/state_counties_corrected.csv')

st.title("Region Data")
st.write("""
This application uses the region.db SQLite database to look up data on regions.
You can select states or counties and get violations per 1000 facilities for each.
""")
region = None
# Select Region Type
region_type = show_region_type_widget(["State", "County"])
selected_state = st.selectbox("Select states: ", states)
if region_type == "County":
    selected_counties = show_pick_region_widget(
        type="County", state_widget=[selected_state], multi=False)
program = st.selectbox("Select program", ['CAA', 'CWA', 'RCRA'])
year = st.selectbox("Select year: ", [2020, 2021, 2022])


# def get_per_1000(type, region, year):
#     if region_type == "County":
# s         region = Region(type='County', state=selected_state, value=selected_counties,
#                         programs=program)
#     else:
# s         region = Region(type='State', state=selected_state,
#                         programs=program)
#     df = region.get_per_1000('violations', 'USA', year)
#     st.write("USA violations")
#     st.write(df)
#     df = region.get_per_1000('violations', 'State', year)
#     st.write("State violations - {}".format(selected_state))
#     st.write(df)
#     if region_type == "County":
#         df = region.get_per_1000('violations', 'County', year)
#         st.write("County violations - {}".format(selected_counties))
#         st.write(df)
#     return df


def get_recurring_violations(program):
    if region_type == "County":
        region = Region(type='County', state=selected_state, value=selected_counties,
                        programs=program)
    else:
        region = Region(type='State', state=selected_state,
                        programs=program)
    df = region.get_recurring_violations(program)
    st.write("USA violations")
    st.write(df)
    df = region.get_recurring_violations(program)
    st.write("State violations - {}".format(selected_state))


def get_inflation(base_year):
    # base_year is the year for which a dollar is a dollar
    conn = sqlite3.connect("region.db")
    cursor = conn.cursor()

    sql = 'select year, rate from inflation order by year desc'
    df_fac = pd.read_sql_query(sql, conn)

    inflation_by_year = {}
    calculated_inflation = 1.0
    for row in df_fac:
        if row[year] > base_year:
            continue
        inflation_by_year[int(row['year'])] = calculated_inflation
        if row[year] <= base_year:
            calculated_inflation *= 1.0 + .01 * row['rate']
    df = pd.DataFrame.from_dict(inflation_by_year, orient='index')
    df = df.sort_index()
    df.reset_index(inplace=True)
    # df = df.reindex()
    # df.columns = ['Year', 'rate']
    # df = df.rename( columns=['Year', 'rate'])
    return df


def get_events(type, program, base_year):
    if region_type == "County":
        region = Region(type='County', state=selected_state, value=selected_counties,
                        programs=program)
    else:
        region = Region(type='State', state=selected_state,
                        programs=program)
    df = region.get_events('County', program, base_year)
    st.write("USA violations")
    st.write(df)
    df = region.get_events('County', program, base_year)
    st.write("State violations - {}".format(selected_state))
    st.write(df)


def get_non_compliants(program):
    region = Region(type='County', state=selected_state, value=selected_counties,
                    programs=program)
    df = region.get_non_compliants(program)
    st.write("USA violations")
    st.write(df)
    df = region.get_non_compliants(program)
    st.write("State violations - {}".format(selected_state))
    st.write(df)


def get_active_facilities(program, table='active_facilities'):
    if region_type == "County":
        region = Region(type='County', state=selected_state, value=selected_counties,
                        programs=program)
    else:
        region = Region(type='State', state=selected_state,
                        programs=program)
    df = region.get_active_facilities(program, table)
    st.write("USA violations")
    st.write(df)
    df = region.get_active_facilities(program, table)
    st.write("State violations - {}".format(selected_state))
    st.write(df)
    if region_type == "County":
        df = region.get_active_facilities(program, table)
        st.write("State violations - {}".format(selected_state))


state_widget = selected_state  # NY, or whatever

if (region_type == 'County'):
    region_widget = selected_counties

region_selected = None

# if (region_type != 'State'):
#     region_selected = region_widget


# def get_county(row, state):
#     programs = ['CAA', 'CWA', 'RCRA']
# n     region = Region(type='County', state=state, value=row,
#                     programs=programs)
#     df = region.get_per_1000(type='violations', region='County', year=2022)
#     df.insert(0, 'State', state)
#     df.insert(1, 'County', row)
#     return df


def plot_data(title, data_frame):
    st.line_chart(data_frame)


def run_data_analysis(selected_state, selected_counties):
    st.write(selected_state)
    st.write(selected_counties)
    st.write(program)
    if region_type == "State":
        region = Region(type="State", state='NY',
                        programs=program)
        st.write(region)
    elif region_type == "County":
        region = Region(type='County', state=selected_state,
                        value=selected_counties, programs=program)
        st.write(region)

    else:
        st.error("Please select a region type and corresponding area.")
        return

    # this_state = 'NY'
    # this_county = 'Tompkins'
    # region = Region(type='County', state=this_state, value=this_county,
    #                 programs=program)
    df = region.get_per_1000('violations', 'USA', 2020)
    st.write(df)
    # violations_per_1000 = region.get_per_1000('violations', region_type, 2020)
    # st.write("Violations per 1000 facilities", violations_per_1000)

    # recurring_violations = get_recurring_violations(program)
    # st.write("Recurring violations: ", recurring_violations)

    # inflation = get_inflation(2000)
    # plot_data("Inflation since 2000: ", inflation)

    events = region.get_events('violations', program, year)
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


# def create_df(data_type, y_field):
#     usa_region = Region(type='Nation')
#     usa_num_facs = usa_region.get_active_facilities(program)
#     usa_events = usa_region.get_events(data_type, program, 2021)
#     usa_events['USA'] = usa_events[y_field]/usa_num_facs

#     state_events_dict = {}
#     for state in states:
#         state_region = Region(type='State', state=state,
#                               programs=program)
#         state_num_facs = state_region.get_active_facilities(program)
#         state_events = state_region.get_events(data_type, program, 2021)
#         state_events[state] = state_events[y_field]/state_num_facs
#         state_events_dict[state] = state_events

#     if (region_type == 'County'):
#         local_region = Region(type=region_type, state=states, value=region_selected,
#                               programs=program)
#         local_num_facs = local_region.get_active_facilities(program)
#         local_events = local_region.get_events(data_type, program, 2021)
#         local_events[region_selected] = local_events[y_field]/local_num_facs

#     df_events = usa_events.drop(columns=y_field, axis=1)
#     for state_name, state_events in state_events_dict.items():
#         df_events = df_events.merge(state_events[['Year', state_name]])
#     if (region_type != 'State'):
#         df_events = df_events.merge(local_events[['Year', region_selected]])
#     return df_events


# df_inspections = create_df('inspections', 'Count')
# st.write("Inspections per Facility")
# st.line_chart(df_inspections, x='Year')

# df_violations = create_df('violations', 'Count')
# st.write("Violations per Facility")
# st.line_chart(df_violations, x='Year')

# df_enforcements = create_df('enforcements', 'Count')
# st.write("Enforcements per Facility")
# st.line_chart(df_enforcements, x='Year')

# df_fines = create_df('enforcements', 'Amount')
# st.write("Fines per Facility")
# st.line_chart(df_fines, x='Year')

# df_events = create_df('inspections', 'Count')
# ylabel = '{} per facility'.format('inspections')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('violations', 'Count')
# ylabel = '{} per facility'.format('violations')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('enforcements', 'Count')
# df_events = df_events.drop(columns='Amount', axis=1)
# ylabel = '{} per facility'.format('enforcements')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('enforcements', 'Amount')
# df_events = df_events.drop(columns='Count', axis=1)
# ylabel = '{} per facility'.format('fines')
# df_events.plot.line(x='Year', ylabel=ylabel)


# st.title("Graph inspections, violations, enforcements and fines per facility over time")
# region_type_widget = show_region_type_widget(
#     region_types=['County', 'State'], default_value='County')
# state_widget = None
# # state_widget = show_state_widget(multi=False)
# region_widget = None
# region_type = region_type_widget
# if (region_type != 'State'):
#     region_widget = show_pick_region_widget(type=region_type,
#                                             state_widget=state_widget, multi=False)
# states = state_widget if state_widget is not None else None
# region_selected = None
# if (region_type != 'State'):
#     region_selected = region_widget

# program_widget = st.multiselect(
#     options=['RCRA', 'CAA', 'CWA'],
#     label='Program:',
#     disabled=False,
# )


# def create_df(data_type, y_field):
#     usa_region = Region(type='Nation')
#     usa_num_facs = usa_region.get_active_facilities(program)
#     usa_events = usa_region.get_events(data_type, program, 2021)
#     usa_events['USA'] = usa_events[y_field]/usa_num_facs

#     state_events_dict = {}
#     for state in state_widget:
#         state_region = Region(type='State', state=state,
#                               programs=program)
#         state_num_facs = state_region.get_active_facilities(program)
#         state_events = state_region.get_events(data_type, program, 2021)
#         state_events[state] = state_events[y_field]/state_num_facs
#         state_events_dict[state] = state_events

#     if (region_type == 'County'):
#         local_region = Region(type=region_type, state=state_widget, value=region_selected,
#                               programs=program)
#         local_num_facs = local_region.get_active_facilities(program)
#         local_events = local_region.get_events(data_type, program, 2021)
#         local_events[region_selected] = local_events[y_field]/local_num_facs

#     df_events = usa_events.drop(columns=y_field, axis=1)
#     for state_name, state_events in state_events_dict.items():
#         df_events = df_events.merge(state_events[['Year', state_name]])
#     if (region_type != 'State'):
#         df_events = df_events.merge(local_events[['Year', region_selected]])
#     return df_events


# df_events = create_df('inspections', 'Count')
# ylabel = '{} per facility'.format('inspections')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('violations', 'Count')
# ylabel = '{} per facility'.format('violations')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('enforcements', 'Count')
# df_events = df_events.drop(columns='Amount', axis=1)
# ylabel = '{} per facility'.format('enforcements')
# df_events.plot.line(x='Year', ylabel=ylabel)

# df_events = create_df('enforcements', 'Amount')
# df_events = df_events.drop(columns='Count', axis=1)
# ylabel = '{} per facility'.format('fines')
# df_events.plot.line(x='Year', ylabel=ylabel)
