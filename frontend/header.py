import streamlit as st

st.set_page_config(page_title="Page Title", layout="wide")

# Connect file to style.css
# FIX PATH AS NEEDED
with open("C:\\Users\\owenc\\Hack4Impact\\EDGI_Website\\css\\style.css") as f:
    st.markdown(
        f"""<style>{f.read()}</style> <body>

  </body>""",
        unsafe_allow_html=True,
    )

# Disable default navbar
st.markdown("""
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        .st-emotion-cache-2e90o1.ezrtsby2 {
            display: none;
        }
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
