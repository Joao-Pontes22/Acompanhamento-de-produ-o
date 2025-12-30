import sqlite3
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
TARGET = '012453bf5fc6'

print('DB path:', DB_PATH)
try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)')
    cur.execute('DELETE FROM alembic_version')
    cur.execute('INSERT INTO alembic_version (version_num) VALUES (?)', (TARGET,))
    conn.commit()
    cur.execute('SELECT version_num FROM alembic_version')
    row = cur.fetchone()
    print('Updated version_num ->', row[0] if row else None)
except Exception as e:
    print('Error:', e)
finally:
    try:
        conn.close()
    except:
        pass
