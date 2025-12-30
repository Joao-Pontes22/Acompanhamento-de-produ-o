#!/usr/bin/env python3
"""
Script para restaurar dados do backup para o banco principal
"""

import sqlite3
import os
import shutil
from pathlib import Path

def restore_backup():
    """Copia todos os dados do backup para o banco principal"""
    
    backup_path = "./db_backup_20251219_144049.db"
    main_db_path = "./db.db"
    
    if not os.path.exists(backup_path):
        print(f"❌ Arquivo de backup não encontrado: {backup_path}")
        return
    
    print(f"📦 Conectando ao backup: {backup_path}")
    print(f"📦 Banco principal: {main_db_path}\n")
    
    try:
        # Conectar aos dois bancos
        backup_conn = sqlite3.connect(backup_path)
        main_conn = sqlite3.connect(main_db_path)
        
        backup_cursor = backup_conn.cursor()
        main_cursor = main_conn.cursor()
        
        # Obter lista de tabelas do backup
        backup_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = backup_cursor.fetchall()
        
        if not tables:
            print("❌ Nenhuma tabela encontrada no backup!")
            return
        
        print(f"📊 {len(tables)} tabelas encontradas no backup:\n")
        
        # Transferir dados de cada tabela
        for (table_name,) in tables:
            try:
                # Contar registros no backup
                backup_cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = backup_cursor.fetchone()[0]
                
                if count == 0:
                    print(f"⏭️  {table_name}: Nenhum registro")
                    continue
                
                # Obter estrutura da tabela
                backup_cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [col[1] for col in backup_cursor.fetchall()]
                
                # Limpar tabela no banco principal
                main_cursor.execute(f"DELETE FROM {table_name}")
                main_conn.commit()
                
                # Copiar dados
                backup_cursor.execute(f"SELECT * FROM {table_name}")
                rows = backup_cursor.fetchall()
                
                columns_str = ", ".join(columns)
                placeholders = ", ".join(["?" for _ in columns])
                insert_sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
                
                main_cursor.executemany(insert_sql, rows)
                main_conn.commit()
                
                print(f"✅ {table_name}: {count} registros copiados")
                
            except Exception as e:
                print(f"❌ Erro em {table_name}: {str(e)}")
        
        backup_conn.close()
        main_conn.close()
        
        print("\n✨ Restauração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {str(e)}")

if __name__ == "__main__":
    restore_backup()
