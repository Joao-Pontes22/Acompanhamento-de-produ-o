import sqlite3, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM components_and_parts')
print('Total components_and_parts:', cur.fetchone()[0])
cur.execute("SELECT part_number, description FROM components_and_parts WHERE description LIKE '%Braço%' OR description LIKE '%braço%' LIMIT 50")
rows = cur.fetchall()
print('Braço-related rows sample:', len(rows))
for r in rows[:10]:
    print(r)
cur.execute('SELECT part_number, description FROM components_and_parts LIMIT 10')
for r in cur.fetchall():
    print(r)
conn.close()
