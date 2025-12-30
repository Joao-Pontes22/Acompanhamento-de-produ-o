"""
Script para remover hífens e palavras bruto/usinado de peças da categoria PART
"""

import os
import sys
from pathlib import Path
import re

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.Models import ComponentsAndParts

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def clean_description(desc):
    """Remove hífens e palavras bruto/usinado da descrição"""
    if not desc:
        return desc
    
    # Remove a palavra "bruto" ou "usinado" (case-insensitive)
    cleaned = re.sub(r'\s*-\s*(bruto|usinado)\s*', '', desc, flags=re.IGNORECASE)
    # Remove hífens extras
    cleaned = re.sub(r'\s*-\s*', ' ', cleaned)
    # Remove espaços extras
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned.strip()

def clean_part_descriptions():
    """Remove hífens e palavras bruto/usinado de peças PART"""
    with Session(engine) as session:
        # Busca todas as peças com part_number contendo "PART-"
        parts = session.query(ComponentsAndParts).filter(
            ComponentsAndParts.part_number.like('PART-%')
        ).all()
        
        if not parts:
            print("❌ Nenhuma peça PART encontrada")
            return
        
        print(f"📊 Total de peças PART encontradas: {len(parts)}")
        print("\n🔄 Limpando descrições...\n")
        
        updated_count = 0
        for part in parts:
            old_desc = part.description
            new_desc = clean_description(part.description)
            
            if old_desc != new_desc:
                part.description = new_desc
                updated_count += 1
                print(f"✅ {part.part_number}")
                print(f"   Antes: {old_desc}")
                print(f"   Depois: {new_desc}\n")
        
        session.commit()
        print(f"\n✨ Total de peças atualizadas: {updated_count}/{len(parts)}")

if __name__ == "__main__":
    clean_part_descriptions()
