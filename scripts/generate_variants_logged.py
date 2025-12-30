import sqlite3
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'generate_variants.log')

BRUTO_COUNT = 10
USINADO_COUNT = 20

strip_re = re.compile(r"(-BR-\d+|-US-\d{3}|-US-\d+)$", re.IGNORECASE)

def normalize_base(part_number: str, idx: int) -> str:
    if not part_number:
        return f'PN{idx:04d}'
    return strip_re.sub('', part_number)

special_terms = ['braço', 'braco', 'pitman', 'braço de controle', 'bra%C3%A7o']

log_lines = []

def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    log_lines.append(line)
    print(line)

if __name__ == '__main__':
    log(f"Script start. DB={DB_PATH}")
    if not os.path.exists(DB_PATH):
        log('ERROR: database file not found.')
        open(LOG_PATH, 'w', encoding='utf-8').write('\n'.join(log_lines))
        raise SystemExit(1)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

    try:
        cur.execute('SELECT id, part_number, description, category, client_ID, supplier_ID, cost FROM components_and_parts')
        rows = cur.fetchall()
        log(f'Found {len(rows)} components in components_and_parts')

        cur.execute('SELECT part_number FROM components_and_parts')
        existing = {r[0] for r in cur.fetchall() if r[0]}

        created = 0
        updated = 0

        for idx, row in enumerate(rows, start=1):
            id_, part_number, description, category, client_ID, supplier_ID, cost = row
            base = normalize_base(part_number or '', idx)
            desc = (description or '').strip()
            lower = desc.lower()
            is_special = any(term in lower for term in special_terms)

            if is_special:
                # Make original the first USINADO
                new_orig_pn = f"{base}-US-001"
                i = 1
                while new_orig_pn in existing:
                    i += 1
                    new_orig_pn = f"{base}-US-{i:03d}"
                cur.execute('UPDATE components_and_parts SET part_number = ?, description = ? WHERE id = ?',
                            (new_orig_pn, 'Braço pitman Usinado', id_))
                existing.add(new_orig_pn)
                updated += 1
                log(f'Updated id={id_} -> part_number={new_orig_pn} description="Braço pitman Usinado"')

                # create remaining usinado variants
                for n in range(2, USINADO_COUNT+1):
                    pn = f"{base}-US-{n:03d}"
                    if pn in existing:
                        continue
                    cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                                (pn, 'Braço pitman Usinado', category, client_ID, supplier_ID, cost))
                    existing.add(pn)
                    created += 1
                    if created % 50 == 0:
                        log(f'Created {created} variants so far...')
                    log(f'Inserted part_number={pn} (Braço pitman Usinado)')

            else:
                # Update original to BR-01
                new_orig_pn = f"{base}-BR-01"
                j = 1
                while new_orig_pn in existing:
                    j += 1
                    new_orig_pn = f"{base}-BR-{j:02d}"
                cur.execute('UPDATE components_and_parts SET part_number = ?, description = ? WHERE id = ?',
                            (new_orig_pn, (desc + ' Bruto').strip(), id_))
                existing.add(new_orig_pn)
                updated += 1
                log(f'Updated id={id_} -> part_number={new_orig_pn} description="{(desc + " Bruto").strip()}"')

                # create remaining Bruto variants
                for n in range(2, BRUTO_COUNT+1):
                    pn = f"{base}-BR-{n:02d}"
                    if pn in existing:
                        continue
                    cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                                (pn, (desc + ' Bruto').strip(), category, client_ID, supplier_ID, cost))
                    existing.add(pn)
                    created += 1
                    log(f'Inserted part_number={pn} description="{(desc + " Bruto").strip()}"')

                # create Usinado variants
                for m in range(1, USINADO_COUNT+1):
                    pn = f"{base}-US-{m:03d}"
                    if pn in existing:
                        continue
                    cur.execute('INSERT INTO components_and_parts (part_number, description, category, client_ID, supplier_ID, cost) VALUES (?,?,?,?,?,?)',
                                (pn, (desc + ' Usinado').strip(), category, client_ID, supplier_ID, cost))
                    existing.add(pn)
                    created += 1
                    if created % 50 == 0:
                        log(f'Created {created} variants so far...')
                    log(f'Inserted part_number={pn} description="{(desc + " Usinado").strip()}"')

        conn.commit()
        log(f'COMMIT complete. Updated originals: {updated}, Created variants: {created}')

        cur.execute('SELECT COUNT(*) FROM components_and_parts')
        total = cur.fetchone()[0]
        log(f'Total components_and_parts rows after changes: {total}')

    except Exception as e:
        conn.rollback()
        log(f'ERROR, rolled back. Exception: {e}')
    finally:
        conn.close()
        open(LOG_PATH, 'w', encoding='utf-8').write('\n'.join(log_lines))
        log(f'Log written to {LOG_PATH}')
