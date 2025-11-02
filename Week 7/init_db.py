"""Initialize the week7 database with sample data.

Run this from the Week 7 directory (or with python pointing to project root):
    D:\\Python_venv\\Normal_App_Windows\\Scripts\\activate.bat
    python init_db.py
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'week7_database.sqlite3')


def init_db():
    """Idempotently create missing tables (course, enrollments) and insert example rows into
    student/course/enrollments tables. If a table exists, it will be used as-is; existing rows
    are not duplicated (we use INSERT OR IGNORE for unique columns).
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # enable foreign keys
    cur.execute('PRAGMA foreign_keys = ON')

    # detect existing tables (case-insensitive search for expected names)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]

    def find_table(name):
        low = name.lower()
        for t in tables:
            if t.lower() == low:
                return t
        for t in tables:
            if low in t.lower():
                return t
        return None

    student_table = find_table('student')
    if not student_table:
        student_table = 'student'
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS student (
                student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll_number TEXT UNIQUE NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT
            )''')

    course_table = find_table('course')
    if not course_table:
        course_table = 'course'
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS course (
                course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_code TEXT UNIQUE NOT NULL,
                course_name TEXT NOT NULL,
                course_description TEXT
            )''')

    enroll_table = find_table('enrollments')
    if not enroll_table:
        enroll_table = 'enrollments'
        cur.execute(
            '''CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER NOT NULL,
                course_id INTEGER NOT NULL,
                FOREIGN KEY(student_id) REFERENCES student(student_id),
                FOREIGN KEY(course_id) REFERENCES course(course_id)
            )''')

    # refresh table list after potential creation
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    # ensure our variables point to actual names
    student_table = find_table('student') or student_table
    course_table = find_table('course') or course_table
    enroll_table = find_table('enrollments') or enroll_table

    # example students and courses
    students = [
        ("R001", "Alice", "Anderson"),
        ("R002", "Bob", "Brown"),
        ("R003", "Charlie", "Clark"),
    ]
    courses = [
        ("MATH101", "Mathematics", "Basic mathematics"),
        ("PHY101", "Physics", "Introductory physics"),
        ("CS101", "Programming", "Intro to programming"),
    ]

    # insert students (roll_number unique) - use INSERT OR IGNORE
    for roll, first, last in students:
        cur.execute(f"INSERT OR IGNORE INTO {student_table} (roll_number, first_name, last_name) VALUES (?, ?, ?)", (roll, first, last))

    # insert courses
    for code, name, desc in courses:
        cur.execute("INSERT OR IGNORE INTO course (course_code, course_name, course_description) VALUES (?, ?, ?)", (code, name, desc))

    conn.commit()

    # insert enrollments only if table empty
    cur.execute(f"SELECT COUNT(*) FROM {enroll_table}")
    count = cur.fetchone()[0]
    if count == 0:
        # get ids from actual student/course tables
        cur.execute(f"SELECT student_id, roll_number FROM {student_table}")
        students_map = {r[1]: r[0] for r in cur.fetchall()}
        cur.execute(f"SELECT course_id, course_code FROM {course_table}")
        courses_map = {r[1]: r[0] for r in cur.fetchall()}

        examples = [
            (students_map['R001'], courses_map['MATH101']),
            (students_map['R001'], courses_map['PHY101']),
            (students_map['R001'], courses_map['CS101']),
            (students_map['R002'], courses_map['MATH101']),
            (students_map['R002'], courses_map['CS101']),
            (students_map['R003'], courses_map['MATH101']),
            (students_map['R003'], courses_map['PHY101']),
        ]

        # determine actual column names in enrollments table
        cols = [c[1] for c in cur.execute(f"PRAGMA table_info('{enroll_table}')")]
        s_col = next((c for c in cols if 'student' in c.lower()), None)
        c_col = next((c for c in cols if 'course' in c.lower()), None)
        if not s_col or not c_col:
            raise RuntimeError(f"Cannot determine student/course columns in {enroll_table}: {cols}")

        for sid, cid in examples:
            cur.execute(f"INSERT INTO {enroll_table} ({s_col}, {c_col}) VALUES (?, ?)", (sid, cid))
        conn.commit()
        print('Inserted example enrollments.')
    else:
        print('Enrollments already present; skipping enrollment insertion.')

    print('init_db: done. DB file:', DB_PATH)
    conn.close()


if __name__ == '__main__':
    # import the Flask app and use its context when initializing the DB
    from app import app
    with app.app_context():
        init_db()
