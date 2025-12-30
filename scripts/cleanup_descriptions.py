import sqlite3
import os
import re
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(ROOT, 'db.db')
LOG_PATH = os.path.join(os.path.dirname(__file__), 'cleanup_descriptions.log')

pattern = re.compile(r"\b(bruto|fundição|fundicao|acabamento|premium)\b", re.IGNORECASE)

log_lines = []
def log(msg):
    ts = datetime.utcnow().isoformat()
    line = f"[{ts}] {msg}"
    log_lines.append(line)
    print(line)

def main():
    if not os.path.exists(DB_PATH):
        log(f"ERROR: DB not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON')

    try:
        cur.execute('SELECT COUNT(*) FROM components_and_parts')
        total_before = cur.fetchone()[0]
        log(f'Total before: {total_before}')

        # Delete rows containing 'teste' or 'test' in part_number or description
        cur.execute("SELECT id FROM components_and_parts WHERE lower(part_number) LIKE '%teste%' OR lower(description) LIKE '%teste%' OR lower(part_number) LIKE '%test%' OR lower(description) LIKE '%test%'")
        ids = [r[0] for r in cur.fetchall()]
        del_count = 0
        if ids:
            cur.executemany('DELETE FROM components_and_parts WHERE id = ?', [(i,) for i in ids])
            del_count = len(ids)
            log(f'Deleted {del_count} rows matching TEST/TESTE')
        else:
            log('No TEST rows found to delete')

        # Clean descriptions: remove suffix words
        cur.execute("SELECT id, description FROM components_and_parts WHERE description IS NOT NULL")
        updates = []
        for id_, desc in cur.fetchall():
            if not desc:
                continue
            new_desc = pattern.sub('', desc)
            new_desc = re.sub(r'\s+', ' ', new_desc).strip(' -–—:,.')
            if new_desc != desc.strip():
                updates.append((new_desc, id_))

        if updates:
            cur.executemany('UPDATE components_and_parts SET description = ? WHERE id = ?', updates)
            log(f'Updated {len(updates)} descriptions (removed sufixes)')
        else:
            log('No descriptions required cleaning')

        conn.commit()

        cur.execute('SELECT COUNT(*) FROM components_and_parts')
        total_after = cur.fetchone()[0]
        log(f'Total after: {total_after}')

        # show a small sample of modified rows
        cur.execute("SELECT id, part_number, description FROM components_and_parts WHERE description IS NOT NULL ORDER BY id DESC LIMIT 10")
        rows = cur.fetchall()
        log('Sample rows:')
        for r in rows:
            log(str(r))

    except Exception as e:
        conn.rollback()
        log(f'ERROR: {e}')
    finally:
        conn.close()
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            for l in log_lines:
                f.write(l + '\n')
        log(f'Log appended to {LOG_PATH}')

if __name__ == '__main__':
    main()
