import requests

def send_otp(otp: str, to: str, phone_number_id: str, access_token: str,template_name: str, language_code: str = "en_US"):
    print('inside send_otp: ')
    """
    Sends an OTP via WhatsApp using the Cloud API and a template message.
    
    Parameters:
    - otp: The OTP code to send
    - to: Recipient phone number (including country code, no '+')
    - phone_number_id: The WhatsApp phone number ID from Facebook
    - access_token: The system user access token for authorization
    - language_code: Language code for the template (default 'en_US')
    """
    pid = int(phone_number_id)
    url = f"https://graph.facebook.com/v22.0/{pid}/messages"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    payload ={
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": to,
  "type": "template",
  "template": {
    "name": template_name,
    "language": {
      "code": language_code
    },
    "components": [
      {
        "type": "body",
        "parameters": [
          {
            "type": "text",
            "text": otp
          }
        ]
      },
      {
        "type": "button",
        "sub_type": "url",
        "index": "0",
        "parameters": [
          {
            "type": "text",
            "text": otp
          }
        ]
      }
    ]
  }
}

    response = requests.post(url, headers=headers, json=payload, timeout=15)
    response.raise_for_status()  # raise exception if the request failed
    return response.json()
