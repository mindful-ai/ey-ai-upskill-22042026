"""
Streamlit UI for ABOC system
"""

import streamlit as st
import requests

API_URL = "http://localhost:8000/run"

st.set_page_config(page_title="ABOC AI System", layout="wide")

st.title("🚀 Autonomous Business Operations Co-Pilot")

st.markdown("### Enter a business request:")

user_input = st.text_input(
    "Example: Create a PO for 50 sensors from VendorA under 400000 INR"
)

if st.button("Run Workflow"):

    if user_input:
        with st.spinner("Processing..."):

            response = requests.post(API_URL, json={"query": user_input})

            if response.status_code == 200:
                data = response.json()["result"]

                st.success("Workflow Completed!")

                st.subheader("📊 Output")

                for key, value in data.items():
                    st.write(f"**{key}**: {value}")

            else:
                st.error("API Error")