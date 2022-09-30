import pandas as pd
import plotly.express as px
import streamlit as st 
import numpy as np

df = pd.DataFrame(
    np.random.randn(1, 5),
    columns=('col %d' % i for i in range(5)))
#streamlit run webapp.py
st.set_page_config(page_title="Beam Deflection using FDM", page_icon=":bar_chart:", layout="wide")

# ---- SIDEBAR ----

# ---- MAINPAGE ----
st.title(":bar_chart: line Deflection using FDM")

col_data_input, col_parameter = st.columns(2)

with col_data_input:
    st.header("Input Loads")
    if st.button('Define Loads'):
        with st.form("take load"):
            st.number_input("Length of load:",0,100,1,5,help="1 if it is a point load")
            
            st.number_input("Location of load:",0,100,50,5)
            
            st.number_input("Magnitude of load (in N):",0.0,10000.0,10.0,5.0)
            
            st.form_submit_button()
    
    st.metric("Num of loads", "2")
    
    with st.expander("View Loads"):
        st.write("view point load loaction and magnitude")

with col_parameter:
    st.header("Parameters of the bar")
    
    Material = st.selectbox("Select the Material:",
        options=["Iron","Steel","Copper"]
        )

    cross_section = st.selectbox(
        "Select the Cross Section Type:",
        options=["Circle","Square","rectangle"]
        )

    Length = st.number_input(
        "the length of the rod in mm:",
        0,10000000,1000
    )

    Detail=st.slider(
        "the number of nodes:",
        0,1000,50,50
        )
    
col1, col2, col3 , col4, col5 = st.columns(5)
col1.metric("Nodes", "100",help="Recommended:100")
col2.metric("Length", "1 m",help="Recommended:1m")
col3.metric("Number of Loads","2",help="Recommended:2")
col4.metric("Modulous of Elasticity","210 Gpa",help="Recommended:210Gpa")
col5.metric("Moment of Inertia","1",help="Recommended:circle")



st.markdown("""---""")
