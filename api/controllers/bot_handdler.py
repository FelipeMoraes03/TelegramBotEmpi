from typing import Dict

from api.controllers.generate_response import *
from api.config_bot import *

# Choose your model between 'GPT' and 'GEMINI'
MODEL='GEMINI'

INTRODUCTION_SOPHIA="Olá! Eu sou a Sophia, uma assistente virtual projetada para ajudar empreendedores com conselhos e informações relevantes para seus negócios. Como posso te ajudar hoje?"

def introduce_sophia(msg: str) -> None:
    print(f"Sophia: {INTRODUCTION_SOPHIA}")
    bot.send_message(msg.chat.id, INTRODUCTION_SOPHIA)

def message_bot(msg: str) -> Dict:
    response = gpt_call(msg.text) if MODEL == 'GPT' else gemini_call(msg.text)
    bot.send_message(msg.chat.id, response)
    print(f"User: {msg.text}\nSophia: {response}")
    
    return {
            'request': msg.text,
            'response': response
        }