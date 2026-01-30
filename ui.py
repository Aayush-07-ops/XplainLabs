import streamlit as st

APP_NAME = "XplainLab"

def set_app_config():
    st.set_page_config(
        page_title=APP_NAME,
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def sidebar_user_card():
    with st.sidebar:
        st.markdown(f"## {APP_NAME}")
        if st.session_state.get("logged_in"):
            st.success("Logged in")
            st.write(f"**Name:** {st.session_state.get('name','-')}")
            st.write(f"**Email:** {st.session_state.get('email','-')}")
            st.write(f"**Phone:** {st.session_state.get('phone','-')}")
            role = st.session_state.get("role", "-")
            st.write(f"**Role:** {role}")
            st.divider()
            if st.button("Log out", type="secondary"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()
        else:
            st.warning("Not logged in")
            st.caption("Go to **Login** page.")