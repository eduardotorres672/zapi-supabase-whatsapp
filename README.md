Z-API Supabase WhatsApp

Script em Python que busca contatos ativos na tabela `contacts` do Supabase e envia mensagens personalizadas via Z-API (WhatsApp).

---

## Requisitos da Tabela

Crie a tabela no Supabase com o seguinte SQL:

```sql
CREATE TABLE contacts (
    id      BIGSERIAL PRIMARY KEY,
    name    TEXT    NOT NULL,
    phone   TEXT    NOT NULL,
    active  BOOLEAN NOT NULL DEFAULT TRUE
);

-- Exemplo de dados
INSERT INTO contacts (name, phone, active) VALUES
    ('Eduardo', '5511999999991', true),
    ('Victoria', '5511999999992', true),
    ('Carlos', '5511999999993', true);
Atenção: O campo phone deve conter apenas números (DDI + DDD + número).
Exemplo correto: 5511912345678

Configuração

Clone o repositório:Bashgit clone https://github.com/eduardotorres672/zapi-supabase-whatsapp.git
cd zapi-supabase-whatsapp
Copie o arquivo de exemplo:Bashcp env.example .env
Edite o arquivo .env e preencha suas credenciais:

env# Supabase
SUPABASE_URL=https://seusupabase.supabase.co
SUPABASE_KEY=sua_anon_key

# Z-API
ZAPI_INSTANCE_ID=seu_instance_id
ZAPI_TOKEN=seu_token
ZAPI_CLIENT_TOKEN=seu_client_token

Como Executar
Bashpython -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp env.example .env                # configure o .env
python main.py

Stack

Python 3
Supabase (supabase-py)
Z-API
python-dotenv
requests


Observações Importantes

A mensagem enviada está definida na variável message dentro do arquivo main.py
Apenas contatos com active = true são processados
O script não possui delay entre envios nem registra os envios realizados

Projeto simples, funcional e fácil de customizar.
