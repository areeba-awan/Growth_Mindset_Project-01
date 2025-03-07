              
# Importing Streamlit and other libraries for the Growth Mindeset Project # 
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title = "💿 Data Sweeper", layout="wide")

# #custom css for basic styling 

#  st.markdown("""

#  <style>
#     .stApp{
#          background-color: #black;
#        color: white;
#     }
#      </style>
#        """,
#        unsafe_allow_html=True)


# Main Title of the app and a brief description of the app
st.title("💿 Data Sweeper By Areeba Awan 🧕")  
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")
st.write("Creating a data-driven culture in your organization is easier than ever with Data Sweeper.")


# File uploader widget that accepts CSV and Excel files
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue

        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📚 File Size:** {file.size / 1024:.2f} KB")

       # File Details
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())

      # Data Cleaning Options for App

        st.subheader("🧹 Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates Removed Successfully! ✅")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing Values Have Been Filled! ✅")

        # Choose Specific Columns to Keep or Convert
        st.subheader("🎯 Select Columns to Keep or Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

       # Create some Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Convert the File -> CSV to Excel Options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            # Download Button
            st.download_button(
                label=f"📥 Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 Data Cleaning and Conversion Completed Successfully! 🎉")
                            
