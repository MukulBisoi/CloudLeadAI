# CloudLead AI

AI-powered B2B lead scoring and sales intelligence built with Streamlit.

## Features

- Executive sales dashboard with lead KPIs, Hot lead feed, score distribution, and model-based funnel.
- Lead directory with search, category filters, score filtering, and prioritization.
- Single-lead profile with model-grounded drivers and deterministic sales recommendations.
- Batch CSV upload, validation, scoring, and downloadable results.
- Model health page with artifact checks, threshold views, cumulative gains, and feature importance.
- Settings page for UI threshold adjustment and integration placeholders.

## Architecture

The current deployment is a local Streamlit inference app. It loads saved artifacts and does not retrain models.

Future production components such as FastAPI, Celery, PostgreSQL, Redis, Salesforce, HubSpot, Slack, and email are shown as target architecture only. They are not live integrations in this codebase.

## Project Structure

```text
app.py
views/
utils/
models/
  cloudlead_model.pkl
  cloudlead_config.pkl
data/
  LeadScoring.csv
requirements.txt
README.md
.gitignore
```

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The saved scikit-learn pipeline requires `scikit-learn==1.6.1`.

## Running The App

```powershell
streamlit run app.py
```

## Model Artifacts

- `models/cloudlead_model.pkl`: saved XGBoost/scikit-learn inference pipeline.
- `models/cloudlead_catboost_model.cbm`: optional CatBoost artifact when the config selects CatBoost.
- `models/cloudlead_config.pkl`: deployment contract containing model name, threshold, numeric features, categorical features, and excluded columns.

The app reads artifacts from `models/` first and falls back to the project root for compatibility with the original notebook export.

## Batch Scoring

Upload a CSV containing every feature listed in:

- `config["numeric_features"]`
- `config["categorical_features"]`

The output preserves original columns and adds:

- `Conversion_Probability`
- `Lead_Score`
- `Lead_Category`
- `Top_Driver`
- `Recommended_Action`

## Deployment

For Streamlit Community Cloud, set `app.py` as the main file and include the model artifacts in the repository or provide them through configured deployment storage.

## Limitations

CRM integrations, PostgreSQL, Redis, FastAPI, Celery, Slack notifications, and email automation are future production components unless credentials and integration code are added. The app does not fabricate contact details, metrics, CRM stages, or live integrations.
