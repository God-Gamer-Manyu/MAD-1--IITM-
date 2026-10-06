# Modern Application Development I (IIT Madras): Coursework

Weekly assignments for **Modern Application Development I (MAD-1)** in the IIT Madras BS in Data Science & Applications program. The work progresses from static HTML pages to **Jinja2 templating**, a **Flask** web app, and finally a full **CRUD application backed by SQLite and SQLAlchemy**. A few **GitHub Actions** workflows are included as well.

---

## 📂 Contents

| Folder | Topic | What it does |
|---|---|---|
| `Week 2/` | HTML & static sites | Multi-page personal website (home, academics, personal, contact, resume) |
| `Week 3/` | Python + Jinja2 + Matplotlib | CLI (`app.py -s <student_id>` / `-c <course_id>`) that reads `data.csv` and renders an HTML report (`output.html`) with a marks-frequency histogram |
| `Week 4/` | Flask | Web version of Week 3: `/student?s=<id>` (marks and total), `/course?c=<id>` (average, max, bar chart) |
| `Week 7/` | Flask + SQLAlchemy + SQLite | Student–Course–Enrollment management app with full CRUD, relationships and charts |
| `.github/workflows/` | CI/CD | Hello-world workflow, dependency caching, and **GitHub Pages** deployment of the static site |

---

## 🏗️ Architecture & Concepts

### Week 7: Flask MVC + ORM

```
Browser ──HTTP──► Flask routes (controllers, app.py)
                     │  forms / flash messages
                     ▼
              SQLAlchemy ORM models ──► SQLite (week7_database.sqlite3)
              Student 1───* Enrollment *───1 Course
                     │
                     ▼
              Jinja2 templates (base.html → students / courses / enrollments views)
              Matplotlib (Agg backend) → charts in static/images
```

- **Models:** `Student`, `Course`, `Enrollment`, with `db.relationship` / `back_populates` and cascade deletes; models are mapped onto an existing schema (custom table and column names)
- **Routes:** create, read, update and delete for students and courses; enrolment management; duplicate-key validation with a custom error page
- **Helpers:** `init_db.py` seeds sample data; `inspect_db.py` and `check_enrollments.py` inspect the DB; `smoketest.py` runs quick endpoint checks

**Concepts:** HTML/CSS · Jinja2 templating and template inheritance · MVC pattern · Flask routing, query params and forms · **SQL / relational modelling** (one-to-many, many-to-many through an association table) · **SQLAlchemy ORM** · server-side chart generation (Matplotlib) · CLI argument parsing (`argparse`) · **GitHub Actions** (CI, caching, Pages deployment)

---

## ⚙️ Getting Started

```bash
git clone https://github.com/God-Gamer-Manyu/MAD-1--IITM-.git
cd MAD-1--IITM-
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
```

**Week 3: CLI report generator**
```bash
cd "Week 3"
pip install jinja2 matplotlib
python app.py -s 1001     # student report  → output.html
python app.py -c 2001     # course report   → output.html + 2001.png
```

**Week 4: Flask data viewer**
```bash
cd "Week 4"
pip install flask matplotlib
python app.py             # → http://127.0.0.1:5000/student?s=1001
```

**Week 7: Flask + SQLAlchemy CRUD app**
```bash
cd "Week 7"
pip install -r requirements.txt
python init_db.py         # optional: (re)create sample data
python app.py             # → http://127.0.0.1:5000
```

**Week 2: static site**: open `Week 2/index.html` in a browser.

## 🛠️ Tech Stack

`HTML` · `CSS` · `Python` · `Flask` · `Jinja2` · `SQLAlchemy` · `SQLite` · `Matplotlib` · `GitHub Actions` · `GitHub Pages`

## 👤 Author

**Rtamanyu N J**, [@God-Gamer-Manyu](https://github.com/God-Gamer-Manyu)
