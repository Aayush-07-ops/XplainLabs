from __future__ import annotations

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, export_text

from sklearn.linear_model import LogisticRegression


ALGORITHMS = ["Decision Tree", "KNN", "Logistic Regression"]


def _build_preprocessor(X: pd.DataFrame) -> ColumnTransformer:
    cat_cols = [c for c in X.columns if X[c].dtype == "object"]
    num_cols = [c for c in X.columns if c not in cat_cols]

    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    return ColumnTransformer(
        transformers=[
            ("num", numeric, num_cols),
            ("cat", categorical, cat_cols),
        ],
        remainder="drop",
    )


def _build_model(algo: str):
    if algo == "Decision Tree":
        return DecisionTreeClassifier(max_depth=4, random_state=42)
    if algo == "KNN":
        return KNeighborsClassifier(n_neighbors=5)
    if algo == "Logistic Regression":
        return LogisticRegression(max_iter=2000)
    raise ValueError(f"Unknown algorithm: {algo}")


def train_model(df: pd.DataFrame, target_col: str, algo: str) -> dict:
    """
    Returns dict with:
      - pipeline
      - feature_names (after preprocessing)
      - X_cols (original)
      - metrics
    """
    df = df.copy()
    df = df.dropna(subset=[target_col])

    X = df.drop(columns=[target_col])
    y = df[target_col].astype(str)

    pre = _build_preprocessor(X)
    model = _build_model(algo)

    pipe = Pipeline(steps=[("pre", pre), ("model", model)])

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y if y.nunique() > 1 else None
    )
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred)) if len(y_test) else None

    # feature names after preprocessing (for explanations)
    feature_names = None
    try:
        pre_fitted = pipe.named_steps["pre"]
        feature_names = list(pre_fitted.get_feature_names_out())
    except Exception:
        feature_names = None

    return {
        "pipeline": pipe,
        "feature_names": feature_names,
        "X_cols": list(X.columns),
        "metrics": {"accuracy_holdout": acc, "n_rows": int(len(df))},
    }


def predict_with_explanations(model_bundle: dict, input_row: pd.DataFrame, algo: str) -> dict:
    """
    input_row must be a 1-row DataFrame with the same columns as training X.
    """
    pipe: Pipeline = model_bundle["pipeline"]
    feature_names = model_bundle["feature_names"]

    pred = pipe.predict(input_row)[0]
    proba = None
    if hasattr(pipe, "predict_proba"):
        try:
            proba = pipe.predict_proba(input_row)[0]
        except Exception:
            proba = None

    out = {
        "prediction": pred,
        "proba": proba,
        "explanations": {},
    }

    # transformed vector
    Xt = pipe.named_steps["pre"].transform(input_row)
    if hasattr(Xt, "toarray"):
        Xt_dense = Xt.toarray()
    else:
        Xt_dense = np.asarray(Xt)
    x_vec = Xt_dense[0]

    # Decision Tree explanation: text rules + path-ish simplification
    if algo == "Decision Tree":
        tree = pipe.named_steps["model"]
        try:
            rule_text = export_text(tree, feature_names=feature_names, decimals=2)
        except Exception:
            rule_text = "Rule extraction unavailable."
        out["explanations"]["tree_rules"] = rule_text

    # Logistic regression explanation: top contributions
    if algo == "Logistic Regression":
        lr = pipe.named_steps["model"]
        if hasattr(lr, "coef_") and feature_names is not None:
            coef = lr.coef_[0]
            contrib = coef * x_vec
            top_idx = np.argsort(np.abs(contrib))[::-1][:10]
            top = []
            for i in top_idx:
                top.append(
                    {
                        "feature": feature_names[i],
                        "contribution": float(contrib[i]),
                        "coef": float(coef[i]),
                        "value": float(x_vec[i]),
                    }
                )
            out["explanations"]["top_contributions"] = top

    # KNN explanation: nearest neighbors (approx)
    if algo == "KNN":
        knn = pipe.named_steps["model"]
        try:
            distances, indices = knn.kneighbors(Xt_dense, n_neighbors=min(5, knn.n_neighbors), return_distance=True)
            out["explanations"]["knn_neighbors"] = {
                "distances": [float(d) for d in distances[0]],
                "indices_in_train_space": [int(i) for i in indices[0]],
                "note": "Indices are in the KNN internal training matrix order (not original Loan_ID/Student_ID).",
            }
        except Exception:
            out["explanations"]["knn_neighbors"] = {"note": "Neighbor explanation unavailable."}

    return out