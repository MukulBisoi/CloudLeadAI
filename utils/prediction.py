import numpy as np
import pandas as pd

from utils.model_loader import required_features


def assign_lead_category(probability, hot_threshold):
    if probability >= hot_threshold:
        return "Hot"
    if probability >= 0.50:
        return "Warm"
    return "Cold"


def validate_input_features(df, config):
    required = required_features(config)
    missing = [col for col in required if col not in df.columns]
    extra = [col for col in df.columns if col not in required and col not in config.get("excluded_columns", [])]
    return {"valid": not missing, "missing": missing, "extra": extra}


def prepare_features(df, config):
    required = required_features(config)
    result = df.copy()
    for col in required:
        if col not in result.columns:
            result[col] = np.nan
    return result.reindex(columns=required)


def predict_leads(df, model, config, hot_threshold=None):
    threshold = float(hot_threshold if hot_threshold is not None else config.get("hot_lead_threshold", 0.72))
    features = prepare_features(df, config)
    probabilities = model.predict_proba(features)[:, 1].astype(float)
    scored = df.copy()
    scored["Conversion_Probability"] = probabilities
    scored["Lead_Score"] = np.round(probabilities * 100, 2)
    scored["Lead_Category"] = [assign_lead_category(p, threshold) for p in probabilities]
    return scored


def prediction_health_check(model, config):
    sample = {}
    for col in config.get("numeric_features", []):
        sample[col] = 0.0
    for col in config.get("categorical_features", []):
        sample[col] = "Unknown"
    try:
        predict_leads(pd.DataFrame([sample]), model, config)
        return True, "Prediction check passed."
    except Exception as exc:
        return False, str(exc)
