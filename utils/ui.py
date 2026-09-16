import streamlit as st


PALETTE = {
    "charcoal": "#0F172A",
    "canvas": "#F8FAFC",
    "indigo": "#4F46E5",
    "hot": "#10B981",
    "warm": "#F59E0B",
    "cold": "#EF4444",
}


def apply_theme():
    st.markdown(
        f"""
        <style>
        .stApp {{ background: {PALETTE['canvas']}; color: {PALETTE['charcoal']}; }}
        section[data-testid="stSidebar"] {{ background: {PALETTE['charcoal']}; }}
        section[data-testid="stSidebar"] * {{ color: #E5E7EB !important; }}
        section.main label,
        section.main label p,
        div[data-testid="stNumberInput"] label,
        div[data-testid="stNumberInput"] label p,
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextInput"] label p,
        div[data-testid="stSelectbox"] label,
        div[data-testid="stSelectbox"] label p,
        div[data-testid="stSlider"] label,
        div[data-testid="stSlider"] label p,
        div[data-testid="stMultiSelect"] label,
        div[data-testid="stMultiSelect"] label p {{
            color: #0F172A !important;
            opacity: 1 !important;
            visibility: visible !important;
        }}
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] label p {{
            color: #E5E7EB !important;
        }}
        .brand {{ font-size: 1.45rem; font-weight: 800; color: white; margin: .35rem 0 0; }}
        .tagline {{ color: #CBD5E1; font-size: .86rem; margin-bottom: 1.25rem; }}
        .hero, .metric-card, .card {{
            background: white; border: 1px solid #E2E8F0; border-radius: 8px;
            padding: 1rem; box-shadow: 0 1px 2px rgba(15,23,42,.05);
        }}
        .hero {{ padding: 1.35rem 1.5rem; margin-bottom: 1rem; }}
        .hero h1 {{ margin: 0; font-size: 2rem; letter-spacing: 0; }}
        .hero p {{ margin: .25rem 0 0; color: #64748B; }}
        .model-strip {{
            display: flex; gap: 1rem; align-items: center; flex-wrap: wrap;
            background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
            padding: .65rem .85rem; margin: -.35rem 0 .75rem;
            color: #0F172A;
        }}
        .model-strip strong {{ color: #0F172A; }}
        .model-strip span {{ color: #475569; }}
        .model-dot {{ color: #10B981 !important; font-weight: 900; }}
        .top-nav {{
            background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px;
            padding: .35rem; margin-bottom: 1rem; overflow-x: auto;
        }}
        .top-nav div[data-baseweb="button-group"] {{
            display: flex; flex-wrap: wrap; gap: .35rem;
        }}
        .top-nav button {{
            border-radius: 6px !important;
            color: #0F172A !important;
            border-color: #CBD5E1 !important;
            background: #FFFFFF !important;
            font-weight: 700 !important;
        }}
        .top-nav button[aria-pressed="true"] {{
            background: #4F46E5 !important;
            color: #FFFFFF !important;
            border-color: #4F46E5 !important;
        }}
        .badge {{ display: inline-block; padding: .2rem .55rem; border-radius: 999px; font-size: .78rem; font-weight: 700; }}
        .hot {{ background: #D1FAE5; color: #065F46; }}
        .warm {{ background: #FEF3C7; color: #92400E; }}
        .cold {{ background: #FEE2E2; color: #991B1B; }}
        .muted {{ color: #64748B; }}
        .architecture-table {{
            width: 100%; border-collapse: collapse; background: #FFFFFF;
            border: 1px solid #E2E8F0; border-radius: 8px; overflow: hidden;
        }}
        .architecture-table th {{
            color: #0F172A; background: #EEF2FF; text-align: left;
            padding: .75rem; border-bottom: 1px solid #CBD5E1;
        }}
        .architecture-table td {{
            color: #0F172A; padding: .75rem; border-bottom: 1px solid #E2E8F0;
        }}
        div.stButton > button[kind="primary"] {{ background: {PALETTE['indigo']}; border-color: {PALETTE['indigo']}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title, subtitle):
    st.markdown(f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>', unsafe_allow_html=True)


def sidebar_status(config):
    model_name = config.get("model_name", "Unknown")
    st.markdown("**Model Status**")
    st.markdown('<span style="color:#10B981">●</span> Model Online', unsafe_allow_html=True)
    st.caption(f"Active Model: {model_name}")


def top_model_status(config):
    model_name = config.get("model_name", "Unknown")
    st.markdown(
        f"""
        <div class="model-strip">
            <strong>Model Status</strong>
            <span><span class="model-dot">●</span> Model Online</span>
            <span>Active Model: <strong>{model_name}</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def category_badge(category):
    css = {"Hot": "hot", "Warm": "warm", "Cold": "cold"}.get(category, "cold")
    return f'<span class="badge {css}">{category}</span>'


def metric_row(items):
    cols = st.columns(len(items))
    for col, (label, value, help_text) in zip(cols, items):
        with col:
            st.metric(label, value, help=help_text)
