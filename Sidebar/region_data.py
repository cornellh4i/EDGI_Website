import pdb
import git
import os
import streamlit as st
import pandas as pd


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

