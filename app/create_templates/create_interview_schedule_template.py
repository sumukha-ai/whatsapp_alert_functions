import requests

def create_interview_schedule_template(
    waba_id: str,
    access_token: str,
    template_name: str = "interview_schedule_details_utility",
    language: str = "en",
    category: str = "UTILITY",
    base_interview_url: str = "https://sumukhaai.com/interviews"
):
    """
    Creates a compliant WhatsApp UTILITY template for sending a
    compulsory interview schedule with a 'View Details' button.

    Args:
        waba_id (str): WhatsApp Business Account ID.
        access_token (str): System user access token.
        template_name (str): The name for the new template.
        language (str): Template language code.
        category (str): The category of the template, must be 'UTILITY'.
        base_interview_url (str): The base HTTPS URL for the interview details page.

    Returns:
        dict: The JSON response from the Meta API.
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
                "text": "Mandatory Interview Schedule"
            },
            {
                "type": "BODY",
                "text": (
                    "Dear student,\n\n"
                    "Your interview has been scheduled with {{company_name}}.\n\n"
                    "• Timings: {{timings}}\n"
                    "• Venue: {{venue}}\n\n"
                    "Attendance for this interview is compulsory. Please ensure you are present at the specified time and location. Failure to attend may affect future opportunities."
                ),
                "example": {
                    "body_text_named_params": [
                        {"param_name": "company_name", "example": "Quantum Solutions"},
                        {"param_name": "timings", "example": "28-Oct-2025 at 2:00 PM"},
                        {"param_name": "venue", "example": "Main Auditorium, Central Campus"}
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
                        "example": ["QS-INT-15"]
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
