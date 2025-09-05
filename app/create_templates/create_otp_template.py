import requests

def create_otp_template(
    waba_id: str,
    access_token: str,
    template_name: str = "send_authentication_otp",
    language: str = "en_US",
    code_expiration_minutes: int = 10,
    button_text: str = "Copy Code"
):
    """
    Creates a WhatsApp authentication template with a COPY_CODE OTP button.

    Args:
        waba_id (str): WhatsApp Business Account ID
        access_token (str): Meta Graph API access token
        template_name (str): Name of the template
        language (str, optional): Template language (default: en_US)
        code_expiration_minutes (int, optional): Expiration time for OTP code (default: 10)
        button_text (str, optional): Text to display on the OTP button (default: "Copy Code")

    Returns:
        dict: API response in JSON format
    """
    url = f"https://graph.facebook.com/v23.0/{waba_id}/message_templates"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": template_name,
        "language": language,
        "category": "AUTHENTICATION",
        "components": [
            {
                "type": "BODY",
                "add_security_recommendation": True
            },
            {
                "type": "FOOTER",
                "code_expiration_minutes": code_expiration_minutes
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "OTP",
                        "otp_type": "COPY_CODE",
                        "text": button_text
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        return response.json()
    except Exception:
        return {"error": "Invalid JSON response", "raw": response.text}



