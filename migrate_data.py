import sqlite3

OLD_DB = "db_backup.db"
NEW_DB = "db.db"

# Mapeamento de nomes de tabelas: OLD -> NEW
TABLE_NAME_MAP = {
    "components_and_parts": "ComponentsAndParts",
    "Assembly_Production": "AssemblyProduction",
    "Machining_Production": "MachiningProduction",
}

old_conn = sqlite3.connect(OLD_DB)
new_conn = sqlite3.connect(NEW_DB)

old_cur = old_conn.cursor()
new_cur = new_conn.cursor()

# Buscar tabelas do banco antigo (ignora sqlite internas e alembic)
tables = old_cur.execute("""
    SELECT name FROM sqlite_master
    WHERE type='table'
      AND name NOT LIKE 'sqlite_%'
      AND name != 'alembic_version'
""").fetchall()

for (old_table,) in tables:
    new_table = TABLE_NAME_MAP.get(old_table, old_table)

    print(f"\n🔄 Migrando dados da tabela: {old_table} → {new_table}")

    # Colunas do banco antigo
    old_cols = [
        col[1]
        for col in old_cur.execute(f"PRAGMA table_info({old_table})").fetchall()
    ]

    # Verifica se tabela existe no banco novo
    new_table_exists = new_cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (new_table,)
    ).fetchone()

    if not new_table_exists:
        print(f"⚠️  Tabela {new_table} não existe no banco novo, pulando.")
        continue

    # Colunas do banco novo
    new_cols = [
        col[1]
        for col in new_cur.execute(f"PRAGMA table_info({new_table})").fetchall()
    ]

    # Colunas compatíveis
    common_cols = [c for c in old_cols if c in new_cols]

    if not common_cols:
        print(f"⚠️  Nenhuma coluna compatível entre {old_table} e {new_table}, pulando.")
        continue

    cols_sql = ", ".join(common_cols)
    placeholders = ", ".join(["?"] * len(common_cols))

    # Buscar dados do banco antigo
    rows = old_cur.execute(
        f"SELECT {cols_sql} FROM {old_table}"
    ).fetchall()

    if not rows:
        print("ℹ️  Nenhum dado para migrar.")
        continue

    try:
        new_cur.executemany(
            f"""
            INSERT OR IGNORE INTO {new_table} ({cols_sql})
            VALUES ({placeholders})
            """,
            rows
        )
        print(f"✅ {len(rows)} registros processados.")
    except Exception as e:
        print(f"❌ Erro ao migrar {old_table} → {new_table}: {e}")

new_conn.commit()
old_conn.close()
new_conn.close()

print("\n🎉 Migração concluída com sucesso (dados apenas, duplicatas ignoradas).")
