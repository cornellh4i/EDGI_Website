import pdb
import os
import streamlit as st
import pandas as pd
import altair as alt

from EEW_County_ReportCards.Region import Region
from EEW_County_ReportCards.AllPrograms_util import get_region_rowid
from ECHO_modules.geographies import states

def get_sidebar_grades(state_name, county_name, types):

    def get_county(row, state):
        programs = ['CAA', 'CWA', 'RCRA']
        region = Region(type='County', state=state, value=row[1].county,
                        programs=programs)
        df = region.get_per_1000(
            type=types, region='County')
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

def get_graphs(county, state, data_type):
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
        
        local_events = local_region.get_events(data_type, program)
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


get_graphs("ALBANY", "NY", "inspections")
    

