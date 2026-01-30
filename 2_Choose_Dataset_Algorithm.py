import streamlit as st
from lib.ui import set_app_config, sidebar_user_card
from lib.auth import require_login
from lib.models import ALGORITHMS

set_app_config()
sidebar_user_card()
require_login()

st.title("Choose Dataset & Algorithm")

role = st.session_state.get("role", "Student")

default_dataset = "loan" if role == "Loan Applicant" else "student"
dataset = st.radio(
    "Select dataset",
    options=[("loan", "Loan Eligibility"), ("student", "Student Eligibility")],
    format_func=lambda x: x[1],
    index=0 if default_dataset == "loan" else 1,
)

algo = st.selectbox("Select ML algorithm", options=ALGORITHMS, index=0)
mode = st.radio("Explanation mode", options=["Beginner", "Expert"], index=0)

col1, col2 = st.columns(2)
with col1:
    if st.button("Save Selection", type="primary"):
        st.session_state["dataset"] = dataset[0]
        st.session_state["algorithm"] = algo
        st.session_state["mode"] = mode
        st.success("Saved. Now open the relevant form page from the sidebar.")

with col2:
    st.info("Next step: open **Loan Applicant** or **Student Eligibility** page in the sidebar.")

# Redirect to Loan Applicant or Student Eligibility page based on user choice
if st.button("Submit"):
    if st.session_state["dataset"] == "loan":
        st.switch_page("pages/3_Loan_Applicant.py")
    elif st.session_state["dataset"] == "student":
        st.switch_page("pages/4_Student_Eligibility.py")