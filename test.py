import streamlit as st
import zipfile
import io
import pandas as pd

# Cache the function that reads and processes the ZIP file
@st.cache_data
def process_zip(uploaded_file):
    # Dictionary to store DataFrames with filename as the key
    df_dict = {}
    
    # Use zipfile to open the ZIP archive
    with zipfile.ZipFile(io.BytesIO(uploaded_file.read())) as zf:
        # List the files inside the ZIP archive
        file_names = zf.namelist()
        
        # Loop through the files and read them as CSVs
        for file_name in file_names:
            if file_name.endswith('.txt'):  # Assuming the text files are CSV-formatted
                with zf.open(file_name) as file:
                    try:
                        # Read the content of the text file as a DataFrame
                        df = pd.read_csv(file)
                        
                        # Store the DataFrame in the dictionary with filename as the key
                        df_dict[file_name] = df
                    except Exception as e:
                        st.write(f"Error reading {file_name}: {e}")
    return df_dict

# Upload the ZIP file containing CSV text files
uploaded_file = st.file_uploader("Upload a ZIP file containing text (CSV) files", type="zip")

# If a file is uploaded
if uploaded_file is not None:
    # Process the ZIP file and cache the result
    df_dict = process_zip(uploaded_file)
    
    # Display DataFrames stored in the dictionary
    if df_dict:
        selected_file = st.selectbox("Select a file to view:", list(df_dict.keys()))
        
        # Show the selected DataFrame
        st.write(f"Displaying Data from: {selected_file}")
        st.dataframe(df_dict[selected_file])  # Display the selected DataFrame
