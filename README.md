# CloudLead AI

Streamlit app for scoring a lead's conversion probability and classifying it as
Hot, Warm, or Cold.

## Run locally

From this folder, create or activate a virtual environment and install the
artifact-compatible dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

The files `cloudlead_model.pkl` and `cloudlead_config.pkl` must remain beside
`app.py`. The scikit-learn version is pinned because the saved pipeline was
created with scikit-learn 1.6.1.

## Streamlit Community Cloud

Deploy the repository, set the main file to `app.py`, and Streamlit will install
the dependencies from `requirements.txt`. Keep both model artifacts committed
to the repository or provide them through the deployment's configured storage.
