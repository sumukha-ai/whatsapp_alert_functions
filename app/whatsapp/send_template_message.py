import json
import logging
import requests
from flask import Blueprint
from app import config

logger = logging.getLogger(__name__)


def send_template_message(
    *,
    to: str,
    phone_number_id: str,
    template_name: str,
    language_code: str,
    body_parameters: list | None = None
):
    """
    Send a WhatsApp template message (Cloud API) using a payload structure
    aligned with the provided cURL example.

    body_parameters is a list of parameter dicts, each of which may be:
      - {"type": "text", "text": "text-string"}
      - {"type": "currency", "currency": {"fallback_value": "$100.99", "code": "USD", "amount_1000": 100990}}
      - {"type": "date_time", "date_time": {"fallback_value": "February 25, 1977", "day_of_week": 5, "year": 1977, "month": 2, "day_of_month": 25, "hour": 15, "minute": 33, "calendar": "GREGORIAN"}}
      You can also include header/footer/buttons components if needed by extending the components list below.
    """
    url = f"{config.get('facebook', 'graph_url_base')}/{config.get('facebook', 'graph_url_version')}/{phone_number_id}/messages"
    access_token = config.get('secrets', 'system_user_access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    components = []
    if body_parameters:
        components.append({
            "type": "body",
            "parameters": body_parameters
        })

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {"code": language_code},
            "components": components if components else []
        }
    }

    response = requests.post(url, headers=headers, json=payload, timeout=15)
    logger.info(f"Template message sent: status={response.status_code} body={response.text}")
    response.raise_for_status()
    return response.json()
