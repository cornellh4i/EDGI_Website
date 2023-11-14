import streamlit as st
import folium
import pandas as pd
import numpy as np
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
body {
    padding: 0;
    margin: 0;
    overflow: hidden;
}
iframe {
    width: 100%;
    min-height: 400px;
    height: 600px;
}
</style>
"""
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


# Function to display words to the left and circles with text to the right
def display_words_and_circles(word,number):
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

def highlightTabData():
  # Define the colors and words
  colors = ["#8A6E95", "#89BAB9", "#E4AA7A"]
  words = ["Bush", "Obama", "Trump"]

  # Create a horizontal layout with colored boxes to the left of words
  st.markdown(
    """
    <style>
      .horizontal-layout {
        display: inline-flex;  
        align-items: center;
      }
      .color-box {
        width: 24px;
        height: 24px;
        margin-right: 10px;
      }
    </style>
    """,
    unsafe_allow_html=True
  )

  for color, word in zip(colors, words):
    st.markdown(
      f'<div class="horizontal-layout">'
      f'   <div class="color-box" style="background-color: {color};"></div>'
      f'   {word}'
      f'</div>',
      unsafe_allow_html=True,
  )
  
  st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Mostly complete data<subtitle>", unsafe_allow_html=True)
  # this is a filler graph
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
  st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Potentially incomplete data<subtitle>", unsafe_allow_html=True)
  # this is a filler graph
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
  st.markdown("<h2>Facility Inspections - CAA, CWA, RCRA</h2> <subtitle>Mostly incomplete data<subtitle>", unsafe_allow_html=True)
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
  st.markdown("<h2 style='text-align: center'>Inspections per 1000 Facilities (2022)</h2>", unsafe_allow_html=True)
  # this is where graph for CAA Violators
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
  st.markdown("<h2 style='text-align: center'>CWA Violators</h2>", unsafe_allow_html=True)
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
  st.markdown("<h2 style='text-align: center'>CAA Violators</h2>", unsafe_allow_html=True)
  # this is where graph for CAA Violators
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
  st.markdown("<h2 style='text-align: center'>CWA Violators</h2>", unsafe_allow_html=True)
  # this is where graph for CWA Violators
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
  st.markdown("<h2 style='text-align: center'>RCRA Violators</h>", unsafe_allow_html=True)
  # this is where graph for RCRA Violators
  chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
  st.bar_chart(chart_data)
   
# Bottom info for the tabs 
def bottom_info():
  st.header("") # creates a gap

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
        st.subheader(state)
        st.header("") # Add an empty line to create space
        st.header("Operating Facilities")
        st.subheader("CAA: " + str(CAA_value))
        st.subheader("CWA: " + str(CWA_value))
        st.subheader("RCRA: " + str(RCRA_value))
        with st.container():
          grading, highlight, comparison, non_compliance = st.tabs(["Grading", "Highlights", "In Comparison", "Recent Non-Compliance"])
          with grading:
            gradingTabData()
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

# Information that is shown when button is clicked
if st.session_state.button:
    # User opens the sidebar
    with st.sidebar:
      #fillSideBar() #starter
      fillSideBar("Niagara County","New York", 72, 73,74)