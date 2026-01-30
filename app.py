import streamlit as st
from lib.ui import set_app_config, sidebar_user_card
from lib.auth import require_login
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

set_app_config()

st.title("XplainLab")
st.caption("Transparent ML decisions for Loan Eligibility + Student Eligibility (Decision Tree, KNN, Logistic Regression).")

sidebar_user_card()

if not st.session_state.get("logged_in"):
    st.info("Please login first using the **Login** page in the sidebar.")
    st.stop()

st.success("You're logged in. Use the sidebar to continue:")
st.write("- **Choose Dataset & Algorithm**")
st.write("- Fill **Loan Applicant** or **Student Eligibility** form")
st.write("- See **Prediction + Why (Explainability) + Visuals + Rules**")
from lib.auth import go_login

if not st.session_state.get("logged_in"):
    go_login()