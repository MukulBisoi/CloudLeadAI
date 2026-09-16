from pathlib import Path

import pandas as pd
import streamlit as st

from utils.prediction import predict_leads
from utils.scoring import recommended_action, top_driver


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


def _candidate_data_files():
    return [
        DATA_DIR / "cloudlead_scored_leads.csv",
        ROOT / "cloudlead_scored_leads.csv",
        DATA_DIR / "LeadScoring.csv",
        ROOT / "Lead Scoring.csv",
    ]


@st.cache_data(show_spinner=False)
def _read_csv(path):
    return pd.read_csv(path)


def load_source_leads():
    for path in _candidate_data_files():
        if path.exists():
            return _read_csv(path), path
    return pd.DataFrame(), None


def load_scored_leads(model, config, hot_threshold):
    df, path = load_source_leads()
    if df.empty:
        return df
    if {"Conversion_Probability", "Lead_Score", "Lead_Category"}.issubset(df.columns):
        scored = df.copy()
    else:
        scored = predict_leads(df, model, config, hot_threshold)
    scored["Top_Driver"] = scored.apply(top_driver, axis=1)
    scored["Recommended_Action"] = scored.apply(recommended_action, axis=1)
    scored.attrs["source_path"] = str(path) if path else ""
    return scored


def lead_id_column(df):
    for col in ["Lead Number", "Prospect ID", "Lead ID"]:
        if col in df.columns:
            return col
    return None


def available_options(df, column, limit=100):
    if column not in df.columns:
        return []
    values = df[column].dropna().astype(str)
    values = values[~values.str.lower().isin(["nan", "select"])]
    return sorted(values.unique().tolist())[:limit]
