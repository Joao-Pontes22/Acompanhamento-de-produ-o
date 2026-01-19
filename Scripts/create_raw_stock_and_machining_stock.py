import requests
BASE_URL = "http://127.0.0.1:8000"
CREATE_PART_NUMBER = "0150.559.638"

# 🔐 LOGIN
login_payload = {
    "emp_id": "9290",
    "password": "123"
}

login = requests.post(
    f"{BASE_URL}/Login/Login",
    json=login_payload,
    timeout=10
)

login.raise_for_status()
token = login.json()["access_token"]

headers = {
    "Authorization": f"Bearer {token}"
}

# 🔗 BUSCA RELAÇÕES
relations_resp = requests.get(
    f"{BASE_URL}/relations/relations_filtred",
    params={"create_item_part_number": CREATE_PART_NUMBER},
    headers=headers,
    timeout=10
)

relations_resp.raise_for_status()
relations = relations_resp.json()

print(f"{len(relations)} relações encontradas")

# 🔁 LOOP COMPONENTES
for rel in relations:
    consume_pn = rel["consume_item_Part_number"]

    relations_machi = requests.get(
        f"{BASE_URL}/relations/relations_filtred",
        params={"create_item_part_number": consume_pn},
        headers=headers,
        timeout=10
    )

    relation_raw = relations_machi.json()

    if not relation_raw:
        continue

    raw_pn = relation_raw[0]["consume_item_Part_number"]

    payload_raw = {
        "sector": "montagem 1",
        "part_number": raw_pn,
        "qnty": 10,
        "reason": "Ordem de produção #100"
    }

    resp = requests.post(
        f"{BASE_URL}/stock/Create_Stock",
        json=payload_raw,
        headers=headers,
        timeout=10
    )

    if resp.ok:
        print(f"✅ Stock criado para {raw_pn}")
    else:
        print(f"❌ Erro {raw_pn}: {resp.status_code} - {resp.text}")

# 🔁 STOCK FINAL
for rel in relations:
    part_number = rel["consume_item_Part_number"]

    payload = {
        "sector": "montagem 1",
        "part_number": part_number,
        "qnty": 10,
        "reason": "Ordem de produção #100"
    }

    resp = requests.post(
        f"{BASE_URL}/stock/Create_Stock",
        json=payload,
        headers=headers,
        timeout=10
    )

    if resp.ok:
        print(f"✅ Stock criado para {part_number}")
    else:
        print(f"❌ Erro {part_number}: {resp.status_code} - {resp.text}")
