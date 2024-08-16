import streamlit as st
import docker_management
import database_view

st.set_page_config(page_title="R-Scrape Admin Panel", layout="wide")

def main():
    st.title("R-Scrape Admin Panel")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Docker Management", "Database View"])
    
    if page == "Docker Management":
        docker_management.show()
    elif page == "Database View":
        database_view.show()

if __name__ == "__main__":
    main()