import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from lib.ui import set_app_config, sidebar_user_card
from lib.auth import require_dataset_and_algo
from lib.data import load_loan_df
from lib.models import train_model, predict_with_explanations

set_app_config()
sidebar_user_card()
require_dataset_and_algo()

if st.session_state["dataset"] != "loan":
    st.warning("You selected Student dataset. Please switch dataset on **Choose Dataset & Algorithm**.")
    st.stop()

st.title("Loan Applicant — XplainLab")

df = load_loan_df()

with st.expander("Preview sample loan dataset"):
    st.dataframe(df.head(20), use_container_width=True)

algo = st.session_state["algorithm"]
mode = st.session_state["mode"]

# Training data
train_df = df.drop(columns=["Loan_ID"])
target = "Loan_Status"

model_bundle = train_model(train_df, target_col=target, algo=algo)

st.caption(f"Model: **{algo}** | Mode: **{mode}** | Rows used: {model_bundle['metrics']['n_rows']} | Holdout Accuracy: {model_bundle['metrics']['accuracy_holdout']}")

st.subheader("1) Enter Loan Applicant Details")

with st.form("loan_form"):
    c1, c2, c3 = st.columns(3)

    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Married", ["Yes", "No"])
        dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
        education = st.selectbox("Education", ["Graduate", "Not Graduate"])

    with c2:
        self_employed = st.selectbox("Self Employed", ["No", "Yes"])
        applicant_income = st.number_input("Applicant Income", min_value=0.0, value=5000.0, step=100.0)
        coapp_income = st.number_input("Coapplicant Income", min_value=0.0, value=0.0, step=100.0)
        loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0.0, value=120.0, step=1.0)

    with c3:
        term = st.number_input("Loan Amount Term (months)", min_value=12.0, value=360.0, step=12.0)
        credit_history = st.selectbox("Credit History", ["1", "0"])
        property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

    submitted = st.form_submit_button("Get Prediction", type="primary")

if not submitted:
    st.stop()

input_row = pd.DataFrame(
    [{
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapp_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": term,
        "Credit_History": float(credit_history),
        "Property_Area": property_area,
    }]
)

result = predict_with_explanations(model_bundle, input_row=input_row, algo=algo)

# Output mapping
pred = str(result["prediction"])
approved = (pred.upper() == "Y")
status_text = "APPROVED ✅" if approved else "REJECTED ❌"

tabs = st.tabs(["2) Prediction Result", "3) Why? (Explanation)", "4) Visuals", "5) Explore Rules"])

with tabs[0]:
    st.subheader(status_text)
    st.write("**Model output:**", pred)

    if result["proba"] is not None:
        # Assume binary classes, find probability of "Y" if present
        pipe = model_bundle["pipeline"]
        classes = list(pipe.named_steps["model"].classes_)
        if "Y" in classes:
            pY = float(result["proba"][classes.index("Y")])
            st.metric("Probability of Approval (Y)", f"{pY:.3f}")
        else:
            st.write("Class probabilities:", result["proba"])

    if mode == "Beginner":
        st.info(
            "This result is based on patterns learned from sample data. "
            "You can change inputs (income, credit history, etc.) and observe how decisions change."
        )

with tabs[1]:
    st.subheader("Explanation (human-friendly)")

    # Simple human-style reasoning (beginner) + model-specific details (expert)
    reasons = []
    if float(credit_history) < 0.5:
        reasons.append("Credit history is 0 → historically decreases approval chance.")
    else:
        reasons.append("Credit history is 1 → historically increases approval chance.")
    if applicant_income + coapp_income < 4000:
        reasons.append("Total income is relatively low → may reduce approval chance.")
    if loan_amount > 200:
        reasons.append("Loan amount is high → may reduce approval chance.")

    st.write("**Quick reasons (rule-of-thumb):**")
    for r in reasons[:6]:
        st.write("- ", r)

    st.divider()
    st.write(f"**Model-specific explainability ({algo}):**")

    if algo == "Decision Tree":
        st.code(result["explanations"].get("tree_rules", "No rules."), language="text")

    elif algo == "Logistic Regression":
        top = result["explanations"].get("top_contributions", [])
        if not top:
            st.write("No contribution data available.")
        else:
            st.write("Top feature contributions (bigger magnitude = more influence):")
            st.dataframe(pd.DataFrame(top), use_container_width=True)

    elif algo == "KNN":
        st.write(result["explanations"].get("knn_neighbors", {}))

with tabs[2]:
    st.subheader("Visuals")

    # Distribution plots using dataset
    df_plot = df.copy()
    df_plot["Credit_History"] = pd.to_numeric(df_plot["Credit_History"], errors="coerce")

    c1, c2 = st.columns(2)

    with c1:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df_plot, x="Loan_Status", ax=ax)
        ax.set_title("Loan Status Distribution (sample)")
        st.pyplot(fig)

    with c2:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.boxplot(data=df_plot, x="Loan_Status", y="ApplicantIncome", ax=ax)
        ax.set_title("Applicant Income vs Loan Status (sample)")
        st.pyplot(fig)

with tabs[3]:
    st.subheader("Explore Rules & Tips")
    if approved:
        st.success("You appear eligible under the current model settings.")
        st.write("- Keep credit history strong.")
        st.write("- Keep loan amount proportional to income.")
    else:
        st.error("You appear not eligible under the current model settings.")
        st.write("- Improve credit history (if possible).")
        st.write("- Increase verified income or reduce requested loan amount.")
        st.write("- Try different algorithms to compare outcomes.")
        from lib.auth import go_choose

if st.session_state["dataset"] != "loan":
    go_choose()