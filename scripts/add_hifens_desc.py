import sqlite3
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG = os.path.join(os.path.dirname(__file__), 'add_hifens.log')

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
log_lines = []

def L(msg):
    ts = datetime.utcnow().isoformat()
    log_lines.append(f"[{ts}] {msg}")
    print(msg)

try:
    cur.execute('SELECT id, description FROM components_and_parts WHERE description IS NOT NULL')
    rows = cur.fetchall()
    L(f'Processing {len(rows)} descriptions')

    to_update = []
    for id_, desc in rows:
        if not desc:
            continue
        
        # Pattern: text followed by Bruto/Usinado without hyphen before it
        # e.g., "CARCAÇA Bruto" -> "CARCAÇA - Bruto"
        # e.g., "PISTÃO Usinado" -> "PISTÃO - Usinado"
        new_desc = re.sub(r'([A-ZÁÉÍÓÚ][A-Za-záéíóúç\s]*?)\s+(Bruto|Usinado|Braço)', r'\1 - \2', desc)
        
        # Clean up multiple spaces or hyphens
        new_desc = re.sub(r'\s+(-)\s+', r' \1 ', new_desc)
        new_desc = re.sub(r'\s+', ' ', new_desc).strip()
        
        if new_desc != desc:
            to_update.append((new_desc, id_))
            L(f'id={id_}: "{desc}" -> "{new_desc}"')

    if to_update:
        cur.executemany('UPDATE components_and_parts SET description = ? WHERE id = ?', to_update)
        conn.commit()
        L(f'Updated {len(to_update)} descriptions (added hífens)')
    else:
        L('No descriptions needed hyphen adjustment')

    # Show sample of updated descriptions
    cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE description LIKE '%Bruto' OR description LIKE '%Usinado' ORDER BY id DESC LIMIT 15")
    L('Sample of updated descriptions:')
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
