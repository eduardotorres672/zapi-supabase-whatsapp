# Z-API + Supabase — WhatsApp Message Sender

Script Python que busca contatos ativos no Supabase e dispara mensagens personalizadas via WhatsApp usando a Z-API. Simples de configurar, fácil de adaptar para o seu caso.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Supabase](https://img.shields.io/badge/Supabase-2.10.0-green)
![Z-API](https://img.shields.io/badge/WhatsApp-Z--API-brightgreen)

---

## Como funciona

O script segue um fluxo direto:

1. Conecta ao Supabase e busca todos os contatos com `active = true`
2. Valida o formato do número antes de fazer qualquer chamada à API — telefones fora do padrão são logados e pulados
3. Envia `"Olá, {nome} tudo bem com você?"` via Z-API para cada contato válido
4. Exibe no terminal o resultado de cada envio e um resumo final (enviados / falhas)

---

## Pré-requisitos

- Python 3.9 ou superior
- Conta ativa na [Z-API](https://www.z-api.io/) com uma instância WhatsApp conectada
- Projeto criado no [Supabase](https://supabase.com/)

---

## Configuração do Supabase

Crie a tabela `contacts` no seu projeto:

```sql
CREATE TABLE contacts (
    id      BIGSERIAL PRIMARY KEY,
    name    TEXT    NOT NULL,
    phone   TEXT    NOT NULL,
    active  BOOLEAN NOT NULL DEFAULT TRUE
);
```

Insira seus contatos:

```sql
INSERT INTO contacts (name, phone, active) VALUES
    ('Eduardo',  '5511999999991', true),
    ('Victoria', '5511999999992', true),
    ('Carlos',   '5511999999993', false);  -- ignorado pelo filtro active = true
```

> O campo `phone` aceita apenas dígitos, sem `+`, espaços ou traços (DDI + DDD + número).
> Formato esperado: `5511912345678`

---

## Instalação

```bash
git clone https://github.com/eduardotorres672/zapi-supabase-whatsapp.git
cd zapi-supabase-whatsapp

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp env.example .env
```

Edite o `.env` com suas credenciais:

```env
# Supabase
SUPABASE_URL=https://seusupabase.supabase.co
SUPABASE_KEY=sua_anon_key

# Z-API
ZAPI_INSTANCE_ID=seu_instance_id
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token
```

As credenciais da Z-API estão disponíveis no painel da instância em [app.z-api.io](https://app.z-api.io).

---

## Execução

```bash
python main.py
```

Saída esperada:

```
2025-01-15 10:32:01 [INFO] 2 contato(s) encontrado(s)
2025-01-15 10:32:02 [INFO] mensagem enviada pra Eduardo (5511999999991)
2025-01-15 10:32:03 [INFO] mensagem enviada pra Victoria (5511999999992)
2025-01-15 10:32:03 [INFO] fim — 2 enviado(s), 0 falha(s)
```

---

## Personalizando a mensagem

Edite o texto diretamente em `main.py`, na função `send_whatsapp()`:

```python
payload = {
    "phone": phone,
    "message": f"Olá, {name} tudo bem com você?",
}
```

O `{name}` é substituído automaticamente pelo nome do contato vindo do banco.

---

## Comportamentos do script

| Ponto | Detalhe |
|---|---|
| Limite de contatos | Busca até 3 por execução — ajuste o `.limit(3)` em `get_contacts()` conforme necessário |
| Filtro | Só processa contatos com `active = true` |
| Validação de telefone | Aceita entre 10 e 15 dígitos numéricos; fora disso, pula e loga aviso |
| Erros de envio | Erros HTTP e falhas de rede são capturados individualmente — o script não para no primeiro erro |
| Delay | Não há pausa entre os envios; adicione `time.sleep()` se quiser evitar bloqueios por spam |
| Registro | Os envios não são gravados no banco — implemente uma coluna `sent_at` se precisar rastrear |

---

## Stack

- [Python 3](https://www.python.org/)
- [supabase-py](https://pypi.org/project/supabase/) `2.10.0`
- [Z-API](https://www.z-api.io/)
- [python-dotenv](https://pypi.org/project/python-dotenv/) `1.0.1`
- [requests](https://pypi.org/project/requests/) `2.32.3`

---

Projeto simples, funcional e fácil de customizar. Contribuições são bem-vindas.
