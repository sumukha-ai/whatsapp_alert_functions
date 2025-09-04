from app import app
from app import config
from flask import Flask, request, jsonify


from app.whatsapp.send_otp import send_otp
from app.functions.get_facebook_access_token import get_access_token
from app.functions.subcribe_to_webhook import subscribe_to_webhook
@app.route('/get_facebook_token', methods=['POST'])
def facebook_token():
    data = request.get_json()
    code = data.get('code')
    result = get_access_token(code)
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


if __name__ == '__main__':
    # send_otp(otp='123344', to='919900978577', phone_number_id=config.get('facebook', 'phone_number_id'), access_token=config.get('secrets','system_user_access_token')) 
    app.run(debug=True, port=8020)