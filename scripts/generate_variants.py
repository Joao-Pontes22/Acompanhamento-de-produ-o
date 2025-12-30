import sqlite3
import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')

BRUTO_COUNT = 10
USINADO_COUNT = 20

strip_re = re.compile(r"(-BR-\d+|-US-\d+|-BR-\d{2})$", re.IGNORECASE)

def normalize_base(part_number: str) -> str:
    if not part_number:
        return 'PN'
    return strip_re.sub('', part_number)

special_keywords = ['braço', 'bra%C3%A7o', 'pitman', 'braço de controle', 'braco']

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute('PRAGMA foreign_keys = ON')

cur.execute("SELECT id, part_number, description, category, client_ID, supplier_ID, cost FROM components_and_parts")
rows = cur.fetchall()

existing = set()
cur.execute('SELECT part_number FROM components_and_parts')
for (pn,) in cur.fetchall():
    if pn:
        existing.add(pn)

created = 0
updated = 0
skipped = 0

try:
    for row in rows:
        id_, part_number, description, category, client_ID, supplier_ID, cost = row
        base = normalize_base(part_number or 'PN' + str(id_))
        desc = (description or '').strip()
        lower_desc = desc.lower() if desc else ''
        is_special = any(k in lower_desc for k in ['braço', 'braco', 'pitman', 'braço de controle'])

        if is_special:
            # For special case: only Usinado variants; set original to first Usinado
            new_orig_pn = f"{base}-US-001"
            # ensure uniqueness
            i = 1
            while new_orig_pn in existing:
                i += 1
                new_orig_pn = f"{base}-US-{i:03d}"
            existing.add(new_orig_pn)
            cur.execute('UPDATE components_and_parts SET part_number = ?, description = ? WHERE id = ?',
                        (new_orig_pn, 'Braço pitman Usinado', id_))
            updated += 1

            # create remaining usinado variants until count
            for n in range(2, USINADO_COUNT+1):
                pn = f"{base}-US-{n:03d}"
                if pn in existing:
                    continue
                cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                            (pn, 'Braço pitman Usinado', category, client_ID, supplier_ID, cost))
                existing.add(pn)
                created += 1
        else:
            # Update original to first Bruto
            new_orig_pn = f"{base}-BR-01"
            i = 1
            while new_orig_pn in existing:
                i += 1
                new_orig_pn = f"{base}-BR-{i:02d}"
            existing.add(new_orig_pn)
            cur.execute('UPDATE components_and_parts SET part_number = ?, description = ? WHERE id = ?',
                        (new_orig_pn, (desc + ' Bruto').strip(), id_))
            updated += 1

            # create remaining Bruto variants up to BRUTO_COUNT
            start = 2
            n = start
            while n <= BRUTO_COUNT:
                pn = f"{base}-BR-{n:02d}"
                if pn in existing:
                    n += 1
                    continue
                cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                            (pn, (desc + ' Bruto').strip(), category, client_ID, supplier_ID, cost))
                existing.add(pn)
                created += 1
                n += 1

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
    print(f'Updated originals: {updated}, Created variants: {created}, Skipped: {skipped}')

    # quick validation counts
    cur.execute("SELECT COUNT(*) FROM components_and_parts")
    total = cur.fetchone()[0]
    print('Total components_and_parts rows:', total)

except Exception as e:
    conn.rollback()
    print('Error:', e)
finally:
    conn.close()
