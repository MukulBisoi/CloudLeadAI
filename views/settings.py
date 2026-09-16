import streamlit as st


def render(config):
    st.header("Settings & CRM Integrations")
    st.subheader("Lead Threshold")
    default = float(config.get("hot_lead_threshold", 0.72))
    threshold = st.slider("Hot Lead Threshold", 0.50, 0.95, float(st.session_state.hot_lead_threshold), 0.01)
    st.session_state.hot_lead_threshold = threshold
    st.write(f"Probability: {threshold:.2f}")
    st.write(f"Score: {threshold * 100:.0f}")
    st.caption(f"Stored model default: {default:.2f}. This setting changes UI classification only and does not retrain or overwrite the model.")
    st.info(f"Hot: score >= {threshold * 100:.0f} | Warm: 50-{threshold * 100:.0f} | Cold: <50")
    st.subheader("CRM Integrations")
    for name, action in [("Salesforce", "Connect Salesforce"), ("HubSpot", "Connect HubSpot"), ("Slack", "Configure Alerts")]:
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 2, 1])
            c1.markdown(f"**{name}**")
            c2.warning("Not Connected")
            c3.button(action, disabled=True)
            st.caption("Integration framework ready - credentials required. Use st.secrets for API keys and tokens.")
