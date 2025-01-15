# Core Pkgs
import streamlit as st 

# EDA Pkgs
import pandas as pd 
from ydata_profiling import ProfileReport 

# Components Pkgs
from streamlit_pandas_profiling import st_profile_report

def main():
    """A Simple EDA App with Streamlit Components"""

    # Sidebar Menu
    menu = ["Home", "YData Profiling", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.subheader("Home")
        st.markdown("""
        <div style="background-color:royalblue;padding:10px;border-radius:10px">
        <h1 style="color:white;text-align:center;">Simple EDA App with YData Profiling</h1>
        </div>
        """, unsafe_allow_html=True)
        st.write("Upload your dataset and start exploring!")

    elif choice == "YData Profiling":
        st.subheader("Automated EDA with YData Profiling")
        
        # File uploader
        data_file = st.file_uploader("Upload CSV", type=['csv'])
        
        if data_file is not None:
            # Read the uploaded CSV file
            df = pd.read_csv(data_file)
            st.dataframe(df.head())  # Show the first rows of the dataset
            
            # Generate YData Profiling Report
            st.subheader("Profile Report")
            profile = ProfileReport(df, explorative=True)
            st_profile_report(profile)

    elif choice == "About":
        st.subheader("About App")
        st.write("This app uses Streamlit and YData Profiling to create automated EDA reports.")

if __name__ == '__main__':
    main()

