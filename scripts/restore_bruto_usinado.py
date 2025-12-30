import sqlite3
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'restore_bruto_usinado.log')

log = []
def add_log(msg):
    ts = datetime.utcnow().isoformat()
    log.append(f"[{ts}] {msg}")
    print(msg)

if not os.path.exists(DB_PATH):
    print('DB not found:', DB_PATH)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
try:
    cur.execute('SELECT id, part_number, description FROM components_and_parts')
    rows = cur.fetchall()
    updated = 0
    for id_, pn, desc in rows:
        desc = (desc or '').strip()
        lower = desc.lower()
        new_desc = desc
        if pn and '-BR-' in pn.upper():
            if 'bruto' not in lower:
                new_desc = (desc + ' Bruto').strip()
        if pn and '-US-' in pn.upper():
            if 'usinado' not in lower:
                new_desc = (new_desc + ' Usinado').strip()
        if new_desc != desc:
            cur.execute('UPDATE components_and_parts SET description = ? WHERE id = ?', (new_desc, id_))
            updated += 1
            add_log(f'Updated id={id_} pn={pn} -> "{new_desc}"')
    conn.commit()
    add_log(f'Total updated descriptions: {updated}')
    cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE part_number LIKE '%-BR-%' OR part_number LIKE '%-US-%' ORDER BY id DESC LIMIT 10")
    for r in cur.fetchall():
        add_log(str(r))
except Exception as e:
    conn.rollback()
    add_log('ERROR: ' + str(e))
finally:
    conn.close()
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        for l in log:
            f.write(l + '\n')
    add_log('Log appended to ' + LOG_PATH)
