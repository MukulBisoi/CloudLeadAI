import pandas as pd
import streamlit as st


def render():
    st.header("Project Overview & System Architecture")
    st.caption("How CloudLead AI transforms raw lead data into actionable sales intelligence.")
    c1, c2, c3 = st.columns(3)
    c1.markdown("**The Challenge**\n\nTraditional B2B lead scoring relies on static heuristics and can miss complex buyer behavior.")
    c2.markdown("**The Solution**\n\nCloudLead AI uses gradient-boosted decision trees to produce conversion probabilities and priority scores.")
    c3.markdown("**Core Value**\n\nPrioritize high-intent prospects, explain scoring drivers, and support data-driven sales workflows.")
    st.subheader("Current Streamlit Deployment")
    st.write("The current app loads saved model artifacts, scores leads, explains model signals, and supports CSV-based batch workflows.")
    st.subheader("Future Production Architecture")
    st.info("FastAPI, Celery, PostgreSQL, Redis, Salesforce, HubSpot, Slack, and email are target architecture components, not live integrations in this deployment.")
    st.graphviz_chart(
        """
        digraph {
          rankdir=TB;
          node [shape=box, style="rounded,filled", color="#CBD5E1", fillcolor="#FFFFFF"];
          sources [label="Lead Sources\\nCSV Upload | CRM | Website Telemetry"];
          ingest [label="Data Ingestion Layer\\nFastAPI | Celery | CSV Parser"];
          prep [label="Preprocessing & Feature Engineering\\nPandas | NumPy | Scikit-learn"];
          ml [label="ML & Inference Engine\\nXGBoost | CatBoost | SHAP"];
          store [label="PostgreSQL\\nLead History | Score Logs"];
          cache [label="Redis\\nDashboard Cache"];
          ui [label="CloudLead AI Dashboard\\nStreamlit UI"];
          actions [label="Sales Actions\\nCRM Sync | Email | Slack"];
          sources -> ingest -> prep -> ml -> ui -> actions;
          ml -> store; ml -> cache; store -> ui; cache -> ui;
        }
        """
    )
    st.subheader("Data Flow Pipeline")
    steps = ["New Lead", "Data Ingestion", "Validation", "Preprocessing", "Feature Engineering", "ML Inference", "Conversion Probability", "Lead Score 0-100", "Hot / Warm / Cold", "Feature Explanation", "Sales Recommendation", "Sales Outreach"]
    st.write(" -> ".join(steps))
    st.subheader("Architecture Technology Table")
    table = pd.DataFrame(
        [
            ["Data Ingestion", "FastAPI, Celery, CSV Parser", "Bulk uploads, CRM webhooks, telemetry"],
            ["Preprocessing", "Pandas, NumPy, Scikit-learn", "Validation, transformation, feature engineering"],
            ["ML Engine", "XGBoost, CatBoost, SHAP", "Prediction and explanation"],
            ["Data Layer", "PostgreSQL", "Future lead history and score logs"],
            ["Cache", "Redis", "Future dashboard acceleration"],
            ["Frontend", "Streamlit", "Current dashboard and workflows"],
            ["Integrations", "REST API / Webhooks", "Future CRM and notification integrations"],
        ],
        columns=["Architecture Layer", "Technology", "Responsibility"],
    )
    st.markdown(
        table.to_html(index=False, classes="architecture-table"),
        unsafe_allow_html=True,
    )
