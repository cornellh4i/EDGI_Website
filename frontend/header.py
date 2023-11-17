import streamlit as st
import streamlit as st

with open("C:\\Users\\yummy\\OneDrive\\Documents\\h4i\\EDGI_Website\\style.css") as f:
    st.markdown(
        f"""<style>{f.read()}</style> <body>

</body>""",
        unsafe_allow_html=True,
    )
