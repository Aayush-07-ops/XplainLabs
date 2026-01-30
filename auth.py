import streamlit as st

LOGIN_PAGE = "pages/1_Login.py"
CHOOSE_PAGE = "pages/2_Choose_Dataset_Algorithm.py"

def init_auth_state():
    st.session_state.setdefault("logged_in", False)
    st.session_state.setdefault("name", "")
    st.session_state.setdefault("email", "")
    st.session_state.setdefault("phone", "")
    st.session_state.setdefault("role", "")  # "Loan Applicant" or "Student"
    st.session_state.setdefault("dataset", None)  # "loan" or "student"
    st.session_state.setdefault("algorithm", None)  # "Decision Tree" | "KNN" | "Logistic Regression"
    st.session_state.setdefault("mode", "Beginner")  # Beginner | Expert

def _switch_page(path: str):
    """
    Safe wrapper so the app doesn't crash if Streamlit version doesn't support switch_page.
    """
    try:
        st.switch_page(path)
    except Exception:
        # fallback: show a link + stop
        st.warning("Auto-navigation is not available in your Streamlit version. Please use the sidebar.")
        st.page_link(path, label="Go now", icon="➡️")
        st.stop()

def go_login():
    _switch_page(LOGIN_PAGE)

def go_choose():
    _switch_page(CHOOSE_PAGE)

def require_login():
    init_auth_state()
    if not st.session_state.get("logged_in"):
        go_login()

def require_dataset_and_algo():
    require_login()
    if not st.session_state.get("dataset") or not st.session_state.get("algorithm"):
        go_choose()