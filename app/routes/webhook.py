import json
import logging
import re

from app.whatsapp.send_default_text import send_default_text
from app import config
from flask import Blueprint, abort, request, jsonify


webhook_bp = Blueprint('webhook', __name__)
logger = logging.getLogger(__name__)

def process_message_body(message, from_number, phone_number_id):
    greeting_keywords = ["hi", "hel", "hey", "heyy", "hii", "heya", "yo", "hol"]
    message_type = message.get("type", "")
    logger.info(f"Message type: {message_type}")

    if message_type == "text":
        
        text = message["text"]["body"].lower().strip()
        logger.info(f"text: {text}")
        print('text[:3]: ', text[:3])
        if (text[:3] in greeting_keywords):
            send_default_text(to=from_number, phone_number_id=phone_number_id, message="Hello")
        
    
         
    elif message_type == "interactive":
        interactive_type = message["interactive"].get("type")
        print('interactive_type: ', interactive_type)

        # Handle buttons
        if interactive_type == "button_reply":
            send_default_text(
                from_number,
                phone_number_id,
                "⚠️ You’re already in the middle of a flow. Please complete it before starting a new one.\n\nYou can also send *Hi* to restart the conversation."
            )
            button_id = message["interactive"]["button_reply"].get("id")
            # logger.info(f"Button clicked: {button_id}")
            
         
        # Handle flow submission
        elif interactive_type == "nfm_reply":
            flow_data_raw = message["interactive"]["nfm_reply"].get("response_json")
            flow_data = json.loads(flow_data_raw)
            # logger.info(f"Received flow data: {flow_data}")

          

          
        elif interactive_type == "list_reply":
            print('inside list_reply')
            button_id = message["interactive"]["list_reply"].get("id")
            
                

                
                
                
@webhook_bp.route("/webhook", methods=["POST"])
def real_estate_webhook():
    logger.info(">>>>> Inside webhook")
    try:
        request_json = request.json
        
        if not request_json["entry"][0]["changes"][0]["value"].get("messages", None):
            return jsonify(success=True)

        message = request_json["entry"][0]["changes"][0]["value"]["messages"][0]
        # print('****************message:**********************/n ', message,'****************message:**********************/n ')
        phone_number_id = request_json["entry"][0]["changes"][0]["value"]["metadata"]["phone_number_id"]
        from_number = message["from"]
        if len(from_number) == 12:
            from_number = from_number[2:]

        # logger.info(f"****************************************\nProcessing message from {from_number}\n**********************************************")
        process_message_body(message, from_number, phone_number_id)

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify(error=str(e)), 400

    return jsonify(success=True), 200

@webhook_bp.route("/webhook", methods=["GET"])
def whatsapp_webhook():
    logger.info("********************** WA verify token **********************")

    hub_mode = request.args.get('hub.mode')
    hub_verify_token = request.args.get('hub.verify_token')
    hub_challenge = request.args.get('hub.challenge')
    hub_verify_token_on_server = config.get('facebook','hub_verify_token')

    if hub_mode == "subscribe" and hub_verify_token == hub_verify_token_on_server:
        return str(hub_challenge)
    else:
        abort(401) #
