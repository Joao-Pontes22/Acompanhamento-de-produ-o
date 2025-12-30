import sqlite3
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'remove_part_suffixes_PART.log')

log = []
def L(msg):
    ts = datetime.utcnow().isoformat()
    line = f'[{ts}] {msg}'
    log.append(line)
    print(line)

def normalize_base(pn: str) -> str:
    # remove -BR- or -US- and following
    if pn is None:
        return pn
    m = re.split(r'(-BR-|-US-)', pn, flags=re.IGNORECASE)
    if len(m) >= 1:
        return m[0]
    return pn

if not os.path.exists(DB_PATH):
    print('DB not found:', DB_PATH)
    raise SystemExit(1)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute('PRAGMA foreign_keys = ON')
try:
    # detect tables with part_number column
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    tables_with_pn = []
    for t in tables:
        if t == 'components_and_parts':
            continue
        cur.execute(f"PRAGMA table_info('{t}')")
        cols = [c[1] for c in cur.fetchall()]
        if 'part_number' in cols:
            tables_with_pn.append(t)

    L(f'Tables with part_number to update: {tables_with_pn}')

    # select rows to process
    cur.execute("SELECT id, part_number, description, category, client_ID, supplier_ID, cost FROM components_and_parts WHERE upper(part_number) LIKE 'PART-%-BR-%' OR upper(part_number) LIKE 'PART-%-US-%'")
    rows = cur.fetchall()
    L(f'Found {len(rows)} PART- rows with -BR-/-US- suffixes')

    created = 0
    updated = 0

    # gather existing part_numbers
    cur.execute('SELECT part_number FROM components_and_parts')
    existing = {r[0] for r in cur.fetchall() if r[0]}

    for id_, pn, desc, category, client_ID, supplier_ID, cost in rows:
        base = normalize_base(pn)
        desired = base
        # ensure uniqueness
        if desired in existing:
            # if it's the same row (shouldn't be), skip; otherwise add DUP suffix
            cur.execute('SELECT id FROM components_and_parts WHERE part_number = ?', (desired,))
            row = cur.fetchone()
            if row and row[0] == id_:
                L(f'Skipping id={id_} already has desired part_number={desired}')
                continue
            # make unique
            i = 1
            cand = f"{desired}-DUP-{i:03d}"
            while cand in existing:
                i += 1
                cand = f"{desired}-DUP-{i:03d}"
            desired = cand

        # insert new row with desired part_number
        cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                    (desired, desc, category, client_ID, supplier_ID, cost))
        created += 1
        existing.add(desired)
        L(f'Inserted new components_and_parts part_number={desired} (from id={id_})')

        # update referencing tables to point to desired
        for t in tables_with_pn:
            cur.execute(f"UPDATE {t} SET part_number = ? WHERE part_number = ?", (desired, pn))
            if cur.rowcount:
                L(f'Updated {cur.rowcount} rows in {t} from {pn} to {desired}')

        # delete old row
        cur.execute('DELETE FROM components_and_parts WHERE id = ?', (id_,))
        updated += 1
        L(f'Deleted old components_and_parts id={id_} pn={pn}')

    conn.commit()
    L(f'COMMIT. Inserted {created} new rows, deleted {updated} old rows')

except Exception as e:
    conn.rollback()
    L('ERROR: ' + str(e))
finally:
    conn.close()
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        for l in log:
            f.write(l + '\n')
    L('Log appended to ' + LOG_PATH)
