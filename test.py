import streamlit as st
import zipfile
import io
import pandas as pd

# Upload the ZIP file
uploaded_file = st.file_uploader("Upload a ZIP file containing text (CSV) files", type="zip")

# If a file is uploaded
if uploaded_file is not None:
    # Use the zipfile module to extract the contents of the ZIP file
    with zipfile.ZipFile(io.BytesIO(uploaded_file.read())) as zf:
        # List the file names inside the ZIP file
        file_names = zf.namelist()

        # Loop through the files and read their contents as CSV
        for file_name in file_names:
            if file_name.endswith('.txt'):  # Assuming all .txt files are CSV format
                with zf.open(file_name) as file:
                    # Read the content of the text file as CSV
                    try:
                        df = pd.read_csv(file)
                        st.write(f"Data from {file_name}:")
                    except Exception as e:
                        st.write(f"Error reading {file_name}: {e}")
