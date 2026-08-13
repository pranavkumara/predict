# ⚙️ Predictive Maintenance System

AI-powered machine failure prediction system using **XGBoost**. Predicts whether industrial machines are likely to fail based on sensor readings (temperature, rotational speed, torque, tool wear) and provides risk-level classifications with maintenance recommendations.

<p align="center">
  <a href="https://YOUR_STREAMLIT_APP_URL" target="_blank"><strong>▶ Open the live app</strong></a>
</p>

<!--
  Not deployed yet: replace YOUR_STREAMLIT_APP_URL above and below with your
  real https://*.streamlit.app URL once you've followed "Deploying the live
  demo". Until then this embed will show Streamlit's "app not found" page.
-->
<iframe
  src="https://YOUR_STREAMLIT_APP_URL/?embed=true"
  height="800"
  width="100%"
  style="border:1px solid #ddd;border-radius:8px;"
  title="Predictive Maintenance System — live demo"
></iframe>

## Architecture

```
User → Streamlit Dashboard → FastAPI → XGBoost Model → Prediction + Risk Level
```

| Component   | Technology          | Purpose                          |
| ----------- | ------------------- | -------------------------------- |
| **API**     | FastAPI + Uvicorn   | REST API for predictions         |
| **Dashboard** | Streamlit         | Interactive web UI               |
| **Model**   | XGBoost (scikit-learn) | Binary classification          |
| **Config**  | Pydantic Settings   | Centralized configuration        |

## Project Structure

```
predictive-maintenance/
├── api/                    # FastAPI application
│   ├── main.py             # Endpoints: /, /health, /predict
│   └── schemas.py          # Pydantic request/response models
├── config/                 # Configuration management
│   └── settings.py         # Environment-based settings
├── dashboard/              # Streamlit frontend
│   └── app.py              # Interactive dashboard
├── data/                   # Datasets
│   └── ai4i2020.csv        # AI4I 2020 Predictive Maintenance Dataset
├── models/                 # Trained model artifacts
│   └── predictive_maintenance_model.pkl
├── notebooks/              # Jupyter notebooks (EDA → Training)
│   ├── 01_data_understanding.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
├── scripts/                # Convenience runner scripts
│   ├── run_api.py
│   └── run_dashboard.py
├── src/                    # Shared utilities
│   ├── constants.py        # Risk thresholds, feature columns
│   └── model_loader.py     # Reusable model loading
├── tests/                  # Test suite
│   ├── test_api.py
│   └── test_schemas.py
├── .env.example            # Environment variable template
├── .gitignore
├── pyproject.toml          # Project metadata & dependencies
├── requirements.txt        # Flat dependency list
└── README.md
```

## Setup

### 1. Clone & create virtual environment

```bash
git clone <repository-url>
cd predictive-maintenance

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or with optional groups:

```bash
# Development tools (pytest, ruff)
pip install -e ".[dev]"

# Jupyter notebooks
pip install -e ".[notebook]"
```

### 3. Configure environment (optional)

```bash
copy .env.example .env
# Edit .env to override defaults
```

## Running

### Start the API

```bash
python scripts/run_api.py
```

The API will be available at `http://127.0.0.1:8000`.

- Swagger docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Start the Dashboard

```bash
python scripts/run_dashboard.py
```

Opens at `http://127.0.0.1:8501`. Make sure the API is running first.

## Deploying the live demo

The dashboard can run standalone — if it can't reach the API at `http://127.0.0.1:8000`, it automatically starts the API in a background thread inside the same process (see `dashboard/app.py`). That means the whole app deploys as a single Streamlit service, no separate backend host needed:

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io), sign in with GitHub, and create a new app.
3. Pick this repo/branch, and set the main file path to `dashboard/app.py`.
4. Deploy. Streamlit Cloud installs `requirements.txt` and starts `dashboard/app.py`, which loads the model and boots the API automatically on first load.
5. Copy the resulting `https://*.streamlit.app` URL and replace **every** `YOUR_STREAMLIT_APP_URL` placeholder in this README (the "Open the live app" link and the `<iframe src="...">` near the top) with it — instead of a `localhost` URL, which only ever works on your own machine.

## API Usage

### Predict machine failure

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "machine_type": "M",
    "air_temperature": 298.1,
    "process_temperature": 308.6,
    "rotational_speed": 1551,
    "torque": 42.8,
    "tool_wear": 0
  }'
```

Response:

```json
{
  "prediction": 0,
  "failure_probability": 0.0312,
  "risk_level": "LOW",
  "recommendation": "Machine operating normally. Continue regular monitoring."
}
```

### Risk levels

| Probability  | Risk Level | Action                         |
| ------------ | ---------- | ------------------------------ |
| ≥ 70%        | **HIGH**   | Immediate inspection           |
| 40% – 69%   | **MEDIUM** | Monitor & preventive maintenance |
| < 40%        | **LOW**    | Continue normal monitoring     |

## Testing

```bash
python -m pytest tests/ -v
```

## Notebooks

The `notebooks/` directory contains the full ML pipeline:

1. **01_data_understanding.ipynb** — Dataset exploration and summary statistics
2. **02_eda.ipynb** — Exploratory data analysis and visualizations
3. **03_feature_engineering.ipynb** — Feature encoding and selection
4. **04_model_training.ipynb** — Model training, tuning, and evaluation

## Dataset

[AI4I 2020 Predictive Maintenance Dataset](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset) — 10,000 machine records with 14 features including air/process temperature, rotational speed, torque, and tool wear.
