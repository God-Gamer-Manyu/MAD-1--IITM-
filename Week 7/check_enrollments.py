import sqlite3, os
DB = os.path.join(os.path.dirname(__file__), 'week7_database.sqlite3')
if not os.path.exists(DB):
    print('DB missing', DB)
    raise SystemExit(1)
conn = sqlite3.connect(DB)
cur = conn.cursor()
print('All tables:')
for r in cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'"):
    print(r[0])
    print(r[1])
    print('---')

print('\nCheck enrollments pragma:')
try:
    for col in cur.execute("PRAGMA table_info('enrollments')"):
        print(col)
except Exception as e:
    print('PRAGMA enrollments error:', e)

conn.close()
