import plotly.express as px
import streamlit as st

from utils.explanations import feature_importance
from utils.prediction import prediction_health_check


def render(model, config, leads):
    st.header("Model Analytics & Health")
    ok, message = prediction_health_check(model, config)
    st.metric("Active Model", config.get("model_name", "Unknown"))
    st.success("MODEL STATUS - Operational" if ok else "MODEL STATUS - Warning")
    st.caption(message)
    cols = st.columns(5)
    for col, metric in zip(cols, ["validation_roc_auc", "validation_pr_auc", "test_roc_auc", "test_pr_auc", "brier_score"]):
        col.metric(metric.replace("_", " ").title(), config.get(metric, "Not available"))
    st.metric("Hot Lead Threshold", f"{st.session_state.hot_lead_threshold:.2f}")
    importance = feature_importance(model, config, limit=25)
    st.subheader("Feature Importance")
    if importance.empty:
        st.info("Feature importance is not exposed by the active model artifact.")
    else:
        st.plotly_chart(px.bar(importance.sort_values("Importance"), x="Importance", y="Feature", orientation="h"), use_container_width=True)
    st.subheader("Threshold & Portfolio Views")
    if leads.empty:
        st.info("Lead-level analytics require scored lead data.")
        return
    thresholds = []
    for t in [0.5, 0.6, 0.7, st.session_state.hot_lead_threshold, 0.8, 0.9]:
        thresholds.append({"Threshold": round(t, 2), "Hot Leads": int((leads["Conversion_Probability"] >= t).sum())})
    st.plotly_chart(px.line(thresholds, x="Threshold", y="Hot Leads", markers=True), use_container_width=True)
    gains = leads.sort_values("Conversion_Probability", ascending=False).reset_index(drop=True)
    gains["Percent_Leads"] = (gains.index + 1) / len(gains) * 100
    gains["Cumulative_Expected_Conversions"] = gains["Conversion_Probability"].cumsum()
    st.plotly_chart(px.line(gains, x="Percent_Leads", y="Cumulative_Expected_Conversions", title="Cumulative Gains"), use_container_width=True)
    st.caption("ROC, PR, calibration, and validation curves require saved holdout predictions or curve arrays. They were not present in the current config, so fabricated curves are not shown.")
