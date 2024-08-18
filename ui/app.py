import streamlit as st
import docker_management
import database_view
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation_pipeline.main import evaluate_all_unrated_posts

st.set_page_config(page_title="R-Scrape Admin Panel", layout="wide")

def evaluation_page():
    st.header("Evaluate Unrated Posts")
    
    provider = st.selectbox("Choose AI Provider", ["llama", "ollama", "groq"])
    
    if st.button("Start Evaluation"):
        with st.spinner("Evaluating unrated posts..."):
            num_evaluated = evaluate_all_unrated_posts(provider)
        st.success(f"Evaluated {num_evaluated} posts using {provider} provider.")

def main():
    st.title("R-Scrape Admin Panel")
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Docker Management", "Database View", "Evaluation"])
    
    if page == "Docker Management":
        docker_management.show()
    elif page == "Database View":
        database_view.show()
    elif page == "Evaluation":
        evaluation_page()

if __name__ == "__main__":
    main()