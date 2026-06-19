import os
import re
import time
import logging
import argparse
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# Telefone só com dígitos, sem +, espaço ou traço (Z-API não aceita formatado)
PHONE_REGEX = re.compile(r"^\d{10,15}$")

# Templates de mensagem disponíveis
TEMPLATES = {
    "default":    "Olá, {name}! Tudo bem com você?",
    "promocao":   "Oi, {name}! Temos uma novidade especial esperando por você. Fale com a gente!",
    "lembrete":   "Olá, {name}. Passando para lembrar do seu compromisso. Qualquer dúvida, estamos aqui!",
    "reativacao": "Sentimos sua falta, {name}! Que tal a gente retomar o contato?",
}


# ---------------------------------------------------------------------------
# Supabase
# ---------------------------------------------------------------------------

def get_contacts(supabase, limit: int):
    """Busca contatos ativos que ainda não receberam mensagem (sent_at IS NULL)."""
    response = (
        supabase.table("contacts")
        .select("id, name, phone")
        .eq("active", True)
        .is_("sent_at", "null")
        .limit(limit)
        .execute()
    )
    return response.data


def mark_as_sent(supabase, contact_id: int, template: str, success: bool):
    """Registra o resultado do envio na tabela contacts."""
    now = datetime.now(timezone.utc).isoformat()
    supabase.table("contacts").update({
        "sent_at":          now if success else None,
        "last_template":    template,
        "last_status":      "sent" if success else "failed",
        "last_attempted_at": now,
    }).eq("id", contact_id).execute()


# ---------------------------------------------------------------------------
# Z-API
# ---------------------------------------------------------------------------

def send_whatsapp(name: str, phone: str, message: str) -> bool:
    """Envia mensagem de texto via Z-API. Retorna True em caso de sucesso."""
    instance_id  = os.environ["ZAPI_INSTANCE_ID"]
    token        = os.environ["ZAPI_TOKEN"]
    client_token = os.environ["ZAPI_CLIENT_TOKEN"]

    url = f"https://api.z-api.io/instances/{instance_id}/token/{token}/send-text"

    try:
        response = requests.post(
            url,
            json={"phone": phone, "message": message},
            headers={
                "Content-Type": "application/json",
                "Client-Token": client_token,
            },
            timeout=10,
        )
        response.raise_for_status()
        logger.info(f"enviado → {name} ({phone})")
        return True

    except requests.exceptions.HTTPError as e:
        logger.error(f"erro HTTP ao enviar pra {name}: {e.response.status_code} — {e.response.text}")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"falha de conexão pra {name}: {e}")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(
        description="Dispara mensagens WhatsApp para contatos ativos no Supabase via Z-API."
    )
    parser.add_argument(
        "--template",
        choices=TEMPLATES.keys(),
        default="default",
        help="Template de mensagem a usar (padrão: default)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Número máximo de contatos a processar por execução (padrão: 50)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Intervalo em segundos entre cada envio (padrão: 2.0)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula o envio sem chamar a Z-API nem gravar no banco",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])

    contacts = get_contacts(supabase, limit=args.limit)

    if not contacts:
        logger.info("nenhum contato pendente encontrado.")
        return

    logger.info(f"{len(contacts)} contato(s) encontrado(s) | template: {args.template} | delay: {args.delay}s")

    if args.dry_run:
        logger.warning("modo dry-run ativado — nenhuma mensagem será enviada.")

    template_str = TEMPLATES[args.template]
    enviados = 0
    falhas   = 0

    for contact in contacts:
        contact_id = contact.get("id")
        name       = contact.get("name", "").strip()
        phone      = contact.get("phone", "").strip()

        if not name or not phone:
            logger.warning(f"dado faltando, pulando: {contact}")
            falhas += 1
            continue

        if not PHONE_REGEX.match(phone):
            logger.warning(f"telefone fora do formato esperado, pulando {name}: '{phone}'")
            falhas += 1
            continue

        message = template_str.format(name=name)

        if args.dry_run:
            logger.info(f"[dry-run] simulando envio pra {name} ({phone}): {message!r}")
            enviados += 1
        else:
            success = send_whatsapp(name, phone, message)
            mark_as_sent(supabase, contact_id, args.template, success)

            if success:
                enviados += 1
            else:
                falhas += 1

            time.sleep(args.delay)

    logger.info(f"concluído — {enviados} enviado(s), {falhas} falha(s)")


if __name__ == "__main__":
    main() 
