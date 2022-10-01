from faulthandler import disable
from math import fabs
import pandas as pd
import plotly.express as px
import streamlit as st 
import numpy as np

df = pd.DataFrame(
    np.random.randn(1, 5),
    columns=('col %d' % i for i in range(5)))
#streamlit run webapp.py
st.set_page_config(page_title="Beam Deflection using FDM", page_icon=":bar_chart:", layout="wide")

# ---- Variables ----

if 'count_loads' not in st.session_state:
	st.session_state.count_loads = 0
if 'Moment_of_inertia' not in st.session_state:
	st.session_state.Moment_of_inertia = 0
if 'Loads' not in st.session_state:
	st.session_state.Loads = 0

Materials = {
    "Iron": 201,
    "Steel": 220,
    "Copper": 241
}

# ---- MAINPAGE ----
st.title(":bar_chart: line Deflection using FDM")

col_data_input, col_parameter = st.columns(2)

with col_data_input:
    st.header("Input Loads")
    if st.button('Define Loads') :
        with st.form("take load"):
            st.session_state.count_loads += 1
            length_of_load=st.number_input("Length of load:",0,100,1,5,help="1 if it is a point load")
            
            location_of_load=st.number_input("Location of load:",0,100,50,5)
            
            mag_of_load=st.number_input("Magnitude of load (in N):",0.0,10000.0,10.0,5.0)
            
            st.form_submit_button()
    
    st.metric("Num of loads", st.session_state.count_loads)
    st.write("View Loads")
    chart_data = pd.DataFrame(
    np.random.randn(10, 1),
    columns=['Load'])
    st.line_chart(chart_data)

with col_parameter:
    st.header("Parameters of the bar")
    
    Material = st.selectbox("Select the Material:",
        options=["Iron","Steel","Copper"]
        )

    cross_section = st.selectbox(
        "Select the Cross Section Type:",
        options=["Circle","Square","Rectangle"]
        )
    if cross_section =="Circle":
        radius=st.number_input("Give the radius :")
        st.session_state.Moment_of_inertia=np.pi*radius*radius
    elif cross_section=="Square":
        side_length=st.number_input("Give the length of a side :")
        st.session_state.Moment_of_inertia=side_length*side_length
    elif cross_section=="Rectangle":
        Length=st.number_input("Give the length of the Rectangle :")
        Breath=st.number_input("Give the breath of a Rectangle :")
        st.session_state.Moment_of_inertia=Breath*Length

    Length = st.number_input(
        "the length of the rod in mm:",
        0,10000000,1000
    )

    Detail=st.slider(
        "the number of nodes:",
        0,1000,50,50
        )
    
col1, col2, col3 , col4, col5 = st.columns(5)
col1.metric("Nodes", Detail,help="Recommended:100")
col2.metric("Length", Length,help="Recommended:1m")
col3.metric("Number of Loads",st.session_state.count_loads,help="Recommended:2")
col4.metric("Modulous of Elasticity",Materials[Material],help="Recommended:210Gpa")
col5.metric("Moment of Inertia",float("{:.2f}".format(st.session_state.Moment_of_inertia)),help="Recommended:circle")

st.markdown("""---""")

final_col1,final_col2,final_col3,final_col4,final_col5,final_col6,final_col7 =st.columns(7)
final_col2.button("S O L V E")
final_col4.button("R E R U N")
final_col6.button("D O W N L O A D")

st.markdown("""---""")

chart_data = pd.DataFrame(
np.random.randn(10, 2),
columns=['Deflection','No deviation line'])
st.line_chart(chart_data)