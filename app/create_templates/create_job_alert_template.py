import requests

def create_job_alert_template(
    waba_id: str,
    access_token: str,
    template_name: str = "new_job_alert_with_named_params_url_param",
    language: str = "en_US",
    category: str = "MARKETING",
    base_job_url: str = "https://sumukhaai.com/jobs"
):
    """
    Creates a WhatsApp template using NAMED parameters with the correct `example` structure.

    - Sets `parameter_format` to "NAMED".
    - Uses named placeholders like `{{job_title}}`.
    - Places the `example` block inside each component with variables, as required.

    Args:
        waba_id (str): Your WhatsApp Business Account ID.
        access_token (str): Your system user access token.
        template_name (str): The name for the template.
        language (str): The language code for the template.
        category (str): The template category.
        base_job_url (str): The static HTTPS base of your job URL.

    Returns:
        dict: The API response from Meta.
    """
    url = f"https://graph.facebook.com/v20.0/{waba_id}/message_templates"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    if not base_job_url.startswith("https://"):
        raise ValueError("The base_job_url must be a valid HTTPS URL.")

    payload = {
        "name": template_name,
        "language": language,
        "category": category,
        "parameter_format": "NAMED",
        "allow_category_change": True,
        "components": [
            {
                "type": "HEADER",
                "format": "TEXT",
                "text": "New job alert!"
            },
            {
                "type": "BODY",
                "text": (
                    "Yay! A new job alert just popped up 🎉\n\n"
                    "• Role: {{job_title}} at {{company_name}}\n"
                    "• Location: {{job_location}} | {{job_type}}\n"
                    "• CTC: {{ctc}}\n"
                    "⏳ Apply by: {{deadline}}\n\n"
                    "🚀 Ready to take the next step? Tap the links below to apply or explore the full job details!"
                ),
                "example": {
                    "body_text_named_params": [
                        {"param_name": "job_title", "example": "Frontend Developer"},
                        {"param_name": "company_name", "example": "Acme Innovations"},
                        {"param_name": "job_location", "example": "Bengaluru (Hybrid)"},
                        {"param_name": "job_type", "example": "Full-time"},
                        {"param_name": "ctc", "example": "₹12-15 LPA"},
                        {"param_name": "deadline", "example": "20-Sep-2025"}                    ]
                }
            },
            {
                "type": "BUTTONS",
                "buttons": [
                    {
                        "type": "URL",
                        "text": "View Job Details",
                        "url": f"{base_job_url.strip()}/{{{{1}}}}",
                        "example": ["ACME-FED-01"] # Suffix placeholder example remains an array of strings
                    },
                    {
                        "type": "QUICK_REPLY",
                        "text": "Apply Now"
                    }
                ]
            }
            
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response", "status_code": response.status_code, "raw_text": response.text}

