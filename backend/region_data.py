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
    st.write("yippee2")

try:
    repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
    st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
except git.GitCommandError:
    g = git.cmd.Git("ECHO_Modules")
    g.pull()
    st.write("yippee2")

from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_modules.ECHO_modules.geographies import states


programs = ['CAA', 'CWA', 'RCRA']
this_state = 'NY'
this_county = 'Kings'
region = Region(type='County', state=this_state,
                value=this_county, programs=programs)

df = region.get_per_1000('violations', 'USA', 2020)
st.write("USA violations")
st.write(df)
df = region.get_per_1000('violations', 'State', 2020)
st.write("State violations - {}".format(this_state))
st.write(df)

all_df = pd.DataFrame(columns=['State', 'Program', 'Per1000'])
df_list = []
for this_state in states:
    region = Region(type='State', state=this_state,
                    programs=programs)
    df = region.get_per_1000('violations', 'State', 2020)
    df.insert(0, 'State', this_state)
    df_list.append(df)
all_df = pd.concat(df_list)
st.write(all_df)
all_df.to_json('state_violations.json', orient='records')
all_df.to_csv('state_violations.csv')

# test


def get_sidebar_info(county_name, types):

    def get_county(row, state):
        programs = ['CAA', 'CWA', 'RCRA']
        region = Region(type='County', state=state, value=row[1].county,
                        programs=programs)
        df = region.get_per_1000(
            type=types, region='County', year=2022)
        df.insert(0, 'State', state)
        df.insert(1, 'County', row[1].county)
        return df

    state = 'NY'
    region = Region(type='None')
    counties = region.get_counties_by_state(state)
    print(counties)

    all_df = pd.DataFrame(columns=['State', 'County', 'Program', 'Per1000'])
    df_list = []
    for row in counties.iterrows():
        df = get_county(row, state)
        df_list.append(df)
    all_df = pd.concat(df_list)

    result = {}

    result['CAA'] = all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'CAA')]['Per1000'].values[0]
    result['CWA'] = all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'CWA')]['Per1000'].values[0]
    result['RCRA'] = all_df[(all_df['County'] == county_name) & (
        all_df['Program'] == 'RCRA')]['Per1000'].values[0]

    return result


st.write(get_sidebar_info('ALBANY', 'violations'))
