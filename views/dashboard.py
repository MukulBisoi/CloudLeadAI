import plotly.express as px
import streamlit as st

from utils.data_processing import available_options
from utils.prediction import predict_leads
from utils.ui import PALETTE, category_badge, metric_row


def _quick_predictor(model, config):
    st.subheader("Quick Lead Predictor")
    st.markdown(
        "<div style='color:#0F172A;font-weight:700;margin-bottom:.5rem;'>"
        "Enter a lead's attributes to generate a real model-based score."
        "</div>",
        unsafe_allow_html=True,
    )
    values = {}
    for col in config.get("numeric_features", []):
        default = 500.0 if "Time" in col else 3.0
        values[col] = st.number_input(col, value=default, min_value=0.0, key=f"quick_{col}")
    for col in config.get("categorical_features", []):
        if col in ["Lead Origin", "What is your current occupation", "City"]:
            values[col] = st.text_input(col, value="Unknown", key=f"quick_{col}")
        else:
            values[col] = "Unknown"
    if st.button("Generate Lead Score", type="primary", use_container_width=True):
        result = predict_leads(__import__("pandas").DataFrame([values]), model, config, st.session_state.hot_lead_threshold).iloc[0]
        st.metric("Lead Score", f"{result['Lead_Score']:.1f}")
        st.metric("Conversion Probability", f"{result['Conversion_Probability']:.1%}")
        st.markdown(category_badge(result["Lead_Category"]), unsafe_allow_html=True)


def render(model, config, leads):
    st.header("Sales Intelligence Dashboard")
    st.caption("Prioritize the prospects most likely to convert.")
    st.info(f"Active model: {config.get('model_name', 'Unknown')} | Hot Lead threshold: {st.session_state.hot_lead_threshold:.2f}")
    if leads.empty:
        st.warning("Scored data is unavailable until a CSV is uploaded or data/cloudlead_scored_leads.csv is provided.")
        _quick_predictor(model, config)
        return

    total = len(leads)
    avg = leads["Conversion_Probability"].mean()
    hot = int((leads["Lead_Category"] == "Hot").sum())
    velocity = "Not available"
    metric_row([
        ("Total Scored Leads", f"{total:,}", "All available scored leads."),
        ("Average Conversion Rate", f"{avg:.1%}", "Mean predicted conversion probability."),
        ("Active Hot Leads", f"{hot:,}", "Leads at or above the current Hot threshold."),
        ("Sales Response Velocity", velocity, "CRM activity data is required."),
    ])

    left, right = st.columns([2, 1])
    with left:
        st.subheader("Hot Leads - Immediate Action Required")
        hot_df = leads[leads["Lead_Category"] == "Hot"].sort_values("Lead_Score", ascending=False).head(8)
        if hot_df.empty:
            st.info("No Hot leads at the current threshold.")
        for _, row in hot_df.iterrows():
            lead_id = row.get("Lead Number", row.get("Prospect ID", "Unknown Lead"))
            with st.container(border=True):
                st.markdown(f"**Lead #{lead_id}**")
                st.write(f"{row['Lead_Score']:.1f} score | {row['Conversion_Probability']:.1%} conversion")
                st.caption(f"{row.get('Lead Origin', 'Unknown')} | {row.get('What is your current occupation', 'Unknown')} | {row.get('City', 'Unknown')}")
                st.write(f"Key driver: {row.get('Top_Driver', 'Model score')}")
                st.write(f"Recommended: {row.get('Recommended_Action', 'Prioritize outreach based on score.')}")
    with right:
        _quick_predictor(model, config)

    st.subheader("Lead Score Distribution")
    dist = leads.groupby("Lead_Category", as_index=False).agg(
        Leads=("Lead_Category", "size"),
        Average_Probability=("Conversion_Probability", "mean"),
    )
    fig = px.bar(dist, x="Lead_Category", y="Leads", color="Lead_Category",
                 color_discrete_map={"Hot": PALETTE["hot"], "Warm": PALETTE["warm"], "Cold": PALETTE["cold"]},
                 text="Leads")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Conversion Funnel")
    funnel = {
        "Stage": ["All Leads", "Scored Leads", "Warm + Hot", "Hot Leads", "Predicted Converters"],
        "Count": [total, total, int(leads["Lead_Category"].isin(["Warm", "Hot"]).sum()), hot, int((leads["Conversion_Probability"] >= 0.5).sum())],
    }
    st.caption("Model-based prioritization funnel. Actual CRM pipeline stages are unavailable.")
    st.plotly_chart(px.funnel(funnel, x="Count", y="Stage"), use_container_width=True)

    st.subheader("Model Health")
    st.success("Operational")
    cols = st.columns(4)
    for col, key in zip(cols, ["validation_roc_auc", "validation_pr_auc", "test_roc_auc", "test_pr_auc"]):
        col.metric(key.replace("_", " ").title(), config.get(key, "Not available"))
