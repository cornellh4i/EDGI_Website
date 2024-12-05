import streamlit as st

def header():

    
    # Connect file to style.css
    with open("./css/style.css") as f:
        st.markdown(
            f"""<style>{f.read()}</style>""",
            unsafe_allow_html=True,
        )
   
       # Disable default navbar
    st.markdown("""
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            .st-emotion-cache-2e90o1.ezrtsby2 {
                display: none;
            }
            .st-emotion-cache-18ni7ap.ezrtsby2 {
                display: none;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """, unsafe_allow_html=True)

    # Create navbar
    st.markdown("""
        <nav class="navbar">
        <h1 class="title">
            County Reports
        </h1>
        <a class="exit-button" href="https://www.environmentalenforcementwatch.org/data/notebooks/">
            Exit
        </a>
        </nav>
    """, unsafe_allow_html=True)

    