import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lib.ui import set_app_config, sidebar_user_card
from lib.auth import require_dataset_and_algo
from lib.data import load_student_df
from lib.models import train_model, predict_with_explanations

set_app_config()
sidebar_user_card()
require_dataset_and_algo()

if st.session_state["dataset"] != "student":
    st.warning("You selected Loan dataset. Please switch dataset on **Choose Dataset & Algorithm**.")
    st.stop()

st.title("Student Eligibility — XplainLab")

df = load_student_df()

with st.expander("Preview sample student dataset"):
    st.dataframe(df, use_container_width=True)

algo = st.session_state["algorithm"]
mode = st.session_state["mode"]

train_df = df.drop(columns=["Student_ID"])
target = "Eligible"
model_bundle = train_model(train_df, target_col=target, algo=algo)

st.caption(f"Model: **{algo}** | Mode: **{mode}** | Rows used: {model_bundle['metrics']['n_rows']} | Holdout Accuracy: {model_bundle['metrics']['accuracy_holdout']}")

st.subheader("1) Enter Student Details")

with st.form("student_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        name = st.text_input("Name")
        roll = st.text_input("Roll No.")
        gender = st.selectbox("Gender", ["Male", "Female"])
        department = st.selectbox("Department", ["CSE", "IT", "EEE", "ECE", "CE", "ME"])

    with c2:
        course = st.text_input("Course")
        section = st.text_input("Section")
        attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=75.0, step=1.0)
        cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, value=7.5, step=0.1)

    with c3:
        backlogs = st.number_input("Backlogs", min_value=0.0, value=1.0, step=1.0)
        credits = st.number_input("Credits Completed", min_value=0.0, value=22.0, step=1.0)
        hosteller = st.selectbox("Hosteller", ["Yes", "No"])

    submitted = st.form_submit_button("Get Prediction", type="primary")

if not submitted:
    st.stop()

input_row = pd.DataFrame(
    [{
        "Gender": gender,
        "Attendance": attendance,
        "CGPA": cgpa,
        "Backlogs": backlogs,
        "Credits_Completed": credits,
        "Department": department,
        "Hosteller": hosteller,
    }]
)

result = predict_with_explanations(model_bundle, input_row=input_row, algo=algo)

pred = str(result["prediction"])
eligible = pred.lower() == "yes"
status_text = "ELIGIBLE ✅" if eligible else "NOT ELIGIBLE ❌"

tabs = st.tabs(["2) Prediction Result", "3) Why? (Explanation)", "4) Visuals", "5) Explore Rules"])

with tabs[0]:
    st.subheader(status_text)
    st.write("**Model output:**", pred)

    if mode == "Beginner":
        st.info("Try adjusting Attendance / CGPA / Backlogs and compare algorithms to see how decisions change.")

with tabs[1]:
    st.subheader("Explanation")

    reasons = []
    if cgpa >= 7.0:
        reasons.append("CGPA is good → increases eligibility chance.")
    else:
        reasons.append("CGPA is low → decreases eligibility chance.")

    if attendance >= 75:
        reasons.append("Attendance is strong → increases eligibility chance.")
    else:
        reasons.append("Attendance is low → decreases eligibility chance.")

    if backlogs >= 2:
        reasons.append("Backlogs are high → decreases eligibility chance.")
    else:
        reasons.append("Backlogs are low → increases eligibility chance.")

    st.write("**Quick reasons (rule-of-thumb):**")
    for r in reasons[:6]:
        st.write("- ", r)

    st.divider()
    st.write(f"**Model-specific explainability ({algo}):**")

    if algo == "Decision Tree":
        st.code(result["explanations"].get("tree_rules", "No rules."), language="text")
    elif algo == "Logistic Regression":
        top = result["explanations"].get("top_contributions", [])
        st.dataframe(pd.DataFrame(top), use_container_width=True) if top else st.write("No contribution data available.")
    elif algo == "KNN":
        st.write(result["explanations"].get("knn_neighbors", {}))

with tabs[2]:
    st.subheader("Visuals")

    c1, c2 = st.columns(2)
    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x="Eligible", ax=ax)
        ax.set_title("Eligibility Distribution (sample)")
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.scatterplot(data=df, x="Attendance", y="CGPA", hue="Eligible", ax=ax)
        ax.set_title("Attendance vs CGPA (sample)")
        st.pyplot(fig)

with tabs[3]:
    st.subheader("Explore Rules & Suggestions")
    if eligible:
        st.success("You appear eligible under current model settings.")
        st.write("- Keep attendance and CGPA stable.")
        st.write("- Maintain low backlogs.")
    else:
        st.error("You appear not eligible under current model settings.")
        st.write("- Improve CGPA and attendance.")
        st.write("- Reduce backlogs.")
        st.write("- Compare results across algorithms.")
        from lib.auth import go_choose

if st.session_state["dataset"] != "student":
    go_choose()