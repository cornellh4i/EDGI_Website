import pdb
import os
import pandas as pd
import sqlite3
from AllPrograms_util import get_region_rowid, get_focus_year

# Global variable for the year of the report
Focus_Year = None

def get_inflation(db, base_year):
    # base_year is the year for which a dollar is a dollar
    base_year = int(base_year)
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    sql = 'select year, rate from inflation order by year desc'
    df_fac = pd.read_sql_query(sql, conn)
    print(df_fac)
    inflation_by_year = {}
    calculated_inflation = 1.0
    for idx, row in df_fac.iterrows():
        year = int(row['year'])
        if year > base_year:
            continue
        inflation_by_year[year] = calculated_inflation
        if year <= base_year:
            calculated_inflation *= 1.0 + .01 * row['rate']
    df = pd.DataFrame.from_dict(inflation_by_year, orient='index')
    df = df.sort_index()
    df.reset_index(inplace=True)
    df.columns = ['Year', 'rate']
    return df


class Region:
    '''
    This class represents the data associated with a particular
    region--a state, congressional district, watershed, etc.

    Attributes
    ----------
    type : str
        One of the supported region types--'Nation', 'State', 
        'Congressional District', 'Watershed', 'Zip Code'
    value : str
        The actual identifier of the region--e.g. the number of
        the congressional district, the watershed name
    state : str
        The two letter state abbreviation
    programs : str
        The EPA programs
    db_conn : SQLite connection
        The connection to the local SQLite database holding
        the region's data
    data_sets : list
        The DataSet objects for the region 
    '''

    def __init__(self, db='region.db', type=None, value=None, state=None, programs=None):

        import os.path

        # https://stackoverflow.com/questions/28126140/python-sqlite3-operationalerror-no-such-table
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "region.db")
        print(db_path)

        self.db = db_path  # the Sqlite3 database
        self.type = type  # Region type
        self.value = value  # Region instance
        self.state = state  # State
        self.programs = programs  # The EPA programs to include

        if type != None:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            self.region_id = get_region_rowid(cursor, self.type, self.state, self.value)
            conn.close()

    def get_focus_year():
        global Focus_Year
        if Focus_Year is None:
            Focus_Year = get_focus_year()
        return Focus_Year

    def get_counties_by_state(self, state):
        conn = sqlite3.connect(self.db)
        sql = 'select region as county from regions where state=\'{}\''\
              ' and region_type=\'County\''.format(state)
        df = pd.read_sql_query(sql, conn)
        return df

    def get_cds(self):
        conn = sqlite3.connect(self.db)
        sql = 'select state, cd from real_cds order by state, cd'
        df = pd.read_sql_query(sql, conn)
        return df

    def get_per_1000(self, type, region):
        # type is 'inspections' or 'violations'
        # region is 'USA', 'State', 'CD'
        # programs is a list of the programs to be included--CAA, CWA, etc.
        if (region == 'USA' or region == 'State'):
            return self._get_region_per_1000(type, region)
        # For CDs we can just use the per_fac table and
        # active_facilities for the region
        conn = sqlite3.connect(self.db)

        sql = 'select program as Program, 1000. * count as Per1000 from per_fac'
        sql += ' where region_id={} and type=\'{}\' and year={}'
        if (self.programs is not None):
            sql += ' and program in (\'{}\')'
            sql = sql.format(self.region_id, type, get_focus_year(), '\',\''.join(self.programs))
        else:
            sql = sql.format(self.region_id, type, get_focus_year())
        df = pd.read_sql_query(sql, conn)
        return df

    def _get_region_per_1000(self, type, region):
        # type is 'inspections' or 'violations'
        # region is 'USA', 'State', 'CD'
        conn = sqlite3.connect(self.db)

        sql = 'select program, sum(count) from active_facilities '
        if (self.programs is not None):
            sql += ' where program in (\'{}\') '
            sql = sql.format('\',\''.join(self.programs))
        if (region == 'State'):
            sql += ' and region_id in ( select rowid from regions '
            sql += ' where state=\'{}\' )'
            sql = sql.format(self.state)
        sql += ' group by program'
        df_fac = pd.read_sql_query(sql, conn)

        sql = 'select program, sum(count) from {} where year={}'
        if (region == 'State'):
            sql += ' and region_id in ( select rowid from regions '
            sql += ' where state=\'{}\' )'
            sql = sql.format(type, get_focus_year(), self.state)
        else:
            sql = sql.format(type, get_focus_year())
        if (self.programs is not None):
            sql += ' and program in (\'{}\')'
            sql = sql.format('\',\''.join(self.programs))
        sql += ' group by program'
        df_insp = pd.read_sql_query(sql, conn)

        df_joined = df_fac.join(
            df_insp.set_index(['program']),
            lsuffix='x',
            rsuffix='y',
            on=['program'])
        type_cap = type.capitalize()
        df_joined.columns = ['Program', 'Facilities', type_cap]
        df_joined['Per1000'] = 1000. * df_joined[type_cap] / df_joined['Facilities']
        df = df_joined.drop(['Facilities', type_cap], axis='columns')
        return df

    def get_recurring_violations(self, program):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        sql = 'select sum(count) from active_facilities where '
        if self.state is None:
            sql += ' program=\'{}\''
            sql = sql.format(program)
        else:
            sql += ' program=\'{}\' and region_id in ( select rowid from regions'
            sql += ' where state=\'{}\' )'
            sql = sql.format(program, self.state)
        cursor.execute(sql)
        fetched = cursor.fetchone()
        state_facilities = fetched[0]

        sql = 'select sum(violations) from recurring_violations where '
        if self.state is None:
            sql += ' program=\'{}\''
            sql = sql.format(program)
        else:
            sql += ' program=\'{}\' and region_id in ( select rowid from regions'
            sql += ' where state=\'{}\' )'
            sql = sql.format(program, self.state)
        cursor.execute(sql)
        fetched = cursor.fetchone()
        state_violators = fetched[0]
        data = [{'State': self.state, 'Facilities': state_violators,
                 'Percent': 100. * state_violators / state_facilities
                 if state_facilities > 0 else -1},
                ]

        if self.value is not None:
            sql = 'select violations, facilities from recurring_violations '
            sql += ' where program=\'{}\' and region_id={}'
            sql = sql.format(program, self.region_id)
            cursor.execute(sql)
            cd_fac_viol = cursor.fetchone()

            if cd_fac_viol is not None:
                data.append(
                    {'CD': '{}{}'.format(self.state, self.value),
                     'Facilities': cd_fac_viol[0],
                     '    Percent': 100. * cd_fac_viol[0] / cd_fac_viol[1]
                     if cd_fac_viol[1] > 0 else -1
                     }
                )

        df = pd.DataFrame(data)
        return df

    def get_events(self, event_type, program):
        conn = sqlite3.connect(self.db)

        if event_type == 'inspections':
            sql = 'select year Year, sum(count) Count from inspections'
        elif event_type == 'enforcements':
            sql = 'select year Year, sum(amount) Amount, sum(count) Count '
            sql += ' from enforcements'
        elif event_type == 'violations':
            sql = 'select year Year, sum(count) as Count from violations'
        else:
            return None
        if (self.value is None):
            # If state is None, get the count
            # for all regions in the USA
            if (self.state is None):
                sql += ' where '
            else:
                sql += ' where region_id in ( select rowid from regions where '
                sql += ' state=\'{}\') and '
                sql = sql.format(self.state)
        else:
            sql += ' where region_id={} and '
            sql = sql.format(self.region_id)
        sql += ' year <= {} '
        if (program != 'All'):
            sql += ' and program=\'{}\''
        sql += ' group by year'
        base_year = get_focus_year()
        if (program == 'All'):
            sql = sql.format(base_year)
        else:
            sql = sql.format(base_year, program)
        print(sql)
        df = pd.read_sql_query(sql, conn)
        if event_type == 'enforcements':
            pass # inflation table currently empty
            #self._apply_inflation(df, base_year)
        return df

    def _apply_inflation(self, df, base_year):
        inflation_df = get_inflation(self.db, base_year)
        for idx, row in df.iterrows():
            df.at[idx, 'Amount'] = row['Amount'] * \
                        inflation_df[inflation_df['Year'] == row['Year']]['rate'].iloc[0]

    def get_non_compliants(self, program):
        conn = sqlite3.connect(self.db)

        sql = 'select fac_name, noncomp_count, formal_action_count, dfr_url,'
        sql += ' fac_lat, fac_long from non_compliants where program=\'{}\''
        sql += ' and noncomp_count > 0'
        sql = sql.format(program)
        if (self.value is None):
            if (self.state is not None):
                # Look at the entire state
                sql += ' and region_id in (select rowid from regions where state=\'{}\')'
                sql = sql.format(self.state)
        else:
            sql += ' and region_id={}'
            sql = sql.format(self.region_id)
        return pd.read_sql_query(sql, conn).sort_values(by='noncomp_count',
                                                        ascending=False)

    def get_active_facilities(self, program, table='active_facilities'):
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        if (self.value is None):
            if (self.state is None):
                # Sum active facilities over all regions in the country
                sql = 'select sum(count) from {} where program=\'{}\''
                sql = sql.format(table, program)
            else:
                # Sum active facilities over all regions in the state
                sql = 'select sum(count) from {} where region_id in ('
                sql += ' select rowid from regions where state=\'{}\') and program=\'{}\''
                sql = sql.format(table, self.state, program)
        else:
            sql = 'select count from {} where region_id={}'
            sql += ' and program=\'{}\''
            sql = sql.format(table, self.region_id, program)
        cursor.execute(sql)
        fetch = cursor.fetchone()
        return fetch[0] if fetch else 0

    def get_ranked(self):
        conn = sqlite3.connect(self.db)

        state_columns = 'CAA_Insp_Rank, CAA_Viol_Rank, CAA_Enf_Rank, '
        state_columns += 'CWA_Insp_Rank, CWA_Viol_Rank, CWA_Enf_Rank, '
        state_columns += 'RCRA_Insp_Rank, RCRA_Viol_Rank, RCRA_Enf_Rank'
        cd_columns = 'CAA_Insp_Pct, CAA_Viol_Pct, CAA_Enf_Pct, '
        cd_columns += 'CWA_Insp_Pct, CWA_Viol_Pct, CWA_Enf_Pct, '
        cd_columns += 'RCRA_Insp_Pct, RCRA_Viol_Pct, RCRA_Enf_Pct'

        sql = ''
        if self.type == 'State':
            sql = 'select {} from state_per_1000 where "CD.State" = \'{}\''
            sql = sql.format(state_columns, self.state)
        elif self.type == 'Congressional District':
            sql = 'select {} from cd_per_1000 where "CD.State" = \'{}{}\''
            sql = sql.format(cd_columns, self.state, self.value)
        elif self.type == 'County':
            sql = 'select {} from county_per_1000 where "CD.State" = \'{}{}\''
            sql = sql.format(cd_columns, self.state, self.value)

        return pd.read_sql_query(sql, conn)
