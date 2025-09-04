from app import app
from app import config
from flask import Flask, request, jsonify


from app.whatsapp.send_otp import send_otp
from app.functions.get_facebook_access_token import get_facebook_access_token

@app.route('/get_facebook_token', methods=['POST'])
def facebook_token():
    data = request.get_json()
    code = data.get('code')
    result = get_facebook_access_token(code)
    return jsonify(result)


if __name__ == '__main__':
    # send_otp(otp='123344', to='919900978577', phone_number_id=config.get('facebook', 'phone_number_id'), access_token=config.get('secrets','system_user_access_token')) 
    app.run(debug=True, port=8020)