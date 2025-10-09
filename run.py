from app import app
from app import config
from flask import Flask, request, jsonify


from app.whatsapp.send_otp import send_otp


from app.functions.get_facebook_access_token import get_access_token
from app.functions.subcribe_to_webhook import subscribe_to_webhook
from app.functions.register_phone_number import register_phone
from app.functions.send_template import send_whatsapp_template

from app.create_templates.create_otp_template import create_otp_template
from app.create_templates.create_job_alert_template import create_job_alert_template
from app.create_templates.create_interview_invite_template import create_interview_invite_template
from app.create_templates.create_interview_schedule_template import create_interview_schedule_template


@app.route('/get_facebook_token', methods=['POST'])
def facebook_token():
    data = request.get_json()
    code = data.get('code')
    result = get_access_token(code)
    return jsonify(result)


@app.route('/subscribe_phone', methods=['POST'])
def subscribe_phone():
    data = request.get_json()
    phone_number_id = data.get('pid')
    pin = data.get('pin')
    access_token = data.get('access_token')
    result = register_phone(phone_number_id=phone_number_id, pin=pin, access_token=access_token)
    return jsonify(result)


@app.route('/subscribe_webhook', methods=['POST'])
def subscribe_webhook():
    data = request.get_json()
    waba_id = data.get('waba')
    call = data.get("callback_uri")
    access_token = data.get("access_token")
    test = data.get("test")
    result = subscribe_to_webhook(waba_id=waba_id, callback_uri=call,access_token=access_token,verify_token=test)
    return jsonify(result)


@app.route('/create_otp_template', methods=['POST'])
def create_otp():
    data = request.get_json()
    waba_id = data.get('waba')
    access_token = data.get("access_token")
    result = create_otp_template(waba_id=waba_id, access_token=access_token)
    return jsonify(result)


@app.route('/send_otp_network_call', methods=['POST'])
def send_otp_network_call():
    data = request.get_json()
    waba_id = data.get('waba')
    access_token = data.get("access_token")
    phone = data.get("pid")
    otp = data.get("otp")
    to = data.get("to")
    template_name = data.get("template_name")
    result = send_otp(otp=otp, to=to, phone_number_id=phone, access_token=access_token, template_name=template_name)
    return jsonify(result)


@app.route('/create_job_template', methods=['POST'])
def create_template_job():
    data = request.get_json()
    waba_id = data.get('waba')
    access_token = data.get("access_token")
    # phone = data.get("pid")
    # otp = data.get("otp")
    # to = data.get("to")
    # template_name = data.get("template_name")
    result = create_job_alert_template(waba_id=waba_id, access_token=access_token)
    return jsonify(result)


@app.route('/create_job_schedule_template', methods=['POST'])
def create_interview_invite_template_net_call():
    data = request.get_json()
    waba_id = data.get('waba')
    access_token = data.get("access_token")
    # phone = data.get("pid")
    # otp = data.get("otp")
    # to = data.get("to")
    # template_name = data.get("template_name")
    result = create_interview_invite_template(waba_id=waba_id, access_token=access_token)
    return jsonify(result)

@app.route('/create_interview_schedule_template', methods=['POST'])
def create_interview_schedule_template_net():
    data = request.get_json()
    waba_id = data.get('waba')
    access_token = data.get("access_token")
    # phone = data.get("pid")
    # otp = data.get("otp")
    # to = data.get("to")
    # template_name = data.get("template_name")
    result = create_interview_schedule_template(waba_id=waba_id, access_token=access_token)
    return jsonify(result)




@app.route("/send_job_alert", methods=["POST"])
def handle_send_job_alert():
    """
    An example endpoint that sends a job alert using hardcoded, false data
    for waba_id, access_token, and all template parameters.
    """
    
    data = request.get_json()
    waba_id = data.get('waba')
    pid = data.get("pid")
    access_token = data.get("access_token")
    to = data.get('to')
    
    template_name = "job_application_status_update_utility"
    
    body_named_params = {
        "job_title": "Lead Data Scientist",
        "company_name": "Sumukha AI",
        "job_location": "Bengaluru",
        "job_type": "Full-time",
        "ctc": "₹40-50 LPA",
        "deadline": "15-Oct-2025"
    }
    
    url_button_params = ["sumukha_ai"] # This will be the job slug

    # 3. Call the generic send function with the false data
    api_response = send_whatsapp_template(
        phone_number_id=pid,
        access_token=access_token,
        to_phone=to,
        template_name=template_name,
        named_params=body_named_params,
        button_params=url_button_params,
        language='en'
    )

    if "error" in api_response:
        return jsonify(api_response), 500
        
    return jsonify(api_response), 200

@app.route("/send_job_notification", methods=["POST"])
def handle_send_job_notif():
    """
    An example endpoint that sends a job alert using hardcoded, false data
    for waba_id, access_token, and all template parameters.
    """
    
    data = request.get_json()
    waba_id = data.get('waba')
    pid = data.get("pid")
    access_token = data.get("access_token")
    to = data.get('to')
    
    template_name = "interview_invitation_utility"
    
    body_named_params = {
        "company_name": "Lead Data Scientist",
        "number_of_rounds": "2",
        "round1_timing": "12AM",
        "round1_venue": "AI Room"
    }
    
    url_button_params = ["sumukha_ai"] # This will be the job slug

    # 3. Call the generic send function with the false data
    api_response = send_whatsapp_template(
        phone_number_id=pid,
        access_token=access_token,
        to_phone=to,
        template_name=template_name,
        named_params=body_named_params,
        button_params=url_button_params,
        language='en'
    )

    if "error" in api_response:
        return jsonify(api_response), 500
        
    return jsonify(api_response), 200

@app.route("/send_int_notification", methods=["POST"])
def handle_send_int():
    """
    An example endpoint that sends a job alert using hardcoded, false data
    for waba_id, access_token, and all template parameters.
    """
    
    data = request.get_json()
    waba_id = data.get('waba')
    pid = data.get("pid")
    access_token = data.get("access_token")
    to = data.get('to')
    
    template_name = "interview_schedule_details_utility"
    
    body_named_params = {
        "company_name": " Quantum Solutions ",
        "timings": "28-Oct-2025 at 2:00 PM",
        "venue": "Main Auditorium, Central Campus"
    
    }
    
    url_button_params = ["sumukha_ai"] # This will be the job slug

    # 3. Call the generic send function with the false data
    api_response = send_whatsapp_template(
        phone_number_id=pid,
        access_token=access_token,
        to_phone=to,
        template_name=template_name,
        named_params=body_named_params,
        button_params=url_button_params,
        language='en'
    )

    if "error" in api_response:
        return jsonify(api_response), 500
        
    return jsonify(api_response), 200


if __name__ == '__main__':
    # send_otp(otp='123344', to='919900978577', phone_number_id=config.get('facebook', 'phone_number_id'), access_token=config.get('secrets','system_user_access_token')) 
    app.run(debug=True, port=8020)