import sqlite3
import os
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
SQL_PATH = os.path.join(os.path.dirname(__file__), 'generate_variants.sql')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'generate_variants_applied.log')

if not os.path.exists(DB_PATH):
    print('ERROR: db.db not found at', DB_PATH)
    sys.exit(1)
if not os.path.exists(SQL_PATH):
    print('ERROR: SQL file not found at', SQL_PATH)
    sys.exit(1)

log = []
log.append(f'[{datetime.utcnow().isoformat()}] Applying variants to: {DB_PATH}')

BRUTO_COUNT = 10
USINADO_COUNT = 20

def normalize_base(pn, idx):
    if not pn:
        return f'PN{idx:04d}'
    # strip previous suffixes
    import re
    return re.sub(r'(-BR-\d+|-US-\d+|-US-\d{3})$', '', pn, flags=re.IGNORECASE)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
try:
    cur.execute('PRAGMA foreign_keys = ON')
    cur.execute('SELECT id, part_number, description, category, client_ID, supplier_ID, cost FROM components_and_parts')
    rows = cur.fetchall()
    log.append(f'Found {len(rows)} components')

    cur.execute('SELECT part_number FROM components_and_parts')
    existing = {r[0] for r in cur.fetchall() if r[0]}

    # find tables that have a part_number column (excluding components_and_parts)
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    tables_with_pn = []
    for t in tables:
        if t == 'components_and_parts':
            continue
        try:
            cur.execute(f"PRAGMA table_info('{t}')")
            cols = [c[1] for c in cur.fetchall()]
            if 'part_number' in cols:
                tables_with_pn.append(t)
        except Exception:
            continue

    created = 0
    updated = 0

    for idx, row in enumerate(rows, start=1):
        id_, part_number, description, category, client_ID, supplier_ID, cost = row
        base = normalize_base(part_number or '', idx)
        desc = (description or '').strip()
        lower = desc.lower()
        is_special = 'braço' in lower or 'braco' in lower or 'pitman' in lower

        if is_special:
            # set original to first Usinado
            new_orig = f"{base}-US-001"
            i = 1
            while new_orig in existing:
                i += 1
                new_orig = f"{base}-US-{i:03d}"
            # insert new row with new_orig
            cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                        (new_orig, 'Braço pitman Usinado', category, client_ID, supplier_ID, cost))
            created += 1
            existing.add(new_orig)
            log.append(f'Inserted new original for id={id_} -> {new_orig}')
            # update referencing tables to point to new_orig
            for t in tables_with_pn:
                cur.execute(f"UPDATE {t} SET part_number = ? WHERE part_number = ?", (new_orig, part_number))
                if cur.rowcount:
                    log.append(f'Updated {cur.rowcount} rows in {t} from {part_number} to {new_orig}')
            # delete old row
            cur.execute('DELETE FROM components_and_parts WHERE id = ?', (id_,))
            updated += 1
            # create remaining usinado variants
            for n in range(2, USINADO_COUNT+1):
                pn = f"{base}-US-{n:03d}"
                if pn in existing:
                    continue
                cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                            (pn, 'Braço pitman Usinado', category, client_ID, supplier_ID, cost))
                existing.add(pn)
                created += 1

        else:
            # insert new original as BR-01
            new_orig = f"{base}-BR-01"
            j = 1
            while new_orig in existing:
                j += 1
                new_orig = f"{base}-BR-{j:02d}"
            cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                        (new_orig, (desc + ' Bruto').strip(), category, client_ID, supplier_ID, cost))
            created += 1
            existing.add(new_orig)
            log.append(f'Inserted new original for id={id_} -> {new_orig}')
            # update referencing tables to point to new_orig
            for t in tables_with_pn:
                cur.execute(f"UPDATE {t} SET part_number = ? WHERE part_number = ?", (new_orig, part_number))
                if cur.rowcount:
                    log.append(f'Updated {cur.rowcount} rows in {t} from {part_number} to {new_orig}')
            # delete old row
            cur.execute('DELETE FROM components_and_parts WHERE id = ?', (id_,))
            updated += 1

            # create remaining Bruto variants
            for n in range(2, BRUTO_COUNT+1):
                pn = f"{base}-BR-{n:02d}"
                if pn in existing:
                    continue
                cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                            (pn, (desc + ' Bruto').strip(), category, client_ID, supplier_ID, cost))
                existing.add(pn)
                created += 1

            # create Usinado variants
            for m in range(1, USINADO_COUNT+1):
                pn = f"{base}-US-{m:03d}"
                if pn in existing:
                    continue
                cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                            (pn, (desc + ' Usinado').strip(), category, client_ID, supplier_ID, cost))
                existing.add(pn)
                created += 1

    conn.commit()
    log.append(f'COMMIT. Updated originals: {updated}, Created variants: {created}')

    cur.execute('SELECT COUNT(*) FROM components_and_parts')
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM components_and_parts WHERE part_number LIKE '%-BR-%'")
    br = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM components_and_parts WHERE part_number LIKE '%-US-%'")
    us = cur.fetchone()[0]

    print('TOTAL', total)
    print('BR', br)
    print('US', us)

    cur.execute("SELECT id, part_number, description FROM components_and_parts ORDER BY id DESC LIMIT 10")
    for r in cur.fetchall():
        print(r)

except Exception as e:
    conn.rollback()
    log.append('ERROR: ' + str(e))
    print('ERROR:', e)
finally:
    conn.close()
    with open(LOG_PATH, 'a', encoding='utf-8') as lf:
        for l in log:
            lf.write(l + '\n')
    print('Log appended to', LOG_PATH)
