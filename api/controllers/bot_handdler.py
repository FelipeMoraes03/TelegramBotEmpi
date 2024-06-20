from typing import Dict

from api.controllers.generate_response import *
from api.config_bot import *

# Choose your model between 'GPT' and 'GEMINI'
MODEL='GEMINI'

INTRODUCTION_SOPHIA="Olá! Eu sou a Sofia, uma assistente virtual projetada para ajudar empreendedores com conselhos e informações relevantes para seus negócios. Antes de começarmos queria saber como você se chama?\n\n\nQuando quiser finalizar o chat, digite /end"

def introduce_sophia(msg: str) -> None:
    print(f"Sophia: {INTRODUCTION_SOPHIA}")
    bot.send_message(msg.chat.id, INTRODUCTION_SOPHIA)

def message_bot(msg: str, user_data: dict) -> Dict:
    response = gpt_call(msg.text) if MODEL == 'GPT' else gemini_call(msg.text, user_data, msg.chat.id)
    bot.send_message(msg.chat.id, response, parse_mode='Markdown')
    print(f"User: {msg.text}\nSophia: {response}")
    
    return {
            'request': msg.text,
            'response': response
        }