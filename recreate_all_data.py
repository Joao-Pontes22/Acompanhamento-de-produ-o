import requests

BASE_URL = "http://localhost:8000"

# 1. Criar fornecedores
suppliers_data = [
    {"name": "FAGOR", "contact": "FAGOR", "email": "fagor@gmail.com", "phone": "XXXXXXX"},
    {"name": "FUNDIMIG", "contact": "FUNDIMIG", "email": "fundimig@gmail.com", "phone": "XXXXXXX"},
    {"name": "TUPY", "contact": "TUPY", "email": "tupy@gmail.com", "phone": "XXXXXXX"},
    {"name": "LEPE", "contact": "LEPE", "email": "lepe@gmail.com", "phone": "XXXXXXX"},
    {"name": "CIE FORJAS", "contact": "CIE FORJAS", "email": "cieforjas@gmail.com", "phone": "XXXXXXX"},
    {"name": "SATA", "contact": "SATA", "email": "sata@gmail.com", "phone": "XXXXXXX"},
    {"name": "VALBORMIDA", "contact": "VALBORMIDA", "email": "valbormida@gmail.com", "phone": "XXXXXXX"},
    {"name": "IPERFOR", "contact": "IPERFOR", "email": "iperfor@gmail.com", "phone": "XXXXXXX"},
    {"name": "SAMOT", "contact": "SAMOT", "email": "samot@gmail.com", "phone": "XXXXXXX"},
    {"name": "DANA", "contact": "DANA", "email": "dana@gmail.com", "phone": "XXXXXXX"}
]

print("=== RECRIANDO DADOS DO BANCO ===\n")
print("1. Criando fornecedores...")

for supplier in suppliers_data:
    payload = {
        "supplier_name": supplier["name"],
        "contact_name": supplier["contact"],
        "contact_email": supplier["email"],
        "contact_phone": supplier["phone"]
    }
    try:
        response = requests.post(f"{BASE_URL}/supplier/add_supplier", json=payload)
        if response.status_code == 200:
            print(f"   ✓ {supplier['name']}")
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")

# 2. Criar componentes
print("\n2. Criando componentes...")

components_data = [
    {"part": "CAR-001", "desc": "Carcaça", "suppliers": [1, 2], "cost": 150.50},
    {"part": "TAM-002", "desc": "Tampa da direção", "suppliers": [3, 4, 2], "cost": 85.75},
    {"part": "EIX-003", "desc": "Eixo Setor", "suppliers": [5], "cost": 220.00},
    {"part": "VAL-004", "desc": "Válvula rotativa", "suppliers": [6], "cost": 95.30},
    {"part": "PIS-005", "desc": "Pistão", "suppliers": [7, 8], "cost": 175.80},
    {"part": "BRA-006", "desc": "braço", "suppliers": [9, 10], "cost": 125.40}
]

for comp in components_data:
    for supplier_id in comp["suppliers"]:
        payload = {
            "part_number": comp["part"],
            "description_material": comp["desc"],
            "supplier_ID": supplier_id,
            "cost": comp["cost"]
        }
        try:
            response = requests.post(f"{BASE_URL}/data/add_component", json=payload)
            if response.status_code == 200:
                print(f"   ✓ {comp['desc']} (Fornecedor ID: {supplier_id})")
        except Exception as e:
            print(f"   ✗ Erro: {str(e)}")

# 3. Criar clientes
print("\n3. Criando clientes...")

clients_data = [
    {"name": "MERCEDES-BENZ", "contact": "Departamento de Suprimentos", "email": "suprimentos@mercedes-benz.com.br", "phone": "(11) 3555-0000"},
    {"name": "VOLVO", "contact": "Gerência de Compras", "email": "compras@volvo.com.br", "phone": "(11) 4141-1000"},
    {"name": "SCANIA", "contact": "Setor de Aquisições", "email": "aquisicoes@scania.com.br", "phone": "(19) 3821-1000"},
    {"name": "MAN", "contact": "Departamento de Procurement", "email": "procurement@man.com.br", "phone": "(21) 2534-0000"},
    {"name": "IVECO", "contact": "Coordenação de Fornecedores", "email": "fornecedores@iveco.com.br", "phone": "(31) 3899-0000"}
]

for client in clients_data:
    payload = {
        "name": client["name"],
        "contact": client["contact"],
        "email": client["email"],
        "phone": client["phone"]
    }
    try:
        response = requests.post(f"{BASE_URL}/data/add_client", json=payload)
        if response.status_code == 200:
            print(f"   ✓ {client['name']}")
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")

# 4. Criar parts
print("\n4. Criando parts (Caixa de direção)...")

parts_data = [
    {"part": "DIR-MB-001", "client_id": 1, "cost": 850.00},
    {"part": "DIR-VV-002", "client_id": 2, "cost": 920.50},
    {"part": "DIR-SC-003", "client_id": 3, "cost": 895.75},
    {"part": "DIR-MN-004", "client_id": 4, "cost": 880.00},
    {"part": "DIR-IV-005", "client_id": 5, "cost": 910.25}
]

for part in parts_data:
    payload = {
        "part_number": part["part"],
        "description_parts": "Caixa de direção",
        "clients_ID": part["client_id"],
        "cost": part["cost"]
    }
    try:
        response = requests.post(f"{BASE_URL}/data/add_parts", json=payload)
        if response.status_code == 200:
            print(f"   ✓ {part['part']}")
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")

# 5. Criar máquinas
print("\n5. Criando máquinas...")

machines_data = [
    {"name": "Torno CNC #01", "sector": 4, "desc": "Torno CNC para usinagem de carcaça"},
    {"name": "Torno CNC #02", "sector": 4, "desc": "Torno CNC para usinagem de carcaça"},
    {"name": "Centro de Usinagem #01", "sector": 4, "desc": "Centro de usinagem com 5 eixos"},
    {"name": "Torno CNC #03", "sector": 5, "desc": "Torno CNC para usinagem de eixo"},
    {"name": "Broxa #01", "sector": 5, "desc": "Máquina de broxagem para eixo"},
    {"name": "Centro de Usinagem #02", "sector": 5, "desc": "Centro de usinagem 4 eixos"},
    {"name": "Torno CNC #04", "sector": 6, "desc": "Torno CNC para usinagem de pistão"},
    {"name": "Centro de Usinagem #03", "sector": 6, "desc": "Centro de usinagem para pistão"},
    {"name": "Máquina de Teste de Estanqueidade #01", "sector": 6, "desc": "Teste de estanqueidade"},
    {"name": "Torno CNC #05", "sector": 7, "desc": "Torno CNC para usinagem de sem-fim"},
    {"name": "Centro de Usinagem #04", "sector": 7, "desc": "Centro de usinagem sem-fim"},
    {"name": "Torno CNC #06", "sector": 8, "desc": "Torno CNC para usinagem de válvula"},
    {"name": "Broxa #02", "sector": 8, "desc": "Máquina de broxagem para válvula"},
    {"name": "Máquina de Teste de Vazão #01", "sector": 8, "desc": "Teste de vazão"},
    {"name": "Máquina de Teste de Estanqueidade #02", "sector": 8, "desc": "Teste de estanqueidade"},
    {"name": "Máquina de Teste de Vazão #02", "sector": 9, "desc": "Teste de vazão final"},
    {"name": "Máquina de Teste de Estanqueidade #03", "sector": 9, "desc": "Teste de estanqueidade final"}
]

for machine in machines_data:
    payload = {
        "machine": machine["name"],
        "sector_ID": machine["sector"],
        "description_machine": machine["desc"]
    }
    try:
        response = requests.post(f"{BASE_URL}/Machine/POST_machine", json=payload)
        if response.status_code == 200:
            print(f"   ✓ {machine['name']}")
    except Exception as e:
        print(f"   ✗ Erro: {str(e)}")

print("\n✓ Recriação de dados concluída!")
