"""
Script para criar relações entre componentes brutos e usinados
Para cada componente bruto, vincula 2 componentes usinados diferentes
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.Models import ComponentsAndParts, RelationMachinedxRaw

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_component_relations():
    """
    Cria relações entre componentes brutos e usinados.
    Para cada componente bruto, vincula 2 componentes usinados diferentes.
    """
    with Session(engine) as session:
        # Busca componentes brutos e usinados pela descrição
        all_components = session.query(ComponentsAndParts).all()
        
        raw_components = [c for c in all_components if c.description and "bruto" in c.description.lower()]
        machined_components = [c for c in all_components if c.description and "usinado" in c.description.lower()]
        
        print(f"📊 Total de componentes encontrados: {len(all_components)}")
        print(f"🟡 Componentes Brutos: {len(raw_components)}")
        print(f"🔵 Componentes Usinados: {len(machined_components)}\n")
        
        if not raw_components or not machined_components:
            print("❌ Não há componentes brutos ou usinados suficientes")
            return
        
        # Cria relações: cada bruto -> 2 usinados
        relations_created = 0
        machined_idx = 0
        
        print("🔄 Criando relações...\n")
        
        for raw in raw_components:
            # Pega 2 componentes usinados diferentes (com rolagem)
            machined_1 = machined_components[machined_idx % len(machined_components)]
            machined_2 = machined_components[(machined_idx + 1) % len(machined_components)]
            
            # Evita relacionar o mesmo componente com ele mesmo
            if machined_1.id == raw.id:
                machined_1 = machined_components[(machined_idx + 1) % len(machined_components)]
            if machined_2.id == raw.id or machined_2.id == machined_1.id:
                machined_2 = machined_components[(machined_idx + 2) % len(machined_components)]
            
            # Verifica se já existe relação com este raw
            existing_relations = session.query(RelationMachinedxRaw).filter(
                RelationMachinedxRaw.raw_ID == raw.id
            ).first()
            
            if not existing_relations:
                # Cria primeira relação
                rel1 = RelationMachinedxRaw(
                    raw_ID=raw.id,
                    machined_ID=machined_1.id
                )
                session.add(rel1)
                relations_created += 1
                print(f"✅ {raw.part_number} (Bruto)")
                print(f"   └─ → {machined_1.part_number} (Usinado)")
                
                # Cria segunda relação com relação 1-para-muitos
                # Aqui criamos um novo registro de relação com o mesmo raw mas machined diferente
                rel2 = RelationMachinedxRaw(
                    raw_ID=raw.id,
                    machined_ID=machined_2.id
                )
                session.add(rel2)
                relations_created += 1
                print(f"   └─ → {machined_2.part_number} (Usinado)\n")
            
            machined_idx += 2
        
        session.commit()
        print(f"✨ Total de relações criadas: {relations_created}")
        
        # Exibe resumo das relações
        all_relations = session.query(RelationMachinedxRaw).all()
        print(f"\n📌 Total de relações no banco: {len(all_relations)}")
        
        # Agrupa por componente bruto
        relations_by_raw = {}
        for rel in all_relations:
            if rel.raw_ID not in relations_by_raw:
                relations_by_raw[rel.raw_ID] = []
            relations_by_raw[rel.raw_ID].append(rel)
        
        print(f"\n🔗 Relações por componente bruto:")
        for raw_id, rels in list(relations_by_raw.items())[:10]:  # Mostra apenas os 10 primeiros
            raw_comp = session.query(ComponentsAndParts).filter_by(id=raw_id).first()
            print(f"\n{raw_comp.part_number}:")
            for rel in rels:
                machined = session.query(ComponentsAndParts).filter_by(id=rel.machined_ID).first()
                print(f"  └─ {machined.part_number}")
        
        if len(relations_by_raw) > 10:
            print(f"\n... e mais {len(relations_by_raw) - 10} componentes brutos")

if __name__ == "__main__":
    create_component_relations()
