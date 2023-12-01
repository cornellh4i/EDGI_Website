import streamlit as st
import folium
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import folium_static

with open("C:\\Users\\yummy\\OneDrive\\Documents\\h4i\\EDGI_Website\\style.css") as f:
    st.markdown(
        f"""<style>{f.read()}</style> <body>

</body>""",
        unsafe_allow_html=True,
    )
