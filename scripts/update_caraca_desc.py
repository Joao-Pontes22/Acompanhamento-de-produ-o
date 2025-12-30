import sqlite3
import os
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG = os.path.join(os.path.dirname(__file__), 'update_caraca_desc.log')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
log_lines = []

def L(msg):
    ts = datetime.utcnow().isoformat()
    log_lines.append(f"[{ts}] {msg}")
    print(msg)

try:
    # Update CARCAÇA - USINAGEM Bruto -> CARCAÇA - Bruto
    cur.execute("UPDATE components_and_parts SET description = 'CARCAÇA - Bruto' WHERE description = 'CARCAÇA - USINAGEM Bruto'")
    count1 = cur.rowcount
    L(f'Updated {count1} rows: "CARCAÇA - USINAGEM Bruto" -> "CARCAÇA - Bruto"')

    # Update CARCAÇA - USINAGEM Usinado -> CARCAÇA - Usinado
    cur.execute("UPDATE components_and_parts SET description = 'CARCAÇA - Usinado' WHERE description = 'CARCAÇA - USINAGEM Usinado'")
    count2 = cur.rowcount
    L(f'Updated {count2} rows: "CARCAÇA - USINAGEM Usinado" -> "CARCAÇA - Usinado"')

    conn.commit()
    L(f'COMMIT complete. Total updated: {count1 + count2}')

    # Show sample
    cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE description LIKE 'CARCAÇA%' ORDER BY id DESC LIMIT 10")
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
