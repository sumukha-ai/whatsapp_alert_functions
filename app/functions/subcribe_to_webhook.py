import os
import requests
import json

def subscribe_to_webhook(callback_uri, verify_token, waba_id, access_token):
    print(access_token)
    print('waba_id: ', waba_id)
    print('verify_token: ', verify_token)
    print('callback_uri: ', callback_uri)
    """
    Subscribes an app to webhook notifications with dynamic parameters.

    Args:
        callback_uri (str): The public URL of your webhook endpoint.
        verify_token (str): The secret token to verify webhook setup.
        app_id (str): The Facebook App ID to subscribe.
        access_token (str): The App Access Token for authorization.

    Returns:
        A tuple containing the HTTP status code and the JSON response from the server.
    """
    
    # The target URL is constructed using the app_id
    url = f'https://graph.facebook.com/v20.0/{waba_id}/subscribed_apps'

    # The headers, including the dynamic access token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # The JSON data payload now uses the function parameters
    payload = json.dumps({
        "override_callback_uri": callback_uri,
        "verify_token": verify_token
    })

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        print('response: ', response.json())
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Return the status code and the JSON response
        return response.status_code, response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        if e.response:
            print(f"Response Body: {e.response.text}")
        return None, None

