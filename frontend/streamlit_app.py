from header import header
from footer_info import footer_info
# from guide_sidebar import sidebar
from revised_guide_sidebar import data_sidebar
import streamlit as st 
from searchbox import create_searchbox

st.set_page_config(layout="wide")



 
# with st.container():

selected_state, selected_county = create_searchbox()
data_sidebar(selected_state, selected_county)
footer_info()
header()  



