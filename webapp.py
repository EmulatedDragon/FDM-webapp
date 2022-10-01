from faulthandler import disable
import pandas as pd
import plotly.express as px
import streamlit as st 
import numpy as np
import deflection_calculation as df

#streamlit run webapp.py
st.set_page_config(page_title="Beam Deflection using FDM", page_icon=":bar_chart:", layout="wide")

# ---- Variables ----

if 'nodes' not in st.session_state:
	st.session_state.nodes = 100
if 'count_loads' not in st.session_state:
	st.session_state.count_loads = 0
if 'Moment_of_inertia' not in st.session_state:
	st.session_state.Moment_of_inertia = 0
if 'Loads' not in st.session_state:
	st.session_state.Loads = np.zeros(1000)
if 'Deflection' not in st.session_state:
	st.session_state.Deflection = np.zeros(1000)

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
    #if st.button('Define Loads'):
    take_load = st.form(key="take_load")
    length_of_load = take_load.number_input("Length of load:",0,100,1,5,help="1 if it is a point load")    
    location_of_load = take_load.number_input("Location of load:",0,100,50,5)    
    mag_of_load = take_load.number_input("Magnitude of load (in N):",-10000,10000,10,5)
    #submitted = take_load.form_submit_button("Submit")
    if take_load.form_submit_button("Submit"):
        st.session_state.count_loads += 1
        for i in range(location_of_load,location_of_load+length_of_load+1):
            st.session_state.Loads[i]+=mag_of_load
    st.metric("Num of loads", st.session_state.count_loads)
    st.write("View Loads")
    chart_data = pd.DataFrame(
    st.session_state.Loads[0:st.session_state.nodes],
    columns=['Load'])
    st.line_chart(chart_data)

with col_parameter:
    st.header("Parameters of the bar")
    
    Material = st.radio("Select the Material:",
        options=["Iron","Steel","Copper"]
        )

    Length = st.number_input(
        "the length of the rod in mm:",
        0,10000000,1000
    )

    st.session_state.nodes=st.slider(
        "the number of nodes:",
        0,1000,100,50
        )
    
    cross_section = st.radio(
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
    
col1, col2, col3 , col4, col5 = st.columns(5)
col1.metric("Nodes", st.session_state.nodes,help="Recommended:100")
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

deflection=np.array(df.deflection_calculate(
    st.session_state.Loads[0:st.session_state.nodes],
    st.session_state.nodes,
    Materials[Material],
    st.session_state.Moment_of_inertia,
    Length
))

chart_data = pd.DataFrame(
deflection,
columns=['Deflection'])
st.line_chart(chart_data)

