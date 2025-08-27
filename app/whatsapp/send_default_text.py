import json
import logging
import requests
from flask import Blueprint
from app import  config
logger = logging.getLogger(__name__)


def send_default_text(to, phone_number_id, message):
    url = f"{config.get('facebook', 'graph_url_base')}/{config.get('facebook', 'graph_url_version')}/{phone_number_id}/messages"
    access_token = config.get('secrets', 'system_user_access_token')
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    logger.info(f"Default text message sent: {response.text}")

