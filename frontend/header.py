import streamlit as st

with open("C:\\Users\\owenc\\Hack4Impact\\EDGI_Website\\css\\style.css") as f:
    st.markdown(
        f"""
  <style>{f.read()}</style>
  <body>
    <nav class="navbar">
      <h1 class="title">
        County Reports
      </h1>
      <a class="exit-button" href="https://www.environmentalenforcementwatch.org/data/notebooks/">
        Exit
      </a>
    </nav>
  </body>""",
        unsafe_allow_html=True,
    )