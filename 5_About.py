import streamlit as st
from lib.ui import set_app_config, sidebar_user_card
from lib.auth import require_login

set_app_config()
sidebar_user_card()
require_login()

st.title("About — XplainLab")

st.write("""
**XplainLabs** is a mini “virtual ML lab” to help users understand *why* a model approved/rejected:

- Multi‑page flow: Login → Choose Dataset & Algorithm → Submit form → Predict + Explain + Visualize
- Algorithms: Decision Tree, KNN, Logistic Regression
- Explainability:
  - Decision Tree: rule extraction (readable decision logic)
  - Logistic Regression: top feature contributions
  - KNN: nearest-neighbor style explanation (approx)
""")