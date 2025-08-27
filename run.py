from app import app
from app import config



from app.whatsapp.send_otp import send_otp
if __name__ == '__main__':
    send_otp(otp='123344', to='919900978577', phone_number_id=config.get('facebook', 'phone_number_id'), access_token=config.get('secrets','system_user_access_token')) 
    app.run(debug=True, port=8020)