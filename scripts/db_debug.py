import sqlite3, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
print('DB path:', DB_PATH)
print('Exists:', os.path.exists(DB_PATH))
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print('Tables:', tables)
    if 'components_and_parts' in tables:
        cur.execute('SELECT COUNT(*) FROM components_and_parts')
        print('components_and_parts count:', cur.fetchone()[0])
        cur.execute("SELECT id, part_number, description FROM components_and_parts ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        print('Last 10 rows (id, part_number, description):')
        for r in rows:
            print(r)
        cur.execute("SELECT COUNT(*) FROM components_and_parts WHERE part_number LIKE '%-BR-%'")
        print('BR count:', cur.fetchone()[0])
        cur.execute("SELECT COUNT(*) FROM components_and_parts WHERE part_number LIKE '%-US-%'")
        print('US count:', cur.fetchone()[0])
    else:
        print('components_and_parts table not found')
except Exception as e:
    print('Error:', e)
    sys.exit(1)
finally:
    try:
        conn.close()
    except:
        pass
