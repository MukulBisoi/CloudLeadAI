from pathlib import Path

import joblib
import streamlit as st

try:
    from catboost import CatBoostClassifier
except Exception:  # pragma: no cover
    CatBoostClassifier = None


ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = ROOT / "models"


def _first_existing(*paths):
    for path in paths:
        if path.exists():
            return path
    return paths[0]


def artifact_paths():
    return {
        "config": _first_existing(MODELS_DIR / "cloudlead_config.pkl", ROOT / "cloudlead_config.pkl"),
        "xgboost": _first_existing(MODELS_DIR / "cloudlead_model.pkl", ROOT / "cloudlead_model.pkl"),
        "catboost": _first_existing(MODELS_DIR / "cloudlead_catboost_model.cbm", ROOT / "cloudlead_catboost_model.cbm"),
    }


def artifact_status():
    paths = artifact_paths()
    config_exists = paths["config"].exists()
    model_name = "XGBoost"
    if config_exists:
        try:
            model_name = joblib.load(paths["config"]).get("model_name", "XGBoost")
        except Exception:
            model_name = "Unknown"
    selected = paths["catboost"] if model_name == "CatBoost" else paths["xgboost"]
    return {
        "config_exists": config_exists,
        "model_exists": selected.exists(),
        "model_path": selected,
        "config_path": paths["config"],
        "model_name": model_name,
    }


@st.cache_resource(show_spinner="Loading CloudLead AI model...")
def load_artifacts():
    paths = artifact_paths()
    config = joblib.load(paths["config"])
    model_name = config.get("model_name", "XGBoost")
    if model_name == "CatBoost":
        if CatBoostClassifier is None:
            raise RuntimeError("CatBoost is required to load the selected model.")
        model = CatBoostClassifier()
        model.load_model(str(paths["catboost"]))
    else:
        model = joblib.load(paths["xgboost"])
    return model, config


def required_features(config):
    return list(config.get("numeric_features", [])) + list(config.get("categorical_features", []))
