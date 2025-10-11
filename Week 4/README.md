Week 4 - Flask data viewer

This folder contains a simple Flask app that reads `data.csv` and provides two views:

- `/student?s=<student_id>` — shows all courses and marks for the given student and the total marks.
- `/course?c=<course_id>` — shows average and maximum marks for the given course and a bar chart of the marks frequency.

How to run

1. Ensure you have Python and the packages installed. Recommended minimal virtualenv and install:

```cmd
python -m venv .venv
.venv\Scripts\activate
pip install flask matplotlib
```

2. Run the app:

```cmd
python app.py
```

3. Open http://127.0.0.1:5000/ in your browser and use the forms, or call endpoints directly:

- http://127.0.0.1:5000/student?s=1001
- http://127.0.0.1:5000/course?c=2001

Notes

- The app writes generated chart images into `static/images/`.
- `data.csv` should be in the same folder as `app.py`.
