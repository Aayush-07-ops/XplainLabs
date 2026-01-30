import streamlit as st
from lib.ui import set_app_config, sidebar_user_card
from lib.auth import init_auth_state

set_app_config()
init_auth_state()
sidebar_user_card()

st.title("Login — XplainLab")

with st.form("login_form", clear_on_submit=False):
    name = st.text_input("Full Name *", value=st.session_state.get("name", ""))
    email = st.text_input("Email *", value=st.session_state.get("email", ""))
    phone = st.text_input("Contact Number *", value=st.session_state.get("phone", ""))
    role = st.selectbox("I am a *", ["Loan Applicant", "Student"], index=0 if st.session_state.get("role","Loan Applicant")=="Loan Applicant" else 1)

    st.markdown("### Terms & Conditions (Required)")
    st.caption("This is a demo educational system. Do not enter real sensitive financial data.")
    accept = st.checkbox("I agree to the Terms & Conditions *")

    submitted = st.form_submit_button("Login", type="primary")

if submitted:
    if not name.strip() or not email.strip() or not phone.strip():
        st.error("Please fill Name, Email, and Contact Number.")
    elif not accept:
        st.error("You must accept the Terms & Conditions to continue.")
    else:
        st.session_state["logged_in"] = True
        st.session_state["name"] = name.strip()
        st.session_state["email"] = email.strip()
        st.session_state["phone"] = phone.strip()
        st.session_state["role"] = role
        st.success("Login successful. Now open **Choose Dataset & Algorithm** page from the sidebar.")
        st.session_state["logged_in"] = True
        st.session_state["name"] = name.strip()
        st.session_state["email"] = email.strip()
        st.session_state["phone"] = phone.strip()
        st.session_state["role"] = role

        st.success("Login successful. Redirecting...")
        from lib.auth import go_choose
        go_choose()

# Redirect to Choose Dataset & Algorithm page after login
if st.session_state.get("logged_in"):
    st.switch_page("pages/2_Choose_Dataset_Algorithm.py")