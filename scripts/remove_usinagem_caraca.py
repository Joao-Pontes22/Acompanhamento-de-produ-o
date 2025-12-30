import sqlite3
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG = os.path.join(os.path.dirname(__file__), 'remove_usinagem_caraca.log')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
pattern = re.compile(r"\businagem\b", re.IGNORECASE)
log_lines = []

def L(msg):
    ts = datetime.utcnow().isoformat()
    log_lines.append(f"[{ts}] {msg}")
    print(msg)

try:
    cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE lower(description) LIKE '%carca%C3%A7a%' OR lower(description) LIKE '%carcaca%'")
    rows = cur.fetchall()
    L(f'Found {len(rows)} rows with CARCAÇA in description')

    to_update = []
    for id_, pn, desc in rows:
        if not desc:
            continue
        new_desc = pattern.sub('', desc)
        new_desc = re.sub(r"[\-\s]{2,}", ' ', new_desc).strip(' -–—:,.')
        if new_desc != desc.strip():
            to_update.append((new_desc, id_))

    if to_update:
        cur.executemany('UPDATE components_and_parts SET description = ? WHERE id = ?', to_update)
        conn.commit()
        L(f'Updated {len(to_update)} descriptions (removed "usinagem")')
    else:
        L('No descriptions needed change')

    cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE lower(description) LIKE '%carca%C3%A7a%' OR lower(description) LIKE '%carcaca%' ORDER BY id DESC LIMIT 10")
    for r in cur.fetchall():
        L(str(r))

except Exception as e:
    conn.rollback()
    L('ERROR: ' + str(e))
finally:
    conn.close()
    with open(LOG, 'a', encoding='utf-8') as f:
        for l in log_lines:
            f.write(l + '\n')
    L('Log appended to ' + LOG)
