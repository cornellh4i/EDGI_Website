import pdb
import git
import os
import streamlit as st
# from ECHO_modules.geographies import states
import pandas as pd


try:
    repo_link = "https://github.com/edgi-govdata-archiving/EEW_County_ReportCards"
    st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "EEW_County_ReportCards")
except git.GitCommandError:
    g = git.cmd.Git("EEW_County_ReportCards")
    g.pull()
# except:
    # region = git.Git(
    #     "https://github.com/edgi-govdata-archiving/EEW-ReportCard-Data.git")
    # region.pull(
    #     "https://github.com/edgi-govdata-archiving/EEW-ReportCard-Data.git", "main", rebase=True)

# git.Repo.clone_from(
#     "https://github.com/edgi-govdata-archiving/ECHO_modules", "ECHO_modules")

try:
    repo_link = "https://github.com/edgi-govdata-archiving/ECHO_modules"
    st.write("yippee")
    repo = git.Repo.clone_from(repo_link, "ECHO_Modules")
except git.GitCommandError:
    g = git.cmd.Git("ECHO_Modules")
    g.pull()

from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_Modules.ECHO_modules.geographies import states


programs = ['CAA', 'CWA', 'RCRA']
this_state = 'NY'
this_county = 'Tompkins'
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
# print( "State violations - {}".format(this_state) )
# print(df)
st.write(all_df)
all_df.to_json('state_violations.json', orient='records')
all_df.to_csv('state_violations.csv')


# def get_county(row, state):
#     programs = ['CAA', 'CWA', 'RCRA']
#     region = Region(type='County', state=state, value=row[1].county,
#                     programs=programs)
#     df = region.get_per_1000(type='violations', region='County', year=2022)
#     df.insert(0, 'State', state)
#     df.insert(1, 'County', row[1].county)
#     return df


# state = 'NY'
# region = Region(type='None')
# counties = region.get_counties_by_state(state)
# print(counties)

# all_df = pd.DataFrame(columns=['State', 'County', 'Program', 'Per1000'])
# df_list = []
# for row in counties.iterrows():
#     df = get_county(row, state)
#     df_list.append(df)
# all_df = pd.concat(df_list)
# # Write the results to a file, two ways
# all_df.to_json('cd_violations.json', orient='records')
# all_df.to_csv('cd_violations.csv')
