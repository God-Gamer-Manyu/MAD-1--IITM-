# Week 7 — Flask + SQLAlchemy small app

Files for the Week 7 assignment are in this folder. The app uses Flask, Flask-SQLAlchemy and matplotlib (for charts).

Quick start (Windows cmd, using the venv you provided):

```cmd
:: activate the venv you created
D:\Python_venv\Normal_App_Windows\Scripts\activate.bat

:: install deps (only if needed)
python -m pip install -r requirements.txt

:: initialize the database (creates sample data)
python init_db.py

:: run the app
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

Notes:
- Database file: `week7_database.sqlite3` (created in this folder).
- Chart images are generated into `static/images`.
