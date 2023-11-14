import streamlit as st
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# Initialize a session state variable that tracks the sidebar state
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config 
st.set_page_config(layout= "wide")

# Create a Folium map that is zoomed-in a bit
map = folium.Map(location=[0.0, 0.0], zoom_start=2)

# Define the HTML template with CSS to make the map full-screen
map_html = """
<style>
iframe {
    width: 100%;
    min-height: 400px;
    height: 600px;
}
</style>
"""
# Display the HTML template with the CSS to make the map full-screen using st.markdown
st.markdown(map_html, unsafe_allow_html=True)

# Display the map using st_folium
st_data = folium_static(map)

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
}
</style>""", unsafe_allow_html=True)
st.button('Open Guide', on_click=click_button,)

# TODO: need to add circles that can take on number
def violations(per_fac, per_insp, per_enfo):
  with st.container():
    st.header("Violations per facility")
  with st.container():
    st.header("Violations per inspection")
  with st.container():
    st.header("Violations per enforcement")


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
  sidebar_width = min(max_sidebar_width, content_length * 10)  # Adjust the multiplier as needed

  # Set the width of the sidebar
  st.markdown(f'<style>div.Widget.row-widget.stRadio > div {{ width: {sidebar_width}px !important; }}</style>', unsafe_allow_html=True)

  # Display the content
  st.markdown(content)

def gradingTabData():
  CAA, CWA, RCRA = st.tabs(["CAA", "CWA", "RCRA"])
  with CAA: 
    violations(17, 19,18) #test
  with CWA:
    violations(1, 2, 3) #test
  with RCRA:
    violations(7, 9,8) #test

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

# Bottom part of the tabs 
def bottom_info():
  st.header("") # creates a gap

  # Define a CSS style for the gray rectangle with curved edges
  gray_rectangle_style = """
    background-color: #EFEFEF;
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
  st.markdown(f'<div style="{gray_rectangle_style}">{text}</div>', unsafe_allow_html=True)
  st.header("") # creates a gap

# data visualization for the sidebar
def fillSideBar(county=None, state=None, CAA_value=0, CWA_value=0 , RCRA_value=0):
  if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
      if county is None or state is None:
        starter_top_info()
      else:
        st.title(county)
        st.header(state)
        st.header("")# Add an empty line to create space
        #TODO: create a function that pulls data given the country and state
        st.header("Operating Facilities")
        st.subheader("CAA: " + str(CAA_value))
        st.subheader("CWA: " + str(CWA_value))
        st.subheader("RCRA: " + str(RCRA_value))
        with st.container():
          grading, highlight, comparison, non_compliance = st.tabs(["Grading", "Highlights", "In Comparison", "Recent Non-Compliance"])
          with grading:
            #TODO: need a function here that grabs the information to be shown & need the links 
            gradingTabData()
            bottom_info()
            gradingTabInfo()

          with highlight:
            #TODO: make a highlightTabData() for the graphs
            bottom_info()
            highlightTabInfo()

          with comparison:
            #TODO: make a comparisonTabData() for the graphs
            bottom_info()
            comparisonTabInfo()
            

          with non_compliance:
            #TODO: make a complianceTabData() for the graphs
            bottom_info()


# Information that is shown when button is clicked
if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
      #fillSideBar() #starter
      fillSideBar("hi","test", 72, 73,74)