import streamlit as st
from library import *
import func
import read
import split
import export
import plot

#Webpage Customization
st.set_page_config(layout="wide")

#Path
#source = r"C:\Users\AIRSHOW\Downloads\Raw To Engineering Logs Converter\Engineering Logs\\"
#destination = r"D:\alt\split\\"
uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=["csv"])
#Function to read raw files
#@st.cache_data
def run(source,destination):

    #Run the first filter 
    data_lib = read.run(source,func.filter1)
    
    #Split the telemetry files if there are double sorties in one files.
    parent_path2 = split.run(data_lib,destination)

    #Run the third filter
    data_lib3 = read.run(parent_path2,func.filter2)

    return data_lib3

final_data = run(source,destination)

#Streamlit web section
files = list(final_data.keys())
telemetry_file = st.selectbox("Select files to view", files)

tabs1, tabs2 = st.tabs(['Telemetry', 'Plot'])

with tabs1:
    #Print out the dataframe of the telemetry they want to view
    st.dataframe(final_data[telemetry_file])

with tabs2:
    #User will select the graph they want to plot
    selection = st.selectbox("Select Plot", ['UAV vs Pri Baro', 'UAV vs Sec Baro', 'Pri Baro vs Sec Baro'])

    #After selection (plot the relevant graph selected)
    plot.run(final_data[telemetry_file],selection,toggle=1)

    # Button to generate altitude report
    generate = st.button('Generate Report')

    #Function to generate if the button is pressed
    if generate:
        with st.spinner('Wait for it...'):
            #Generate report
            export.run(final_data)
            st.success("Report Generated")











