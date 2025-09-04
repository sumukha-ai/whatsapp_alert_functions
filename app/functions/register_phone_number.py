import requests
import json

def register_phone(phone_number_id, pin, access_token):
    """
    Registers a WhatsApp Business phone number by verifying it with a PIN.

    This function replicates the curl command to finalize the phone number
    registration process.

    Args:
        phone_number_id (str): The ID of the phone number to register.
        pin (str): The 6-digit PIN received via SMS or voice call.
        access_token (str): The access token for authorization.

    Returns:
        A tuple containing the HTTP status code and the JSON response from the server.
        Returns (None, None) if a request-related error occurs.
    """
    # The target URL is constructed using the phone_number_id
    url = f'https://graph.facebook.com/v20.0/{phone_number_id}/register'

    # The headers, including the dynamic access token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # The JSON data payload with the messaging product and PIN
    payload = {
        "messaging_product": "whatsapp",
        "pin": pin
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the status code and the JSON response
        return response.status_code, response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if e.response:
            print(f"Response Body: {e.response.text}")
        return None, None

