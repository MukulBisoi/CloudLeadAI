import streamlit as st

from utils.data_processing import available_options, lead_id_column


def render(config, leads):
    st.header("Lead Directory")
    st.caption("Search, filter and prioritize every scored prospect.")
    if leads.empty:
        st.warning("No lead data is available.")
        return
    df = leads.copy()
    id_col = lead_id_column(df)
    c1, c2, c3, c4 = st.columns(4)
    search = c1.text_input("Search Lead ID")
    category = c2.multiselect("Lead Category", ["Hot", "Warm", "Cold"], default=["Hot", "Warm", "Cold"])
    score_range = c3.slider("Score range", 0, 100, (0, 100))
    prob_range = c4.slider("Conversion probability", 0, 100, (0, 100))
    for col in ["Lead Origin", "What is your current occupation", "City"]:
        opts = available_options(df, col)
        if opts:
            choice = st.multiselect(col, opts)
            if choice:
                df = df[df[col].astype(str).isin(choice)]
    if search and id_col:
        df = df[df[id_col].astype(str).str.contains(search, case=False, na=False)]
    df = df[df["Lead_Category"].isin(category)]
    df = df[df["Lead_Score"].between(score_range[0], score_range[1])]
    df = df[(df["Conversion_Probability"] * 100).between(prob_range[0], prob_range[1])]
    df = df.sort_values("Lead_Score", ascending=False)
    cols = [c for c in [id_col, "Lead_Score", "Conversion_Probability", "Lead_Category", "Lead Origin",
                        "What is your current occupation", "City", "TotalVisits",
                        "Total Time Spent on Website", "Top_Driver", "Recommended_Action"] if c and c in df.columns]
    st.dataframe(df[cols], use_container_width=True, hide_index=True)
    st.caption("Contact actions use real contact details only. This dataset does not include email, phone, or CRM profile fields.")
