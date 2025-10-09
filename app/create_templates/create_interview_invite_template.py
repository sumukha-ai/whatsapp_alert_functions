import requests


def create_interview_invite_template(
    waba_id: str,
    access_token: str,
    template_name: str = "interview_invitation_utility",
    language: str = "en",
    category: str = "UTILITY",
    base_interview_url: str = "https://sumukhaai.com/interviews"
):
    """
    Creates a compliant WhatsApp UTILITY template for interview invitations
    using named parameters.

    Args:
        waba_id (str): WhatsApp Business Account ID.
        access_token (str): System user access token.
        template_name (str): Template name.
        language (str): Template language code.
        category (str): Should be 'UTILITY'.
        base_interview_url (str): Base HTTPS URL for interview details.

    Returns:
        dict: Meta API response.
    """
    if not base_interview_url.startswith("https://"):
        raise ValueError("The base_interview_url must be a valid HTTPS URL.")

    url = f"https://graph.facebook.com/v20.0/{waba_id}/message_templates"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "name": template_name,
        "language": language,
        "category": category,
        "parameter_format": "NAMED",
        "allow_category_change": False,
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "Interview Invitation"
            },
            {
                "type": "BODY",
                "text": (
                    "You have been invited for an interview with {{company_name}}.\n\n"
                    "• Number of Rounds: {{number_of_rounds}}\n"
                    "• Round 1 Timing: {{round1_timing}}\n"
                    "• Round 1 Venue: {{round1_venue}}\n\n"
                    "Click the button below for more details."
                ),
                "example": {
                    "body_text_named_params": [
                        {"param_name": "company_name", "example": "Innovate Solutions"},
                        {"param_name": "company_name", "example": "3"},
                        {"param_name": "round1_timing", "example": "25-Oct-2025 at 11:00 AM"},
                        {"param_name": "round1_venue", "example": "Virtual via Google Meet"}
                    ]
                }
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "URL",
                        "text": "View Details",
                        "url": f"{base_interview_url.strip()}/{{{{1}}}}",
                        "example": ["IS-DEV-05"]
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {
            "error": "Invalid JSON response",
            "status_code": response.status_code,
            "raw_text": response.text
        }