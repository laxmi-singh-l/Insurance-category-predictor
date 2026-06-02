# Insurance Premium Category Predictor

Simple frontend for predicting insurance premium categories.

## Prerequisites
- Python 3.8 or newer
- Internet access to install packages

## Quick setup (Windows)

1. Create and activate a virtual environment

PowerShell:
```
python -m venv venv
venv\Scripts\Activate.ps1
```

Command Prompt (cmd.exe):
```
python -m venv venv
venv\Scripts\activate.bat
```

2. Install dependencies

```
pip install streamlit requests
```

3. Run the frontend

By default the frontend expects an API at `http://127.0.0.1:8001/predict`.

```
streamlit run frontend.py
```

If your API is hosted at a different URL, set the `API_URL` environment variable before running Streamlit.

PowerShell example:
```
$env:API_URL = "http://your-api-host:8001/predict"
streamlit run frontend.py
```

CMD example:
```
set API_URL=http://your-api-host:8001/predict
streamlit run frontend.py
```

4. (Optional) Run the API

If the repository includes an API (for example in `app.py`), you can run it with a server such as Uvicorn. Example (if `app.py` defines a FastAPI `app` object):

```
pip install uvicorn fastapi
uvicorn app:app --reload --port 8001
```

