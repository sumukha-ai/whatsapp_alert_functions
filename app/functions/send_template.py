import requests
from typing import List, Dict, Optional, Union

def     send_whatsapp_template(
    phone_number_id: str,
    access_token: str,
    to_phone: str,
    template_name: str,
    language: str = "en_US",
    # Use either named_params OR the positional params (body_params, etc.)
    named_params: Optional[Dict[str, Union[str, int, float]]] = None,
    body_params: Optional[List[Union[str, int, float]]] = None,
    header_params: Optional[List[Union[str, int, float]]] = None,
    button_params: Optional[List[Union[str, int, float]]] = None
) -> dict:
    """
    Sends a WhatsApp Cloud API template message, supporting both named and positional parameters.

    Args:
        phone_number_id (str): Your sender Phone Number ID.
        access_token (str): Your Meta Graph API access token.
        to_phone (str): The recipient's WhatsApp number.
        template_name (str): The name of the approved template.
        language (str): The language code of the template.
        named_params (dict, optional): For named parameter templates. A dictionary where keys
                                      are the placeholder names (e.g., {"customer_name": "John"}).
        body_params (list, optional): For positional templates. A list of values for {{1}}, {{2}}, etc.
        header_params (list, optional): Positional values for header placeholders.
        button_params (list, optional): Positional values for button placeholders (e.g., URL suffix).

    Returns:
        dict: The API JSON response from Meta.
    """
    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    template_obj = {
        "name": template_name,
        "language": {"code": language}
    }
    
    components = []

    # --- Handle Header Parameters (Positional) ---
    if header_params:
        components.append({
            "type": "header",
            "parameters": [{"type": "text", "text": str(v)} for v in header_params]
        })

    # --- Handle Body Parameters ---
    if named_params:
        # **Corrected format for NAMED parameters**
        parameters = [
            {"type": "text", "parameter_name": key, "text": str(value)}
            for key, value in named_params.items()
        ]
        components.append({"type": "body", "parameters": parameters})
    elif body_params:
        # Fallback for POSITIONAL parameters
        components.append({
            "type": "body",
            "parameters": [{"type": "text", "text": str(v)} for v in body_params]
        })

    # --- Handle Button Parameters (Positional Suffix) ---
    if button_params:
        components.append({
            "type": "button",
            "sub_type": "url",
            "index": "0", # Assumes the first button is the URL button
            "parameters": [{"type": "text", "text": str(v)} for v in button_params]
        })

    if components:
        template_obj["components"] = components

    payload = {
        "messaging_product": "whatsapp",
        "to": to_phone,
        "type": "template",
        "template": template_obj
    }

    response = requests.post(url, headers=headers, json=payload)
    
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_text": response.text}

