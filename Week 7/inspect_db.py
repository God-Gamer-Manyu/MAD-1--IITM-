import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'week7_database.sqlite3')
print('DB path:', DB)
con = sqlite3.connect(DB)
cur = con.cursor()
print('\nTABLES:')
for row in cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'"):
    print(row[0])
    print(row[1])
    print('---')

print('\nPRAGMA enrollments:')
for row in cur.execute("PRAGMA table_info('enrollments')"):
    print(row)

print('\nPRAGMA student:')
for row in cur.execute("PRAGMA table_info('student')"):
    print(row)

print('\nPRAGMA course:')
for row in cur.execute("PRAGMA table_info('course')"):
    print(row)

con.close()
import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), 'week7_database.sqlite3')
if not os.path.exists(DB):
    print('DB not found at', DB)
    raise SystemExit(1)

conn = sqlite3.connect(DB)
cur = conn.cursor()
print('Tables:')
for row in cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'"):
    print('-', row[0])
    print(row[1])
    print('Columns:')
    for col in cur.execute(f"PRAGMA table_info('{row[0]}')"):
        print('   ', col)
    print()
conn.close()
