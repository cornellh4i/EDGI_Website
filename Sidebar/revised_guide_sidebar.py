import streamlit as st
import folium
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static
from ECHO_modules.ECHO_modules.geographies import states


# Initialize a session state variable that tracks the sidebar state
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config
st.set_page_config(layout="wide")

selected_state = st.selectbox("States", states)

# url stores the link in which we are getting county names from
url = "https://raw.githubusercontent.com/edgi-govdata-archiving/"
url += "ECHO_modules/packaging/data/state_counties_corrected.csv"
# reading the csv
df = pd.read_csv(url)
# counties of the selected state
counties = df[df['FAC_STATE'] == selected_state]['County']
# remove redundant counties
counties = counties.unique()
# display the select box with the counties option
selected_county = st.selectbox(
    "County", counties
)

# Create a Folium map that is zoomed-in a bit
map = folium.Map(location=[0.0, 0.0], zoom_start=2, use_container_width=True)

# Define the HTML template with CSS to make the map full-screen
map_html = """
<style>
body {
    padding: 0;
    margin: 0;
    overflow: hidden;
}
iframe {
    width: 100%;
    min-height: 400px;
    height: 600px;
    border: none;
    position: relative;
    z-index: 1;
}
</style>
"""
st.markdown(map_html, unsafe_allow_html=True)

# Display the map using st_folium
folium_static(map)

# this is for the button
if 'button' not in st.session_state:
    st.session_state.button = False

# Helper function to open/close the sidebar when the user presses the button


def click_button():
    st.session_state.button = not st.session_state.button


# The button itself styled
m = st.markdown("""
<style>
div.stButton > button:first-child {
    color: #3A7568;
    border: #3A7568;
    background: white;
    border-radius: 50%; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    border: 2px solid #3A7568;
    width: 70px;
    height: 70px; 
    position: relative;
    z-index: 2;
}
</style>""", unsafe_allow_html=True)
st.button('Open Guide', on_click=click_button,)


# Function to display words to the left and circles with text to the right
def display_words_and_circles(word, number):
    st.write(f'<div style="display: flex; align-items: center;">\
    <div style="margin-right: 20px;"><h1>{word}</h1></div>\
    <div style="\
    width: 60px; \
    height: 60px; \
    background-color: #808080; \
    border-radius: 50%; \
    display: flex; \
    align-items: center; \
    justify-content: center; \
    color: white; \
    font-weight: bold; \
    margin-left: auto; \
    font-size: 20px;">{number}</div>\
  </div>', unsafe_allow_html=True)


def violations(per_fac, per_insp, per_enfo):
    with st.container():
        display_words_and_circles("Violations per facility", per_fac)
    with st.container():
        display_words_and_circles("Violations per inspection", per_insp)
    with st.container():
        display_words_and_circles("Violations per enforcement", per_enfo)


def starter_top_info():
    st.title("How to use")

    # Define your content as a string
    content = """
  Zoom in or search to select a county to see county-specific data on violations, inspections, and enforcement actions by the EPA under the:
  - Clean Air Act (CAA)
  - Clean Water Act (CWA)
  - Resource Conservation and Recovery Act (RCRA)\n
  You can also click on a state to view its counties, and click on a county to view the data.\n
  Click on the circles within a county to zoom in and locate specific facilities. Hover over the facility’s circle to access its detailed ECHO report.
  """

    # Calculate the length of the content
    content_length = len(content)

    # Set the maximum width of the sidebar
    max_sidebar_width = 500

    # Calculate the sidebar width based on content length
    # Adjust the multiplier as needed
    sidebar_width = min(max_sidebar_width, content_length * 10)

    # Set the width of the sidebar
    st.markdown(
        f'<style>div.Widget.row-widget.stRadio > div {{ width: {sidebar_width}px !important; }}</style>', unsafe_allow_html=True)

    # Display the content
    st.markdown(content)


def gradingTabData(caa_fac, caa_insp, caa_enf, cwa_fac, cwa_insp, cwa_enf, rcra_fac, rcra_insp, rcra_enf):
    CAA, CWA, RCRA = st.tabs(["CAA", "CWA", "RCRA"])
    with CAA:
        violations(caa_fac, caa_insp, caa_enf)  # test
    with CWA:
        violations(cwa_fac, cwa_insp, cwa_enf)  # test
    with RCRA:
        violations(rcra_fac, rcra_insp, rcra_enf)  # test


def gradingTabInfo():
    # Define the CSS style for the gray rectangle
    gray_rectangle_style = """
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        color: black;
    """

    # Define the HTML content as a string
    html_content = f"""
    <div style="{gray_rectangle_style}">
        <subheader><b>Rationale for grading using these metrics:</b></subheader>
        <ul style: font-size: 12px>
            <li>More <b>violations per active facility</b> are worse</li>
            <li>More <b>inspections</b> mean more problems will be found, which is good. Dividing violations by inspections indicates the strength of the inspecting</li>
            <li>More <b>enforcements</b> when violations are found disincentivizes violating. Dividing violations by enforcements indicates the willingness to call fouls</li>
        </ul>
    </div>
    """

    # Use st.markdown to render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)


def highlightTabInfo():
    # Define the CSS style for the gray rectangle
    gray_rectangle_style = """
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        color: black;
    """

    # Define the HTML content as a string
    html_content = f"""
    <div style="{gray_rectangle_style}">
        <ul>
            <li> Comparing the first 3 years of the Obama administration to the first 3 years of the Trump administration, there has been a <b>2% decrease in inspections, 85% decrease in fines, and a 7% increase in enforcement actions.</b> </li>
            <li> Under the Clean Water Act, the law whose regulation is best documented by available EPA data, <b> 759 facilities</b>, representing 44% of all regulated facilities in [county name], were in violation for at least 9 months of the last 3 years. </li>
        </ul>
    </div>
    """

    # Use st.markdown to render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)


def highlightTabData():
    # Use st.markdown to render the HTML content
    st.markdown(
        """
    <div style="display: flex; align-items: center;">
        <div>
            <h1 style="margin-right: 10px;">Key: President</h1>
        </div>
        <div style="margin-left: auto; display: flex; align-items: center;">
            <div style="background-color: #8A6E95; width: 20px; height: 20px; margin: 0;"></div>
            <text style="margin: 5px; font-size: 20px;">Bush</text>
            <div style="background-color: #89BAB9; width: 20px; height: 20px; margin: 0;"></div>
            <text style="margin: 5px; font-size: 20px;">Obama</text>
            <div style="background-color: #E4AA7A; width: 20px; height: 20px; margin: 0;"></div>
            <text style="margin: 5px; font-size: 20px;">Trump</text>
        </div>
    </div>
    """,
        unsafe_allow_html=True
    )

    st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Mostly complete data<subtitle>",
                unsafe_allow_html=True)
    # this is a filler graph
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
    st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Potentially incomplete data<subtitle>",
                unsafe_allow_html=True)
    # this is a filler graph
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
    st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Mostly incomplete data<subtitle>",
                unsafe_allow_html=True)
    # this is a filler graph
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)


def comparisonTabInfo():
    # Define the CSS style for the gray rectangle
    gray_rectangle_style = """
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        color: black;
    """

    # Define the HTML content as a string
    html_content = f"""
    <div style="{gray_rectangle_style}">
        <ul>
            <li>These two charts show how inspections and violations in this state compare to the national average per 1000 facilities in 2022</li>
            <li>We use data from 2022 as it was the most recent full year and the ECHO database only reports currently active facilities</li>
            <li>To enable comparison across locations with a differing number of active facilities, we standardize the comparison to a value per 1000 facilities, proportionally adjusting the data if there are more or less than 1000 facilities in a district or state</li>
        </ul>
    </div>
    """

    # Use st.markdown to render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)


def comparisonTabData():
    st.markdown("<h2 style='text-align: center'>Inspections per 1000 Facilities (2022)</h2>",
                unsafe_allow_html=True)
    # this is where graph for CAA Violators
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
    st.markdown("<h2 style='text-align: center'>Violations per 1000 Facilities in 2022</h2>",
                unsafe_allow_html=True)
    # this is where graph for CWA Violators
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)


def non_complianceTabInfo():
    # Define the CSS style for the gray rectangle
    gray_rectangle_style = """
        background-color: #e6e6e6;
        padding: 10px;
        border-radius: 5px;
        color: black;
    """

    # Define the HTML content as a string
    html_content = f"""
    <div style="{gray_rectangle_style}">
        <ul>
            <li>Noncompliance is ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</li>
            <li>These figures show the ten facilities in this state with the worst history of environmental compliance based on their number of noncompliant quarters in the past 3 years (not necessarily consecutive). Click on a facility name to view its ECHO report.</li>
        </ul>
    </div>
    """

    # Use st.markdown to render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)


def non_complianceTabData():
    st.markdown("<h2 style='text-align: center'>CAA Violators</h2>",
                unsafe_allow_html=True)
    # this is where graph for CAA Violators
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
    st.markdown("<h2 style='text-align: center'>CWA Violators</h2>",
                unsafe_allow_html=True)
    # this is where graph for CWA Violators
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
    st.markdown("<h2 style='text-align: center'>RCRA Violators</h>",
                unsafe_allow_html=True)
    # this is where graph for RCRA Violators
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)

# Bottom info for the tabs


def bottom_info():
    st.header("")  # creates a gap

    # Define a CSS style for the gray rectangle with curved edges
    gray_rectangle_style = """
    background-color: #e6e6e6;
    padding: 10px;
    border-radius: 5px;
    color: black;
    font-size: 12px;
  """

    # text for the bottom of the page
    text = """The reliability of data in figures throughout this report is 
  indicated by the figure subtitle and degree of transparency. See the Data 
  Limitations section to view the transparency-coding table. Access state and 
  congressional district data here."""

    # Use st.markdown to display the gray rectangle with text
    st.markdown(
        f'<div style="{gray_rectangle_style}">{text}</div>', unsafe_allow_html=True)
    st.header("")  # creates a gap

# data visualization for the sidebar

from region_data import get_sidebar_grades


def fillSideBar(county=None, state=None, CAA_value=0, CWA_value=0, RCRA_value=0):
    if st.session_state.button:
        # User opens the sidebar
        with st.sidebar:
            if county is None or state is None:
                starter_top_info()
            else:
                st.title(county)
                st.subheader(state)
                st.header("")  # Add an empty line to create space
                st.header("Operating Facilities")
                st.subheader("CAA: " + str(CAA_value))
                st.subheader("CWA: " + str(CWA_value))
                st.subheader("RCRA: " + str(RCRA_value))
                with st.container():
                    grading, highlight, comparison, non_compliance = st.tabs(
                        ["Grading", "Highlights", "In Comparison", "Recent Non-Compliance"])
                    with grading:
                        violations_caa = get_sidebar_grades(
                            selected_state, selected_county, 'violations')['CAA']
                        violations_cwa = get_sidebar_grades(
                            selected_state, selected_county, 'violations')['CWA']
                        violations_rcra = get_sidebar_grades(
                            selected_state, selected_county, 'violations')['RCRA']
                        inspections_caa = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['CAA']
                        inspections_cwa = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['CWA']
                        inspections_rcra = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['RCRA']
                        enforcements_caa = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['CAA']
                        enforcements_cwa = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['CWA']
                        enforcements_rcra = get_sidebar_grades(
                            selected_state, selected_county, 'inspections')['RCRA']
                        gradingTabData(violations_caa, inspections_caa, enforcements_caa, violations_cwa, inspections_cwa, enforcements_cwa, violations_rcra, inspections_rcra, enforcements_rcra)
                        bottom_info()
                        gradingTabInfo()

                    with highlight:
                        highlightTabData()
                        bottom_info()
                        highlightTabInfo()

                    with comparison:
                        comparisonTabData()
                        bottom_info()
                        comparisonTabInfo()

                    with non_compliance:
                        non_complianceTabData()
                        bottom_info()
                        non_complianceTabInfo()

from region_data import get_number_facs

# Information that is shown when button is clicked
if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
        # fillSideBar() #starter
        fillSideBar(selected_county, selected_state, get_number_facs(selected_state, selected_county, 'CAA'), get_number_facs(selected_state, selected_county, 'CWA'), get_number_facs(selected_state, selected_county, 'RCRA'))
