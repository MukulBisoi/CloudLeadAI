import plotly.express as px
import streamlit as st

from utils.data_processing import lead_id_column
from utils.explanations import explain_lead


def render(model, config, leads):
    st.header("Lead Profile & AI Explainer")
    if leads.empty:
        st.warning("No scored leads are available.")
        return
    id_col = lead_id_column(leads)
    if not id_col:
        st.warning("No lead identifier column was found.")
        return
    ids = leads[id_col].astype(str).tolist()
    selected = st.selectbox("Select a lead", ids, index=0)
    row = leads[leads[id_col].astype(str) == selected].iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("Lead Score", f"{row['Lead_Score']:.1f}")
    c2.metric("Conversion Probability", f"{row['Conversion_Probability']:.1%}")
    c3.metric("Category", row["Lead_Category"])
    overview_cols = [id_col, "Lead Origin", "Lead Source", "What is your current occupation", "City",
                     "TotalVisits", "Total Time Spent on Website", "Page Views Per Visit"]
    overview = row[[c for c in overview_cols if c in leads.columns]].to_frame("Value")
    overview["Value"] = overview["Value"].astype(str)
    st.dataframe(overview, use_container_width=True)
    positives, negatives, note = explain_lead(row, model, config)
    st.subheader("Why did this lead receive this score?")
    st.caption(note)
    left, right = st.columns(2)
    with left:
        st.markdown("**Positive Drivers**")
        st.dataframe(positives, hide_index=True, use_container_width=True)
    with right:
        st.markdown("**Negative Drivers**")
        st.dataframe(negatives, hide_index=True, use_container_width=True)
    if not positives.empty:
        fig = px.bar(positives, x="Contribution", y="Feature", orientation="h")
        st.plotly_chart(fig, use_container_width=True)
    st.subheader("Recommended Sales Action")
    st.write(row.get("Recommended_Action", "Prioritize outreach based on score."))
    st.caption(f"Why: {row.get('Top_Driver', 'Model score')}")
