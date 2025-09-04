import requests
import os
from dotenv import load_dotenv

# Optional: Load from .env in development
load_dotenv()

def get_access_token(code: str):
    """
    Exchanges an authorization code for an access token using Facebook Graph API.

    Args:
        code (str): The authorization code received from the OAuth flow.

    Returns:
        dict: JSON response from Facebook or error details.
    """
    if not code:
        return {"error": "Missing 'code' parameter"}

    # Get environment variables
    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')
    grant_type = os.getenv('GRANT_TYPE', 'authorization_code')  # Default value

    if not client_id or not client_secret:
        return {"error": "CLIENT_ID or CLIENT_SECRET environment variable not set"}

    # Facebook OAuth URL
    url = "https://graph.facebook.com/v22.0/oauth/access_token"
    params = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'grant_type': grant_type
    }

    headers = {
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {
            "error": str(e),
            "details": e.response.json() if e.response else None
        }
