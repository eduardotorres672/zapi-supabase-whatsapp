# 📲 whatsapp-notifier

Busca contatos no Supabase e envia mensagem personalizada via WhatsApp usando a Z-API.

---

## 🗄️ Tabela no Supabase

```sql
CREATE TABLE contacts (
    id      BIGSERIAL PRIMARY KEY,
    name    TEXT    NOT NULL,
    phone   TEXT    NOT NULL,
    active  BOOLEAN NOT NULL DEFAULT TRUE
);

INSERT INTO contacts (name, phone) VALUES
    ('Eduardo', '5511999999991'),
    ('Victoria', '5511999999992'),
    ('Carlos',   '5511999999993');
```

> Telefone só com número, sem `+` ou espaço. Ex: `5511912345678`

---

## ⚙️ Variáveis de ambiente

```env
SUPABASE_URL=
SUPABASE_KEY=
ZAPI_INSTANCE_ID=
ZAPI_TOKEN=
ZAPI_CLIENT_TOKEN=
```

---

## ▶️ Como rodar

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

---

## 🧰 Stack

`Python` · `Supabase` · `Z-API`
