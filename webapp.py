import pandas as pd
import plotly.express as px
import streamlit as st 

#streamlit run webapp.py
st.set_page_config(page_title="Beam Deflection using FDM", page_icon=":bar_chart:", layout="wide")

# ---- SIDEBAR ----
st.sidebar.header("Please Select Parameters:")
Material = st.sidebar.selectbox(
    "Select the Material:",
    options=["Iron","Steel","Copper"]
)

corss_section = st.sidebar.selectbox(
    "Select the Cross Section Type:",
    options=["Circle","Square","rectangle"]
)

Length = st.sidebar.number_input(
    "the length of the rod in mm:",
    0,
    10000000,
    1000
)

Detail=st.sidebar.slider(
    "the number of nodes:",
    0,
    1000,
    50,
    50
)
# ---- MAINPAGE ----
st.title(":bar_chart: line Deflection using FDM")
st.markdown("##")


st.markdown("""---""")
