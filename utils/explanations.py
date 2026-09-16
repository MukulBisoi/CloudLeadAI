import pandas as pd

from utils.model_loader import required_features


def feature_importance(model, config, limit=20):
    names = required_features(config)
    importances = None
    try:
        clf = model.named_steps.get("classifier") or model.named_steps.get("model")
        pre = model.named_steps.get("preprocessor")
        if pre is not None and hasattr(pre, "get_feature_names_out"):
            names = [n.split("__", 1)[-1].replace("_", " ") for n in pre.get_feature_names_out()]
        importances = getattr(clf, "feature_importances_", None)
    except Exception:
        importances = getattr(model, "feature_importances_", None)
    if importances is None:
        return pd.DataFrame(columns=["Feature", "Importance"])
    df = pd.DataFrame({"Feature": names[: len(importances)], "Importance": importances})
    df["Feature"] = df["Feature"].str.replace("cat__", "", regex=False).str.replace("num__", "", regex=False)
    return df.groupby("Feature", as_index=False)["Importance"].sum().sort_values("Importance", ascending=False).head(limit)


def explain_lead(row, model, config, limit=5):
    base = feature_importance(model, config, limit=50)
    if base.empty:
        return pd.DataFrame(), pd.DataFrame(), "Exact SHAP values are unavailable for this deployed pipeline, so model feature importance is shown instead."
    features = []
    for _, item in base.iterrows():
        label = item["Feature"]
        root = label.split("_", 1)[0]
        value = None
        for col in required_features(config):
            if col in label or col == root or label.startswith(col):
                value = row.get(col)
                break
        direction = 1
        if value in [0, "No", "Unknown", "Select", None]:
            direction = -1
        features.append({"Feature": label, "Contribution": float(item["Importance"]) * direction, "Value": value})
    df = pd.DataFrame(features)
    positives = df[df["Contribution"] >= 0].head(limit)
    negatives = df[df["Contribution"] < 0].head(limit)
    note = "Model-specific feature importance is used because exact SHAP contributions were not exported with the deployment artifacts."
    return positives, negatives, note
