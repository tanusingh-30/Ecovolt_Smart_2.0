# EcoVolt Smart 2.0

Premium dark-themed Streamlit dashboard for a solar car project. The dashboard is hardware-independent and displays configured values from `config.py`.

## Files
- `app.py` — Streamlit dashboard, gauges, solar-car illustration, and temperature graph.
- `config.py` — battery, current, temperature, and display-threshold settings.
- `requirements.txt` — Python dependencies.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## Temperature graph note
The graph plots the configured temperature as a flat reference line. It does not fabricate historical readings; connect a sensor or provide real logged data before presenting it as a historical trend.
