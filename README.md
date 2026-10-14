# EcoVolt Smart 2.0

A hardware-independent Streamlit dashboard for a solar-car project. The dashboard displays values configured in `config.py`; it does not connect to physical sensors.

## Configured values
- Battery charge: 83%
- Electrical current: 300 mA
- Room temperature: 25°C, explicitly marked as a placeholder

Edit these constants in `config.py` to change the displayed values.

## Run on Windows
1. Install Python 3.10 or newer.
2. Open Command Prompt in this folder.
3. Create and activate a virtual environment:
   ```bat
   python -m venv .venv
   .venv\Scripts\activate
   ```
4. Install requirements:
   ```bat
   python -m pip install -r requirements.txt
   ```
5. Start the dashboard:
   ```bat
   python -m streamlit run app.py
   ```

If `streamlit` opens in a browser automatically, use the local URL printed in the terminal.
