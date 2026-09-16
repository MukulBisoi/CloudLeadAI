import pandas as pd
import streamlit as st

from utils.prediction import predict_leads, validate_input_features
from utils.scoring import recommended_action, top_driver


def render(model, config):
    st.header("Batch Lead Scoring")
    st.caption("Upload a CSV and score thousands of prospects in seconds.")
    upload = st.file_uploader("Upload lead CSV", type=["csv"])
    if upload is None:
        st.info("Expected columns are the numeric and categorical features listed in the deployment configuration.")
        return
    try:
        df = pd.read_csv(upload)
    except Exception as exc:
        st.error(f"Invalid CSV: {exc}")
        return
    if df.empty:
        st.error("The uploaded CSV is empty.")
        return
    validation = validate_input_features(df, config)
    if validation["missing"]:
        st.error("Missing required columns:")
        st.write(validation["missing"])
        return
    if validation["extra"]:
        st.info(f"Extra columns will be preserved in the output: {', '.join(validation['extra'][:12])}")
    if df.duplicated().any():
        st.warning("Duplicate rows were detected.")
    if df.isna().any().any():
        st.warning("Missing values were detected. The trained preprocessing pipeline will impute supported fields.")
    try:
        scored = predict_leads(df, model, config, st.session_state.hot_lead_threshold)
        scored["Top_Driver"] = scored.apply(top_driver, axis=1)
        scored["Recommended_Action"] = scored.apply(recommended_action, axis=1)
    except Exception as exc:
        st.error("Prediction failed in a controlled way.")
        st.code(str(exc))
        return
    scored = scored.sort_values("Lead_Score", ascending=False)
    st.success(f"Scored {len(scored):,} leads.")
    st.dataframe(scored, use_container_width=True, hide_index=True)
    st.download_button("Download Scored Leads", scored.to_csv(index=False), "cloudlead_scored_leads.csv", "text/csv", type="primary")
