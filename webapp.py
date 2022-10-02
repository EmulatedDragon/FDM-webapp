import pandas as pd
import streamlit as st 
import numpy as np
import deflection_calculation as df

#streamlit run webapp.py
st.set_page_config(page_title="Beam Deflection using FDM", page_icon=":chart_with_upwards_trend:", layout="wide")

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
    "Iron": 200,
    "Steel": 215,
    "Aluminium": 70,
    "Zinc": 96.5
}
# ---- SIDEBAR ----
st.sidebar.title(':closed_book:ABOUT FDM :')
st.sidebar.write("""
This was calculated using the method of Finite Difference Method.
The finite difference method (FDM) is an approximate method for solving partial differential equations.
It has been used to solve a wide range of problems.
""")
st.sidebar.write("The following Differential Equation is used to calculate deflection in a Beam:")
st.sidebar.image('.\src/Equation.jpg',"",200)
st.sidebar.title(":star:CREDITS :")
st.sidebar.subheader("PREETHAM A :v:")
st.sidebar.write("check out my :link:[linkedIn](https://www.linkedin.com/in/preetham-a-289628225/)")
st.sidebar.write("check out my :link:[Github](https://github.com/EmulatedDragon)")



# ---- MAINPAGE ----
st.title(":chart_with_upwards_trend: Line Deflection using FDM")

col_data_input, col_parameter = st.columns(2)

with col_data_input:
    st.header("Input Loads")
    #if st.button('Define Loads'):
    take_load = st.form(key="take_load")
    length_of_load = take_load.number_input("Length of load:",0,100,1,5,help="1 if it is a point load")    
    location_of_load = take_load.number_input("Location of load:",0,100,50,5)    
    mag_of_load = take_load.number_input("Magnitude of load (in N):",-10000,10000,10,5,help="+ve -upward and _ve - Downward")
    #submitted = take_load.form_submit_button("Submit")
    if take_load.form_submit_button("Submit"):
        st.session_state.count_loads += 1
        for i in range(location_of_load,location_of_load+length_of_load+1):
            st.session_state.Loads[i]+=mag_of_load
    st.metric("Num of loads", st.session_state.count_loads)
    st.write("View Loads")
    chart_data_load = pd.DataFrame(
    st.session_state.Loads[0:st.session_state.nodes],
    columns=['Load'])
    st.line_chart(chart_data_load)

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
        options=["Circle","Pipe","Rectangle","I Beam"]
        )
    if cross_section =="Circle":
        st.image('.\src\Circle_crossection.jpg',"",250)
        d=st.number_input("Give d:",10)
        st.session_state.Moment_of_inertia=np.pi*d*d*d*d/32
    elif cross_section=="Pipe":
        st.image('.\src\Pipe_crossection.jpg',"",250)
        d=st.number_input("Give d :")
        t=st.number_input("Give t :")
        st.session_state.Moment_of_inertia=np.pi*d*d*d*t/4
    elif cross_section=="Rectangle":
        st.image('.\src\Rectangle_crossection.jpg',"",250)
        b=st.number_input("Give b :")
        h=st.number_input("Give h :")
        st.session_state.Moment_of_inertia=b*h*(b*b+h*h)/12
    elif cross_section=="I Beam":
        st.image('.\src\I_beam_crossection.jpg',"",250)
        b=st.number_input("Give b (b1=b2=b) :")
        t=st.number_input("Give t (t1=t2=t3=t) :")
        st.session_state.Moment_of_inertia=b*b*t*t

    
col1, col2, col3 , col4, col5 = st.columns(5)
col1.metric("Nodes", st.session_state.nodes,help="Recommended:100")
col2.metric("Length", Length,help="Recommended:1m")
col3.metric("Number of Loads",st.session_state.count_loads,help="Recommended:2")
col4.metric("Modulous of Elasticity",Materials[Material],help="Recommended:210Gpa")
col5.metric("Moment of Inertia(mm^4)",float("{:.2f}".format(st.session_state.Moment_of_inertia)),help="Recommended:circle")

st.markdown("""---""")

final_col1,final_col2,final_col3,final_col4,final_col5,final_col6,final_col7 =st.columns(7)
to_solve=final_col2.checkbox("S O L V E")
if final_col4.button("R E R U N"):
    st.warning("RELOAD")
if final_col6.button("C R E D I T S"):
    st.success("OPEN SIDEBAR")
st.markdown("""---""")
if  to_solve:
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
    chart_data.to_csv(".\src\deflection.csv")
    endc1,endc2,endc3=st.columns(3)
    endc2.download_button("D O W N L O A D (values of deflection at all nodes)",'.\src\deflection.csv')