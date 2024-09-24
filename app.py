import streamlit as st
import json
from model import probe_model_5l_profit  # Import your function from model.py

def main():
    st.title("Financial Analysis Web App")
    
    # Page 1: Upload File
    st.header("Upload your data.json file")
    uploaded_file = st.file_uploader("Choose a data.json file", type="json")
    
    if uploaded_file is not None:
        # Read and process the uploaded JSON data
        data = json.load(uploaded_file)

        # Get results from the model
        results = probe_model_5l_profit(data['data'])
        
        # Page 2: Display Results
        st.header("Results from Financial Analysis")
        st.json(results)  # Display results as formatted JSON

if __name__ == "__main__":
    main()
