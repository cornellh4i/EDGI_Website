import pdb
import git
import os
import streamlit as st
import pandas as pd
import altair as alt


try:
    repo_link = "https://github.com/edgi-govdata-archiving/EEW_County_ReportCards"
    # st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "EEW_County_ReportCards")
except git.GitCommandError:
    g = git.cmd.Git("EEW_County_ReportCards")
    g.pull()

try:
    repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
    # st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
except git.GitCommandError:
    g = git.cmd.Git("ECHO_Modules")
    g.pull()

from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_modules.ECHO_modules.geographies import states




def get_sidebar_grades(state_name, county_name, types):

    def get_county(row, state):
        programs = ['CAA', 'CWA', 'RCRA']
        region = Region(type='County', state=state, value=row[1].county,
                        programs=programs)
        df = region.get_per_1000(
            type=types, region='County', year=2022)
        df.insert(0, 'State', state)
        df.insert(1, 'County', row[1].county)
        return df

    state = state_name
    region = Region(type='None')
    counties = region.get_counties_by_state(state)

    all_df = pd.DataFrame(columns=['State', 'County', 'Program', 'Per1000'])
    df_list = []
    for row in counties.iterrows():
        df = get_county(row, state)
        df_list.append(df)
    all_df = pd.concat(df_list)

    result = {}

    result['CAA'] = int(all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'CAA')]['Per1000'].values[0])
    result['CWA'] = int(all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'CWA')]['Per1000'].values[0])
    result['RCRA'] = int(all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'RCRA')]['Per1000'].values[0])
    return result

def get_number_facs(state, county, program):
    local_region = Region(
        type='County', state=state, value=county, programs=program)    # retrieve the active facility number
    local_num_facs = local_region.get_active_facilities(program)
    return local_num_facs

def get_graphs(county,state, data_type):
    def create_df( data_type, y_field, program):
        # create a local region object
        local_region = Region(type='County', state=state, value=county, programs=program)
        # display the selected county
        # st.write(county)
        # retrieve the active facility number
        local_num_facs = local_region.get_active_facilities( program )
        # display the data_type
        # st.write(data_type)
        # create datagframe for the county, of the specified program and year
        local_events = local_region.get_events( data_type, program, 2022 )
        local_events[county ] = local_events[y_field]/local_num_facs
        df_events = local_events[['Year',county]]
        return df_events
    df_events_cwa = create_df( data_type, 'Count', "CWA" ).add_suffix("cwa")
    df_events_caa = create_df( data_type, 'Count', "CAA" ).add_suffix("caa")
    df_events_rcra = create_df( data_type, 'Count', "RCRA" ).add_suffix("rcra")

    sums_df = pd.concat([df_events_cwa, df_events_caa, df_events_rcra], axis=1)
    
    sums_df['total'] = sums_df[county + 'cwa'] + sums_df[county + 'caa'] + sums_df[county + 'rcra']
    sums_df = sums_df.rename(columns={"Yearcwa": "Year"})
    sums_df = sums_df.rename(columns={"total": data_type})
    return sums_df


    # # Setting 'ID' as the index for each DataFrame
    # df_events_cwa.set_index(county, inplace=True)
    # df_events_caa.set_index(county, inplace=True)
    # df_events_rcra.set_index(county, inplace=True)
    # # Creating a new DataFrame with the sum of values across DataFrames
    # sums_df = pd.DataFrame(index=set(df_events_cwa.index) | set(df_events_caa.index) | set(df_events_rcra.index))
    # sums_df['Total'] = df_events_cwa.get('Value_df1', 0) + df_events_caa.get('Value_df2', 0) + df_events_rcra.get('Value_df3', 0)

    # dfs = [df_events_cwa, df_events_caa, df_events_rcra]
    # concatenated_df = pd.concat(dfs, axis=0, ignore_index=True)
    # # Calculating the sum based on 'ID'
    # sums_df = concatenated_df.groupby(county).sum()
    
    # st.write(df_events_cwa)
    # st.write(df_events_caa)
    # st.write(df_events_rcra)
    # st.write(sums_df)
    # ylabel = '{} per facility'.format( data_type )

get_graphs("ALBANY", "NY", "inspections")
    

