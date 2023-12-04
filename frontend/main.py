from header import header
from footer_info import footer_info
from guide_sidebar import sidebar
import streamlit as st 

st.set_page_config(layout="wide")


with st.container():
    sidebar()
    footer_info()
header()



