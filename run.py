from app import app
from app import config
from flask import Flask, request, jsonify


from app.whatsapp.send_otp import send_otp


from app.functions.get_facebook_access_token import get_access_token
from app.functions.subcribe_to_webhook import subscribe_to_webhook
from app.functions.register_phone_number import register_phone


from app.create_templates.create_otp_template import create_otp_template


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



if __name__ == '__main__':
    # send_otp(otp='123344', to='919900978577', phone_number_id=config.get('facebook', 'phone_number_id'), access_token=config.get('secrets','system_user_access_token')) 
    app.run(debug=True, port=8020)