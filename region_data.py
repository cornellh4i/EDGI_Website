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
st.write(all_df)
all_df.to_json('state_violations.json', orient='records')
all_df.to_csv('state_violations.csv')
