from pathlib import Path

import streamlit as st

from utils.data_processing import load_scored_leads
from utils.model_loader import artifact_status, load_artifacts
from utils.ui import apply_theme, page_header, top_model_status


st.set_page_config(
    page_title="CloudLead AI",
    page_icon="CL",
    layout="wide",
    initial_sidebar_state="collapsed",
)
apply_theme()


PAGES = {
    "Dashboard": "dashboard",
    "Lead Directory & Pipeline": "directory",
    "Lead Profile & AI Explainer": "profile",
    "Batch Scoring & Data Ingestion": "batch",
    "Model Analytics & Health": "analytics",
    "Project Overview & System Architecture": "overview",
    "Settings & CRM Integrations": "settings",
}


def boot():
    status = artifact_status()
    if not status["config_exists"]:
        st.error("Model configuration not found.")
        st.info("Place cloudlead_config.pkl in the models directory.")
        st.stop()
    if not status["model_exists"]:
        st.error("Model artifact not found. Please place the trained model in the models directory.")
        st.stop()
    try:
        return load_artifacts()
    except Exception as exc:
        st.error("CloudLead AI could not load its deployment artifacts.")
        st.code(str(exc))
        st.info("Use the artifact-compatible environment from requirements.txt. The saved pipeline requires scikit-learn 1.6.1.")
        st.stop()


model, config = boot()
if "hot_lead_threshold" not in st.session_state:
    st.session_state.hot_lead_threshold = float(config.get("hot_lead_threshold", 0.72))

page_header("CloudLead AI", "AI-Powered B2B Lead Scoring & Sales Intelligence")
top_model_status(config)
st.markdown('<div class="top-nav">', unsafe_allow_html=True)
selected = st.segmented_control(
    "Navigation",
    list(PAGES),
    default="Dashboard",
    label_visibility="collapsed",
)
st.markdown("</div>", unsafe_allow_html=True)
if selected is None:
    selected = "Dashboard"

scored_leads = load_scored_leads(model, config, st.session_state.hot_lead_threshold)

page = PAGES[selected]
if page == "dashboard":
    from views import dashboard

    dashboard.render(model, config, scored_leads)
elif page == "directory":
    from views import lead_directory

    lead_directory.render(config, scored_leads)
elif page == "profile":
    from views import lead_profile

    lead_profile.render(model, config, scored_leads)
elif page == "batch":
    from views import batch_scoring

    batch_scoring.render(model, config)
elif page == "analytics":
    from views import model_analytics

    model_analytics.render(model, config, scored_leads)
elif page == "overview":
    from views import project_overview

    project_overview.render()
elif page == "settings":
    from views import settings

    settings.render(config)

st.caption(f"Deployment root: {Path(__file__).resolve().parent}")
