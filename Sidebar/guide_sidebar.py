import streamlit as st

# Initialize a session state variable that tracks the sidebar state (either 'expanded' or 'collapsed').
if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'expanded'

# Streamlit set_page_config method has a 'initial_sidebar_state' argument that controls sidebar state.
st.set_page_config(
    initial_sidebar_state=st.session_state.sidebar_state, layout='wide')

m = st.markdown("""
<style>
div.stButton > button:first-child {
    color: black;
    border-radius: 50%; 
}
</style>""", unsafe_allow_html=True)

# Show title and description of the app.
st.title('Example: Controlling sidebar programmatically')
st.sidebar.markdown(
    'This is an example Streamlit app to show how to expand and collapse the sidebar programmatically.')

button = st.button('Hello World')

# Toggle sidebar state between 'expanded' and 'collapsed'.
if button:
    st.session_state.sidebar_state = 'collapsed' if st.session_state.sidebar_state == 'expanded' else 'expanded'
    # Force an app rerun after switching the sidebar state.
    st.experimental_rerun()
