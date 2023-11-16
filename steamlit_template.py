"""
Streamlit Visualization Guide
------------------------------

This script (`streamlit_template.py`) shows some visualizations and different methods to make them

Installation
------------

Virtual Environment (Recommended):
    Before installing the dependencies, I recommend using a virtual environment.
    1. Install `virtualenv` if it's not installed:
        ```
        pip install virtualenv
        ```

    2. Create a virtual environment. Replace `env_name` with your desired environment name:
        ```
        python -m virtualenv env_name
        ```

    3. Activate the virtual environment:
        - Windows:
            ```
            env_name/Scripts/activate
            ```

        - macOS and Linux:
            ```
            source env_name/bin/activate
            ```

    If you're unfamiliar with virtual environments or encounter issues please let me (Jacob) know!

Installing Dependencies:
    Once the virtual environment is activated (or if you're skipping that step), install the dependencies:
        ```
        pip install -r requirements.txt
        ```

Running the Streamlit App
-------------------------

After installing the dependencies, you can run the Streamlit app with:
    ```
    streamlit run steamlit_template.py
    ```

This will start the Streamlit server, and the app should open in your default web browser
"""

# Import necessary libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# Streamlit title
st.title("Streamlit Visualization Guide")

# 1. Streamlit's built-in chart
st.subheader("1. Streamlit's built-in line chart")
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])
st.line_chart(chart_data)

# 2. Matplotlib
st.subheader("2. Matplotlib scatter plot")
fig, ax = plt.subplots()
ax.scatter(np.random.randn(50), np.random.randn(50), color='blue')
ax.set_title("Matplotlib Scatter Plot")
st.pyplot(fig)

# 3. Plotly
st.subheader("3. Plotly bar chart")
df = pd.DataFrame({
    'fruits': ['apple', 'banana', 'cherry', 'date'],
    'count': [10, 20, 30, 40]
})
fig = px.bar(df, x='fruits', y='count', title="Plotly Bar Chart")
st.plotly_chart(fig)

# 4. Altair
st.subheader("4. Altair area chart")
source = pd.DataFrame({
    'x': np.arange(100),
    'y': np.random.randn(100).cumsum()
})
area_chart = alt.Chart(source).mark_area().encode(
    x='x',
    y='y'
).properties(title="Altair Area Chart")
st.altair_chart(area_chart)
