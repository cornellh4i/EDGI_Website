import streamlit as st
import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(initial_sidebar_state=st.session_state.sidebar_state, layout= 'wide')

# map
#TODO: do the style for map 
# Create a Folium map
map = folium.Map()

# Define the HTML template with CSS to make the map full-screen
map_html = """
<style>
iframe {
    width: 100%;
    min-height: 400px;
    height: 100%;
}
</style>
"""

# Display the HTML template with the CSS to make the map full-screen using st.markdown
st.markdown(map_html, unsafe_allow_html=True)

# Display the map using st_folium
st_data = folium_static(map)

#TODO: make the style for the button
# this is for the button
if 'button' not in st.session_state:
    st.session_state.button = False

# Helper function to open/close the sidebar when the user presses the button
def click_button():
    st.session_state.button = not st.session_state.button

# The button itself
st.button('Open Guide', on_click=click_button)

# TODO: need to add circles that can take on numbers

def violations(per_fac, per_insp, per_enfo):
  with st.container():
    st.header("Violations per facility")
  with st.container():
    st.header("Violations per inspection")
  with st.container():
    st.header("Violations per enforcement")

#TODO: get information for CAA, CWA, RCRA
def gradingTab(bottom_info): 
  st.header("") # creates a gap between
  col1, col2 = st.columns(2)
  with col1:
    with st.container():
      CAA, CWA, RCRA = st.tabs(["CAA", "CWA", "RCRA"])
      with CAA: 
        violations(17, 19,18) #test
      with CWA:
        violations(1, 2, 3) #test
      with RCRA:
        violations(7, 9,8) #test

  with col2:
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
        <ul>
            <li>More <b>violations per active facility</b> are worse</li>
            <li>More <b>inspections</b> mean more problems will be found, which is good. Dividing violations by inspections indicates the strength of the inspecting</li>
            <li>More <b>enforcements</b> when violations are found disincentivizes violating. Dividing violations by enforcements indicates the willingness to call fouls</li>
        </ul>
    </div>
    """

    # Use st.markdown to render the HTML content
    st.markdown(html_content, unsafe_allow_html=True)
  
  #bottom info
  st.header("") # creates a gap
  # Define a CSS style for the gray rectangle with curved edges
  gray_rectangle_style = """
    background-color: #e6e6e6;
    padding: 10px;
    border-radius: 5px;
    color: black;
  """

  # Use st.markdown to display the gray rectangle with text
  st.markdown(f'<div style="{gray_rectangle_style}">{bottom_info}</div>', unsafe_allow_html=True)

# data visualization for the sidebar
def fillSideBar(county=None, state=None, CAA_value = None, CWA_value = None, RCRA_value = None):
  if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
      if county is None or state is None:
        st.header("How to use")

        # Define your content as a string
        content = """
        Zoom in, search, or locate yourself and select a county or point to see county-specific data on violations, inspections, and enforcement actions under three laws:
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
      else:
        st.header(county)
        st.subheader(state)
        st.header("")# Add an empty line to create space
        #TODO: create a function that pulls data given the country and state
        st.header("Operating Facilities")
        st.text("CAA: " + str(CAA_value))
        st.text("CWA: " + str(CWA_value))
        st.text("RCRA: " + str(RCRA_value))
        with st.container():
          grading, highlight, compliance, non_compliance = st.tabs(["Grading", "Highlights", "District in Compliance", "Recent Non-Compliance"])

          with grading:
            #TODO: need a function here that grabs the information to be shown
            gradingTab("test")

          with highlight:
            pass

          with compliance:
            pass

          with non_compliance:
            pass


# Information that is shown when button is clicked
if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
      fillSideBar() #starter
      #fillSideBar("hi","test", 72, 73,74)