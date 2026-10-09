# PatchPilot

Review-first coding assistant: submit a task and code to get findings, a suggested full patch, test ideas, and a unified diff. No generated code is executed.

## Model
NVIDIA Nemotron through Nebius Token Factory API. Default model: `nvidia/nemotron-3-super-120b-a12b`.

## Run locally
1. Python 3.10+
2. `python -m venv .venv` and activate.
3. `pip install -r requirements.txt`
4. Set `NEBIUS_API_KEY` or enter it in the app sidebar. Never commit the key.
5. `streamlit run app.py`

For hosted deployment, publish the repo to GitHub, create an app on Streamlit Community Cloud, select `app.py`, and set `NEBIUS_API_KEY` in the app secrets.

Review all model output. The app does not claim tests passed and never runs the generated patch. MIT license in LICENSE.
