from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from api.database import save_chat_log
from api.utils import create_chat_message, create_chat_completion, count_message_tokens, count_string_tokens
from api.agent import get_context_with_history
from api.constants import OPENAI_CHAT_MODEL, OPENAI_CHAT_TOKEN_LIMIT, TWILIO_WHATSAPP_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_ACCOUNT_TOKEN

from api.memory import memory
from loguru import logger

import hashlib
import textwrap

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=['POST'])
def chat_webhook():
    
    incoming_msg = request.values.get('Body', '').lower()
    phone_number = request.values.get('From')
    
    user_id = str(hashlib.md5(str(phone_number).encode()).hexdigest())
    
    logger.info(f"user id: {user_id} len {len(user_id)}")
    context, total_tokens_used = get_context_with_history(user_id)
    context.append(create_chat_message("user", incoming_msg))
    
    total_tokens_used += count_string_tokens(incoming_msg, model_name=OPENAI_CHAT_MODEL)
    ai_reply = create_chat_completion(context, model=OPENAI_CHAT_MODEL, max_tokens=OPENAI_CHAT_TOKEN_LIMIT-total_tokens_used)
    
    resp = MessagingResponse()
    
    save_chat_log(user_id, incoming_msg, ai_reply)
    
    memory.add((
        f"User: {incoming_msg}\n"
        f"Assistant: {ai_reply}"
    ), user_id)

    logger.info(f"Message: {ai_reply} len {len(ai_reply)}")
    
    resp.message(ai_reply)
    return str(resp)
        
        

    

@chat_bp.route("/status_callback", methods=['POST'])
def status_callback():
    message_sid = request.values.get('MessageSid')
    message_status = request.values.get('MessageStatus')
    
    logger.info(f"Message SID {message_sid} has status {message_status}")
    return '', 204