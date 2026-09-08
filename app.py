import joblib
import pandas as pd
import streamlit as st
from pathlib import Path


# ============================================================
# Page configuration
# ============================================================

st.set_page_config(
    page_title="CloudLead AI",
    page_icon="🎯",
    layout="centered",
)


# ============================================================
# Load model and configuration
# ============================================================

@st.cache_resource
def load_artifacts():
    project_dir = Path(__file__).resolve().parent
    model_path = project_dir / "cloudlead_model.pkl"
    config_path = project_dir / "cloudlead_config.pkl"

    missing_files = [
        str(path.name) for path in (model_path, config_path) if not path.exists()
    ]
    if missing_files:
        raise FileNotFoundError(
            "Missing model artifacts: " + ", ".join(missing_files)
        )

    model = joblib.load(model_path)
    config = joblib.load(config_path)

    return model, config


try:
    model, config = load_artifacts()
except Exception as error:
    st.error("CloudLead AI could not load its model artifacts.")
    st.code(str(error))
    st.info(
        "Install the dependencies from requirements.txt and keep the .pkl "
        "files beside app.py."
    )
    st.stop()

threshold = config["hot_lead_threshold"]

numeric_features = config["numeric_features"]
categorical_features = config["categorical_features"]


# ============================================================
# Title
# ============================================================

st.title("CloudLead AI")
st.subheader("Hot Lead Prediction & Lead Scoring")

st.write(
    "Enter the available lead information below to estimate "
    "the probability that the lead will convert."
)


# ============================================================
# Helper functions
# ============================================================

def yes_no_to_string(value):
    return "Yes" if value else "No"


def get_category(probability):

    if probability >= threshold:
        return "Hot Lead"

    elif probability >= 0.50:
        return "Warm Lead"

    else:
        return "Cold Lead"


def predict_lead(input_data):
    probability = float(model.predict_proba(input_data)[0][1])

    score = probability * 100

    category = get_category(probability)

    return probability, score, category


# ============================================================
# Input section
# ============================================================

st.header("Lead Information")


lead_origin = st.selectbox(
    "Lead Origin",
    [
        "API",
        "Landing Page Submission",
        "Lead Add Form",
        "Lead Import",
        "Quick Add Form"
    ]
)


lead_source = st.text_input(
    "Lead Source",
    value="Google"
)


do_not_email = st.selectbox(
    "Do Not Email",
    ["No", "Yes"]
)


do_not_call = st.selectbox(
    "Do Not Call",
    ["No", "Yes"]
)


total_visits = st.number_input(
    "Total Visits",
    min_value=0.0,
    value=3.0,
    step=1.0
)


total_time = st.number_input(
    "Total Time Spent on Website",
    min_value=0,
    value=500,
    step=10
)


page_views = st.number_input(
    "Page Views Per Visit",
    min_value=0.0,
    value=2.0,
    step=0.1
)


country = st.text_input(
    "Country",
    value="India"
)


specialization = st.text_input(
    "Specialization",
    value="Unknown"
)


how_heard = st.text_input(
    "How did you hear about X Education",
    value="Unknown"
)


occupation = st.text_input(
    "Current Occupation",
    value="Unemployed"
)


course_motivation = st.text_input(
    "What matters most to you in choosing a course",
    value="Better Career Prospects"
)


search = st.selectbox(
    "Search",
    ["No", "Yes"]
)


magazine = st.selectbox(
    "Magazine",
    ["No", "Yes"]
)


newspaper_article = st.selectbox(
    "Newspaper Article",
    ["No", "Yes"]
)


x_education_forums = st.selectbox(
    "X Education Forums",
    ["No", "Yes"]
)


newspaper = st.selectbox(
    "Newspaper",
    ["No", "Yes"]
)


digital_advertisement = st.selectbox(
    "Digital Advertisement",
    ["No", "Yes"]
)


through_recommendations = st.selectbox(
    "Through Recommendations",
    ["No", "Yes"]
)


receive_updates = st.selectbox(
    "Receive More Updates About Our Courses",
    ["No", "Yes"]
)


supply_chain_updates = st.selectbox(
    "Update me on Supply Chain Content",
    ["No", "Yes"]
)


dm_updates = st.selectbox(
    "Get updates on DM Content",
    ["No", "Yes"]
)


city = st.text_input(
    "City",
    value="Unknown"
)


cheque_agreement = st.selectbox(
    "I agree to pay the amount through cheque",
    ["No", "Yes"]
)


mastering_interview = st.selectbox(
    "A free copy of Mastering The Interview",
    ["No", "Yes"]
)


# ============================================================
# Prediction button
# ============================================================

if st.button("Predict Lead Score", type="primary", use_container_width=True):

    input_data = pd.DataFrame([{

        "Lead Origin": lead_origin,
        "Lead Source": lead_source,
        "Do Not Email": do_not_email,
        "Do Not Call": do_not_call,
        "TotalVisits": total_visits,
        "Total Time Spent on Website": total_time,
        "Page Views Per Visit": page_views,
        "Country": country,
        "Specialization": specialization,
        "How did you hear about X Education": how_heard,
        "What is your current occupation": occupation,
        "What matters most to you in choosing a course": course_motivation,
        "Search": search,
        "Magazine": magazine,
        "Newspaper Article": newspaper_article,
        "X Education Forums": x_education_forums,
        "Newspaper": newspaper,
        "Digital Advertisement": digital_advertisement,
        "Through Recommendations": through_recommendations,
        "Receive More Updates About Our Courses": receive_updates,
        "Update me on Supply Chain Content": supply_chain_updates,
        "Get updates on DM Content": dm_updates,
        "City": city,
        "I agree to pay the amount through cheque": cheque_agreement,
        "A free copy of Mastering The Interview": mastering_interview
    }])


    # Keep the inference schema identical to the schema used during training.
    input_data = input_data.reindex(columns=numeric_features + categorical_features)


    probability, score, category = predict_lead(
        input_data
    )


    # ========================================================
    # Results
    # ========================================================

    st.divider()

    st.header("Prediction Result")


    col1, col2 = st.columns(2)


    with col1:
        st.metric(
            "Lead Score",
            f"{score:.2f} / 100"
        )


    with col2:
        st.metric(
            "Conversion Probability",
            f"{probability:.2%}"
        )


    if category == "Hot Lead":

        st.success(
            "HOT LEAD — High Priority"
        )

        st.write(
            "This lead has an estimated conversion probability "
            f"of {probability:.2%}, which is above the Hot Lead "
            f"threshold of {threshold:.2f}."
        )


    elif category == "Warm Lead":

        st.warning(
            "WARM LEAD — Medium Priority"
        )

        st.write(
            "This lead shows moderate conversion potential."
        )


    else:

        st.info(
            "COLD LEAD — Lower Priority"
        )

        st.write(
            "This lead has a relatively low estimated "
            "conversion probability."
        )


    st.caption(
        f"Hot Lead threshold: {threshold:.2f}"
    )   