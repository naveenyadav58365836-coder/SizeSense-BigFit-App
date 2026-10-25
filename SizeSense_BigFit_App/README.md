# SizeSense — BigFit Inventory Agent

A small Streamlit inventory dashboard prototype.

## Run in VS Code (Windows)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ and enable **Add Python to PATH**.
2. Extract this ZIP and open the extracted `SizeSense_BigFit_App` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, then activate again. Alternatively use Command Prompt and run `.venv\Scripts\activate.bat`.

5. Install packages:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

6. Start the app:

   ```powershell
   python -m streamlit run app.py
   ```

7. Open the local URL printed in the terminal, usually http://localhost:8501.

## CSV format

For the built-in metrics, the uploaded CSV should include `Stock`. For size charts, include `Size`. For replenishment suggestions, include `Weekly Demand`. Optional columns include `Product`, `Store`, and `Unit Price`.

This is a prototype with demo data. Recommendations are not automatically applied to live inventory.
