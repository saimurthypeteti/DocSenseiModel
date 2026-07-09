@echo off
cd /d "%~dp0"
echo Installing DocSensei dependencies...
py -m pip install -r requirements.txt
echo.
echo Starting DocSensei...
py -m streamlit run app.py
pause
